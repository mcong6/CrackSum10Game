import cv2
import pytesseract

from config import cell_width, cell_center_start_x, cell_center_start_y, board_start_y, board_start_x
from mouse_motion_controller import MouseMotionController
from solver import solve_board_by_chunks, FindSum10Lazy
from utils import ocr_results_to_arr, show_image, save_screen_shot, transform_matrix


class DetectNumbersFromBoard:
    def __init__(self, image_path, board_start_x=None, board_start_y=None, cell_width=None):
        self.binary_thresh = None
        self.adaptive_thresh = None
        self.resized = None
        self.original_image = None
        self.image_path = image_path
        self.preprocess_image()
        self.board_start_x = board_start_x
        self.board_start_y = board_start_y
        self.cell_width = cell_width * 2 if cell_width is not None else None

    def enhance_resized_image(self, resized_image):
        """
        Preprocess the image to improve OCR accuracy.
        """
        # Apply CLAHE for better contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(resized_image)
        # Apply adaptive thresholding
        adaptive_thresh = cv2.adaptiveThreshold(
            enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 5
        )
        return adaptive_thresh

    def preprocess_image(self):
        # Load the image
        self.original_image = cv2.imread(self.image_path)
        # Preprocessing
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        self.resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        self.adaptive_thresh = cv2.adaptiveThreshold(self.resized, 255,
                                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                     cv2.THRESH_BINARY_INV, 11, 2)
        _, self.binary_thresh = cv2.threshold(self.resized, 20, 255, cv2.THRESH_BINARY)
        return self.adaptive_thresh, self.binary_thresh

    def extract_numbers_from_board(self):
        # Detect horizontal contours for rows
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 3))  # Adjust height (20) for row detection
        horizontal_lines = cv2.morphologyEx(self.adaptive_thresh, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(horizontal_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Sort contours by their vertical position (y-coordinate)
        contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])
        show_image(self.binary_thresh)
        # Extract numbers row by row
        matrix = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if h > 15:  # Filter out small contours
                adaptive_row_image = self.adaptive_thresh[y:y + h, :]
                binary_row_image = self.binary_thresh[y:y + h, :]
                resized_image = self.resized[y:y + h, :]
                detected_row = self.extract_numbers_from_row(adaptive_row_image, binary_row_image, resized_image)
                show_image(adaptive_row_image)
                matrix.append(detected_row)
        return matrix

    def extract_numbers_from_board_with_empty_cell(self):
        # Extract numbers row by row
        matrix = []
        for y in range(0, int(self.cell_width * 16), int(self.cell_width)):
            adaptive_row_image = self.adaptive_thresh[y:y + self.cell_width, :]
            binary_row_image = self.binary_thresh[y:y + self.cell_width, :]
            resized_image = self.resized[y:y + self.cell_width, :]
            detected_row = self.extract_numbers_from_row_with_empty_cells(adaptive_row_image, binary_row_image,
                                                                          resized_image)
            show_image(binary_row_image)
            matrix.append(detected_row)
        return matrix

    def extract_numbers_from_row(self, adaptive_row_image, binary_image, resized_image):
        # Detect vertical contours for rows
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 5))  # Adjust height (20) for row detection
        horizontal_lines = cv2.morphologyEx(adaptive_row_image, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(horizontal_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Sort contours by their vertical position (y-coordinate)
        contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])
        row = []

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 10:  # Filter out small contours
                binary_cell_image = binary_image[:, x:x + w]
                detected_number = self.detect_single_number(binary_cell_image)
                if len(detected_number) == 0:
                    resized_cell_image = resized_image[:, x:x + w]
                    number = self.redetect_single_number(resized_cell_image, psm_config=8)
                    if number != "":
                        print(f"Detected missing number: {number}")
                        detected_number = [int(number)]
                if len(detected_number) == 0:
                    resized_cell_image = resized_image[:, x:x + w]
                    resized = cv2.resize(resized_cell_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                    number = self.redetect_single_number(resized, psm_config=10)
                    if number != "":
                        print(f"Detected missing number: {number}")
                        detected_number = [int(number)]
                    else:
                        show_image(resized_cell_image)
                if len(detected_number) == 0:
                    detected_number = [0]
                row.append(detected_number)
        print(f"row:{row}")
        return row

    def extract_numbers_from_row_with_empty_cells(self, adaptive_row_image, binary_image, resized_image):
        # Detect horizontal contours for rows
        row = []
        w = cell_width*2
        for x in range(8, int(w * 10), int(w)):
            binary_cell_image = binary_image[:, x:x + w]
            show_image(binary_cell_image)
            detected_number = self.detect_single_number(binary_cell_image)
            if len(detected_number) == 0:
                resized_cell_image = resized_image[:, x:x + w]
                number = self.redetect_single_number(resized_cell_image, psm_config=10)
                if number != "":
                    print(f"Detected missing number: {number}")
                    detected_number = [int(number)]
            if len(detected_number) == 0:
                resized_cell_image = resized_image[:, x:x + w]
                resized = cv2.resize(resized_cell_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                number = self.redetect_single_number(resized, psm_config=8)
                if number != "":
                    print(f"Detected missing number: {number}")
                    detected_number = [int(number)]
            if len(detected_number) == 0:
                show_image(binary_cell_image)
                detected_number = [0]
            row.append(detected_number)
        print(f"row:{row}")
        show_image(binary_image)
        return row

    def detect_single_number(self, binary_thresh):
        custom_config = r'--psm 10 -c tessedit_char_whitelist=123456789'  # 6, 10
        ocr_result = pytesseract.image_to_string(binary_thresh, config=custom_config)
        arr = ocr_results_to_arr(ocr_result)
        return arr

    def redetect_single_number(self, image_path, psm_config):
        """
        Detect a single number in the provided image.
        """
        # Preprocess the image
        preprocessed = self.enhance_resized_image(image_path)
        # Specify Tesseract OCR configuration
        custom_config = fr'--psm {psm_config} -c tessedit_char_whitelist=0123456789'
        # Perform OCR
        detected_text = pytesseract.image_to_string(preprocessed, config=custom_config)
        # Extract only numeric characters
        number = ''.join(filter(str.isdigit, detected_text))
        return number


def run(matrix=None):
    region = (board_start_x, board_start_y, cell_width * 10, cell_width * 16 - 10)  # webpage
    image_path = 'screenshot.png'
    save_screen_shot(region, image_path)
    if matrix is None:
        matrix = DetectNumbersFromBoard(image_path).extract_numbers_from_board()
        matrix = transform_matrix(matrix)
    print(f"Matrix is:")
    for line in matrix:
        print(line)
    print("Start selecting numbers.")
    best_operation = solve_board_by_chunks(matrix, 4)

    for each_cord in best_operation:
        x1, y1, x2, y2 = each_cord
        MouseMotionController(cell_center_start_x, cell_center_start_y, cell_width).select_rectangle(x1, y1, x2, y2)
    print(f"finished one round")

    save_screen_shot(region, image_path)
    matrix = DetectNumbersFromBoard(image_path, board_start_x, board_start_y,
                                    cell_width).extract_numbers_from_board_with_empty_cell()
    matrix = transform_matrix(matrix)
    print(f"matrix is:")
    for line in matrix:
        print(line)
    print("Start selecting numbers.")
    solver = FindSum10Lazy(matrix)
    solver.start_solver()
    print(f"Coordination of number combo: {solver.res}")
    for each_cord in solver.res:
        x1, y1, x2, y2 = each_cord
        MouseMotionController(cell_center_start_x, cell_center_start_y, cell_width).select_rectangle(x1, y1, x2, y2)
    print(f"finished one round")


if __name__ == '__main__':
    run()

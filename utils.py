import cv2
import pyautogui

from config import display_img


def show_image(image):
    cv2.imshow("image", image)
    if display_img:
        cv2.waitKey(0)
    cv2.destroyAllWindows()


def ocr_results_to_arr(ocr_result):
    arr = []
    for line in ocr_result.splitlines():
        if line.strip():  # Skip empty lines
            row = [int(num) for num in line.split() if num.isdigit()]
            arr += row
    return arr


def transform_matrix(original_matrix):
    matrix = []
    for row in original_matrix:
        transformed_row = []
        for cell in row:
            transformed_row.append(cell[0])
        matrix.append(transformed_row)
    return matrix


def matrix_diff(matrix_1, matrix_2):
    num_row = len(matrix_1)
    num_col = len(matrix_1[0])
    diff = 0
    for i in range(num_row):
        for j in range(num_col):
            diff += abs(matrix_1[i][j] - matrix_2[i][j])

    return diff == 0


def save_screen_shot(region, path):
    # Take the screenshot
    screenshot = pyautogui.screenshot(region=region)
    # Save the screenshot
    screenshot.save(path)

"""Utility functions for image processing and data manipulation."""

import cv2
import pyautogui
from typing import List, Any, Tuple, Optional

from config import Config


class ImageUtils:
    """Image processing utilities."""
    
    @staticmethod
    def show_image(image: Any, window_name: str = "image") -> None:
        """Display image with optional debug mode."""
        cv2.imshow(window_name, image)
        if Config.DISPLAY_IMG:
            cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    @staticmethod
    def save_screenshot(region: Tuple[int, int, int, int], path: str) -> None:
        """Take and save screenshot of specified region."""
        screenshot = pyautogui.screenshot(region=region)
        screenshot.save(path)


class OCRUtils:
    """OCR result processing utilities."""
    
    @staticmethod
    def ocr_results_to_array(ocr_result: str) -> List[int]:
        """Convert OCR text results to array of integers."""
        numbers = []
        for line in ocr_result.splitlines():
            if line.strip():  # Skip empty lines
                row_numbers = [int(num) for num in line.split() if num.isdigit()]
                numbers.extend(row_numbers)
        return numbers


class MatrixUtils:
    """Matrix manipulation utilities."""
    
    @staticmethod
    def transform_matrix(original_matrix: List[List[List[int]]]) -> List[List[int]]:
        """Transform nested matrix structure to simple 2D matrix."""
        matrix = []
        for row in original_matrix:
            transformed_row = [cell[0] for cell in row]
            matrix.append(transformed_row)
        return matrix
    
    @staticmethod
    def matrices_equal(matrix_1: List[List[int]], matrix_2: List[List[int]]) -> bool:
        """Check if two matrices are equal."""
        if len(matrix_1) != len(matrix_2) or len(matrix_1[0]) != len(matrix_2[0]):
            return False
        
        for i in range(len(matrix_1)):
            for j in range(len(matrix_1[0])):
                if matrix_1[i][j] != matrix_2[i][j]:
                    return False
        return True
    
    @staticmethod
    def calculate_matrix_sum(matrix: List[List[int]], 
                           x1: int, y1: int, x2: int, y2: int) -> int:
        """Calculate sum of matrix elements in specified range."""
        total = 0
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                total += matrix[i][j]
        return total


show_image = ImageUtils.show_image
ocr_results_to_arr = OCRUtils.ocr_results_to_array
transform_matrix = MatrixUtils.transform_matrix
matrix_diff = lambda m1, m2: MatrixUtils.matrices_equal(m1, m2)
save_screen_shot = ImageUtils.save_screenshot
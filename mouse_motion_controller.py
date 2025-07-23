"""Mouse motion controller for game automation."""

import pyautogui
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class MouseMotionController:
    """Handles mouse movements and selections for the game grid."""

    def __init__(self, start_x: int, start_y: int, cell_offset: int):
        """
        Initialize mouse controller.
        
        Args:
            start_x: Starting X coordinate of the grid
            start_y: Starting Y coordinate of the grid
            cell_offset: Pixel offset between grid cells
        """
        self.start_x = start_x
        self.start_y = start_y
        self.cell_offset = cell_offset

        # Configure pyautogui
        pyautogui.PAUSE = 0.1
        pyautogui.FAILSAFE = True

    def _convert_grid_to_pixel(self, x_idx: int, y_idx: int) -> Tuple[int, int]:
        """Convert grid indices to pixel coordinates."""
        x_pixel = self.start_x + x_idx * self.cell_offset
        y_pixel = self.start_y + y_idx * self.cell_offset
        return x_pixel, y_pixel

    def _get_rectangle_coordinates(self, x1_idx: int, y1_idx: int,
                                   x2_idx: int, y2_idx: int) -> Tuple[int, int, int, int]:
        """Get pixel coordinates for rectangle selection."""
        x1_pixel, y1_pixel = self._convert_grid_to_pixel(x1_idx, y1_idx)
        x2_pixel, y2_pixel = self._convert_grid_to_pixel(x2_idx, y2_idx)

        logger.info(f"Rectangle coordinates: ({x1_pixel}, {y1_pixel}) to ({x2_pixel}, {y2_pixel})")
        return x1_pixel, y1_pixel, x2_pixel, y2_pixel

    def select_rectangle(self, y1_idx: int, x1_idx: int, y2_idx: int, x2_idx: int) -> None:
        """
        Select a rectangle on the game grid.
        
        Args:
            y1_idx: Starting row index
            x1_idx: Starting column index  
            y2_idx: Ending row index
            x2_idx: Ending column index
        """
        try:
            x1, y1, x2, y2 = self._get_rectangle_coordinates(x1_idx, y1_idx, x2_idx, y2_idx)
            # Move to starting position and click
            pyautogui.moveTo(x1, y1, duration=0)
            pyautogui.click()
            # Drag to ending position
            pyautogui.dragTo(x2, y2, duration=0, button="left")
            logger.info(f"Selected rectangle from grid ({x1_idx}, {y1_idx}) to ({x2_idx}, {y2_idx})")
        except Exception as e:
            logger.error(f"Failed to select rectangle: {e}")
            raise

import pyautogui


class MouseMotionController:
    def __init__(self, start_x, start_y, offset):
        self.start_x = start_x
        self.start_y = start_y
        self.offset = offset

    def convert_idx_to_pixel(self, x1_idx, y1_idx, x2_idx, y2_idx):
        x1_pixel = self.start_x + x1_idx * self.offset
        y1_pixel = self.start_y + y1_idx * self.offset
        x2_pixel = self.start_x + x2_idx * self.offset
        y2_pixel = self.start_y + y2_idx * self.offset
        print(f"x1:{x1_pixel}, y1:{y1_pixel}, x2:{x2_pixel}, y2:{y2_pixel}")
        return x1_pixel, y1_pixel, x2_pixel, y2_pixel

    def select_rectangle(self, y1_idx, x1_idx, y2_idx, x2_idx):
        x1, y1, x2, y2 = self.convert_idx_to_pixel(x1_idx, y1_idx, x2_idx, y2_idx)
        pyautogui.moveTo(x1, y1, duration=0)
        pyautogui.click()
        pyautogui.dragTo(x2, y2, duration=0, button="left")
        # pyautogui.moveTo(x2, y2, duration=0.2)

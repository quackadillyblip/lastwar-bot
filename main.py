import pygetwindow as gw
import pyautogui
import win32gui
import cv2
import numpy as np
import time
import os

class WindowBot:
    def __init__(self, window_title):
        self.window_title = window_title
        self.window = self.find_window()

    def find_window(self):
        for w in gw.getWindowsWithTitle(self.window_title):
            if not w.isMinimized and win32gui.IsWindowVisible(w._hWnd):
                print(f"✅ Venster gevonden: {w.title}")
                return w
        print("❌ Venster niet gevonden!")
        return None

    def get_window_rect(self):
        if self.window:
            return (self.window.left, self.window.top, self.window.width, self.window.height)
        return None

    def take_screenshot(self):
        rect = self.get_window_rect()
        if rect:
            left, top, width, height = rect
            return pyautogui.screenshot(region=(left, top, width, height))
        return None

    def find_template(self, template_path, threshold=0.85):
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            # print(f"❌ Template '{template_path}' niet gevonden of niet leesbaar.")
            return None

        rect = self.get_window_rect()
        if rect:
            left, top, width, height = rect
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
        else:
            screenshot = pyautogui.screenshot()  # volledige scherm als fallback
            left, top = 0, 0

        screenshot = screenshot.convert("L")
        screenshot_cv = np.array(screenshot)

        if screenshot_cv.shape[0] < template.shape[0] or screenshot_cv.shape[1] < template.shape[1]:
            print(f"❌ Template groter dan screenshot! Template: {template.shape}, Screenshot: {screenshot_cv.shape}")
            return None

        result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            template_h, template_w = template.shape[:2]
            match_x = left + max_loc[0] + template_w // 2
            match_y = top + max_loc[1] + template_h // 2
            return match_x, match_y
        return None

    def click_at(self, x, y):
        print(f"🖱️ Klik op ({x}, {y})")
        pyautogui.click(x, y)

    def act_on_template(self, template_name, clicks=1):
        path = os.path.join("templates", template_name)
        coords = self.find_template(path)
        if coords:
            print(f"✅ Template gevonden op {coords}, klikken...")
            for _ in range(clicks):
                self.click_at(*coords)
            return True
        else:
            # print(f"❌ Template '{template_name}' niet gevonden.")
            return False

if __name__ == "__main__":
    # pyautogui.FAILSAFE = False  # Alleen aanzetten als je zeker weet wat je doet
    bot = WindowBot("Last War-Survival Game")
    if bot.window:
        while True:
            bot.act_on_template("help_button.png")
            bot.act_on_template("survivor_found.png")
            bot.act_on_template("survivor_claim.png", 2)
            time.sleep(2)

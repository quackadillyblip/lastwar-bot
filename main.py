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
                print(f"✅ Window found: {w.title}")
                return w
        print("❌ Window not found!")
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
            # print(f"❌ Template '{template_path}' not found or unreadable.")
            return None

        rect = self.get_window_rect()
        if rect:
            left, top, width, height = rect
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
        else:
            screenshot = pyautogui.screenshot()  # fallback to full screen
            left, top = 0, 0

        screenshot = screenshot.convert("L")
        screenshot_cv = np.array(screenshot)

        if screenshot_cv.shape[0] < template.shape[0] or screenshot_cv.shape[1] < template.shape[1]:
            print(f"❌ Template is larger than screenshot! Template: {template.shape}, Screenshot: {screenshot_cv.shape}")
            return None

        result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            template_h, template_w = template.shape[:2]
            match_x = left + max_loc[0] + template_w // 2
            match_y = top + max_loc[1] + template_h // 2
            return match_x, match_y
        return None
    def find_all_templates(self, template_path, threshold=0.85):
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            return []

        rect = self.get_window_rect()
        if rect:
            left, top, width, height = rect
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
        else:
            screenshot = pyautogui.screenshot()
            left, top = 0, 0

        screenshot = screenshot.convert("L")
        screenshot_cv = np.array(screenshot)

        result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)

        matches = []
        template_h, template_w = template.shape[:2]
        for pt in zip(*locations[::-1]):  # Switch columns/rows
            match_x = left + pt[0] + template_w // 2
            match_y = top + pt[1] + template_h // 2
            matches.append((match_x, match_y))

        return matches

    def click_at(self, x, y):
        print(f"🖱️ Click at ({x}, {y})")
        pyautogui.click(x, y)

    def act_on_template(self, template_name, clicks=1):
        path = os.path.join("templates", template_name)
        coords = self.find_template(path)
        if coords:
            print(f"✅ Template found at {coords}, clicking...")
            for _ in range(clicks):
                self.click_at(*coords)
            return True
        else:
            # print(f"❌ Template '{template_name}' not found.")
            return False

if __name__ == "__main__":
    bot = WindowBot("Last War-Survival Game")
    if bot.window:
        while True:
            bot.act_on_template("help_button.png")
            bot.act_on_template("survivor_found.png")
            bot.act_on_template("survivor_claim.png", 2)
            if bot.act_on_template("open_dig.png"):
                time.sleep(0.5)

            if bot.act_on_template("goto_dig.png"):
                time.sleep(0.5)

                # Click join_dig (center of the window)
                rect = bot.get_window_rect()
                if rect:
                    join_x = rect[0] + rect[2] // 2
                    join_y = rect[1] + rect[3] // 2
                    bot.click_at(join_x, join_y)
                    time.sleep(0.5)

                    # Click march (horizontal center, fixed y=880)
                    march_x = rect[0] + rect[2] // 2
                    march_y = 880
                    bot.click_at(march_x, march_y)
                    time.sleep(0.5)
            kuroi_posts = bot.find_all_templates(os.path.join("templates", "kuroi_like.png"))
            liked_icons = bot.find_all_templates(os.path.join("templates", "kuroi_liked.png"))

            for x_post, y_post in kuroi_posts:
                has_like_below = False

                for x_liked, y_liked in liked_icons:
                    if y_liked > y_post:
                        has_like_below = True
                        break

                if not has_like_below:
                    x_click = 150
                    y_click = y_post + 40
                    # print(f"👍 Clicking like for post at ({x_post}, {y_post}) -> ({x_click}, {y_click})")
                    # print(f"<3 liked at ({x_liked}, {y_liked})")
                    bot.click_at(x_click, y_click)
                    time.sleep(0.5)

                    # Confirm like
                    bot.act_on_template("help_button.png")
                    time.sleep(0.5)

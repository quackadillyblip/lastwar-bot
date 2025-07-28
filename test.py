import pygetwindow as gw
import pyautogui
import win32gui
from PIL import ImageChops

window_title = "Last War-Survival Game"
window = None

# Zoek een venster met die titel
for w in gw.getWindowsWithTitle(window_title):
    if not w.isMinimized and win32gui.IsWindowVisible(w._hWnd):
        window = w
        break

if window is None:
    print("❌ Venster niet gevonden!")
else:
    # Breng venster naar voor (optioneel)
    # window.activate()

    # Venstercoördinaten
    left, top, width, height = window.left, window.top, window.width, window.height

    # Screenshot nemen
    screenshot = pyautogui.screenshot(region=(left, top, width, height))

    # Opslaan en tonen
    screenshot.save("screenshot.png")
    screenshot.show()

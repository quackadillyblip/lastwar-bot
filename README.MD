# Last War PC Bot

**Contact:** dindunuffin1234@proton.me

## Description

A bot for the **PC version** of *Last War: Survival*, using OpenCV to detect and interact with UI elements based on template matching.

> ⚠️ The game **must be running in a fixed resolution** — you **can move** the window, but **cannot resize** it.  
> ⚠️ The game window must be **active and visible on-screen** because detection relies on screenshots.  
> ⚠️ The bot will **take over your mouse** during use and will click when UI elements are detected.

---

## Features

- Button detection via OpenCV template matching
- Simple logic for navigating UI and interacting with elements
- Easy to update templates based on your own screenshots

---

## Usage

1. **Launch the game** in the correct resolution.
2. **Ensure** the game window is **active and on-screen**.
3. **Place your template images** into the `templates/` folder.
4. **Run the bot**:

   ```bash
   python main.py

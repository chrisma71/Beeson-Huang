import pyautogui
import pygetwindow as gw
import os
import time

# Define the folder name
folder_name = 'screenshots'

# Create the folder if it doesn't exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Define the file path
file_path = os.path.join(folder_name, 'screenshot.png')

# Switch to the Google Chrome window
window_title = 'Google Chrome'
windows = gw.getWindowsWithTitle(window_title)
if windows:
    chrome_window = windows[0]
    chrome_window.activate()
    time.sleep(2)  # Wait for the window to activate

    # Define the region to capture (left, top, width, height)
    region = (620, 220, 650, 800)  # Adjust these values as needed

    # Take a screenshot of the specified region
    screenshot = pyautogui.screenshot(region=region)

    # Save the screenshot
    screenshot.save(file_path)

    print(f"Screenshot of the region {region} taken and saved as '{file_path}'")
else:
    print(f"No window with title '{window_title}' found.")

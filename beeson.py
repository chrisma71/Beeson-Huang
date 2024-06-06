from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def open_tetrio_and_play_solo():
    # Set up the ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # URL of the website you want to open
    url = "https://tetr.io"

    # Open the URL
    driver.get(url)

    try:
        # Wait for the JOIN button to be clickable and then click it
        join_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "entry_button"))
        )
        join_button.click()
        print("JOIN button clicked.")

        # Wait for the SOLO button to be visible and then click it
        solo_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "play_solo"))
        )
        solo_button.click()
        print("SOLO button clicked.")

        zen_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "game_zen"))
        )
        zen_button.click()
        print("ZEN button clicked.")

        play_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "start_zen"))
        )
        play_button.click()
        print("PLAY button clicked.")
        

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Optionally, you can close the browser after the action
        time.sleep(60)
        driver.quit()


open_tetrio_and_play_solo()

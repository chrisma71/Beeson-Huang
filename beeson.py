from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def open_tetrio():
    # Set up the ChromeDriver

    # URL of the website you want to open
    url = "https://tetr.io"

    # Open the URL
    driver.get(url)

def sign_in():
    # Wait for the username input field to be visible and then enter the username
    username_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "entry_username"))
    )
    username_input.send_keys("beeson")
    print("Entered username: beeson")

    # Wait for the JOIN button to be clickable and then click it
    join_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "entry_button"))
    )
    join_button.click()
    print("JOIN button clicked.")

    password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login_password"))
    )
    password_input.send_keys("beeson")
    print("Entered Password")

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login_button"))
    )
    login_button.click()
    print("LOGIN button clicked.")

    try:
        cool_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='oob_button flex-item pri' and text()='COOL!']"))
        )
        cool_button.click()
        print("COOL! button clicked.")
    except:
        print("COOL! button not present, continuing.")
       
def play_zen():
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

def join_custom(room_id):

    multi_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "play_multi"))
    )
    multi_button.click()
    print("MULTI button clicked.")

    room_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "multi_join"))
    )
    room_input.send_keys(room_id)
    print(f"Entered room ID: {room_id}")

    room_input.send_keys('\n') 

def apply_config():

    config_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "sig_config"))
    )
    config_button.click()
    print("CONFIG button clicked.")

    handling_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h1[@title='Change the way TETR.IO feels']"))
    )
    handling_button.click()
    print("HANDLING button clicked.")

    handling_arr_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "handling_arr_field"))
    )
    handling_arr_field.click()
    handling_arr_field.clear()
    handling_arr_field.send_keys("0")
    print("ARR = 0F")

    handling_das_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "handling_das_field"))
    )
    handling_das_field.click()
    handling_das_field.clear()
    handling_das_field.send_keys("1")
    print("DAS = 1F")

    handling_dcd_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "handling_dcd_field"))
    )
    handling_dcd_field.click()
    handling_dcd_field.clear()
    handling_dcd_field.send_keys("0")
    print("DCD = 0F")

    handling_sdf_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "handling_sdf_field"))
    )
    handling_sdf_field.click()
    handling_sdf_field.clear()
    handling_sdf_field.send_keys("41")
    print("SDF = 41F")








driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
open_tetrio()
sign_in()
apply_config()
time.sleep(60)
driver.quit()
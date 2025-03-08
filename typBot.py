import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Add safety delay to prevent immediate execution
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

def open_and_automate():
    # Initialize Chrome driver
    driver = webdriver.Chrome()
    
    # Open initial URL for login
    driver.get('http://localhost:5173')
    time.sleep(2)  # Wait for page to load
    
    try:
        # Login process
        # Find and fill email
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="email"]'))
        )
        email_field.send_keys('demo')
        
        # Find and fill password
        password_field = driver.find_element(By.XPATH, '//*[@id="password"]')
        password_field.send_keys('7410')
        
        # Submit login form
        password_field.send_keys('\n')
        time.sleep(2)  # Wait for login to complete
        
        # Navigate to chats page
        driver.get('http://localhost:5173/chats')
        time.sleep(2)  # Wait for page to load
        
        # Click on profile
        profile_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="profile"]'))
        )
        profile_element.click()
        time.sleep(1)
        
        # Find and fill message input
        message_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/main/div/div[2]/div[2]/div[3]/div/form/div/div/input'))
        )
        message_input.send_keys('hi')
        
        # Find and click send button
        send_button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/main/div/div[2]/div[2]/div[3]/div/form/button')
        send_button.click()
        
        # Keep the window open indefinitely
        while True:
            time.sleep(1)
            
    except Exception as e:
        print(f"Error occurred: {e}")
    except KeyboardInterrupt:
        print("\nScript stopped by user")
    finally:
        pass  # Do nothing to keep the window open

if __name__ == "__main__":
    print("Starting automation in 3 seconds...")
    print("Press Ctrl+C in the terminal to stop the script when needed")
    time.sleep(3)
    open_and_automate()

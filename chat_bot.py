from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random

class YoutubeLiveChatBot:
    def __init__(self):
        chrome_options = Options()
        
        # Add options to use your default profile
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_argument("--user-data-dir=C:\\Users\\%USERNAME%\\AppData\\Local\\Google\\Chrome\\User Data")
        
        # Disable some features we don't need
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 20)
        except Exception as e:
            print(f"Error starting Chrome: {str(e)}")
            print("Make sure Chrome is closed before running this script!")
            raise e

    def join_live_chat(self):
        try:
            print("Opening YouTube live stream...")
            self.driver.get("https://www.youtube.com/live/1UAlQPsV_2s?si=hj5PPjk7_nbLuAuJ")
            time.sleep(5)
        except Exception as e:
            print(f"Error joining chat: {str(e)}")

    def send_message(self, message):
        try:
            # Wait for chat input to be present and clickable
            chat_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#input.style-scope.yt-live-chat-text-input-field-renderer")))
            chat_input.click()
            chat_input.send_keys(message)
            
            # Send message
            send_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#send-button")))
            send_button.click()
            print(f"Message sent: {message}")
            time.sleep(2)
            
        except Exception as e:
            print(f"Error sending message: {str(e)}")

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    print("Starting YouTube Live Chat Bot...")
    print("Make sure Chrome is CLOSED before running this script!")
    print("Press Enter to continue...")
    input()
    
    bot = YoutubeLiveChatBot()
    
    try:
        # Join chat
        bot.join_live_chat()
        
        while True:
            # Get message from user
            message = input("Enter your message (or 'quit' to exit): ")
            
            if message.lower() == 'quit':
                break
                
            bot.send_message(message)
            time.sleep(2)  # Small delay between messages
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        bot.close()
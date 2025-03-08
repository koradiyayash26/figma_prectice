import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib.parse
import sys

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    return driver

def create_message(student_name, subject, obtained_marks, total_marks, date):
    message = (
        f"પ્રિય વાલીઓ,\n\n"
        f"તમારા બાળક {student_name} ને {date} ના રોજ લેવાયેલી {subject} ટેસ્ટ માં {total_marks} માંથી {obtained_marks} માર્કસ મેળવ્યા છે.\n\n"
        f"આભાર"
    )
    return message

def send_whatsapp_message(driver, phone_number, message):
    try:
        phone_number = str(phone_number).replace("+", "").strip()
        message_encoded = urllib.parse.quote(message)
        url = f'https://web.whatsapp.com/send?phone={phone_number}&text={message_encoded}'
        
        driver.get(url)
        
        wait = WebDriverWait(driver, 30)
        send_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//span[@data-icon="send"]')
        ))
        
        send_button.click()
        time.sleep(2)
        return True
        
    except Exception as e:
        print(f"Error sending to {phone_number}: {str(e)}")
        return False

def process_excel_and_send_messages():
    file_path = 'exam.xlsx'
    driver = None
    
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        # Filter out Summary row and get valid numbers more precisely
        valid_numbers = df[
            (df['Student Name'].notna()) &  # Must have student name
            (df['Student Name'] != 'Summary') &  # Not summary row
            (df['Mobile Number'].notna()) & 
            (df['Mobile Number'] != '-') & 
            (df['Mobile Number'].astype(str).str.len() > 0) &  # Must have valid length
            (df['Obtained Marks'].notna())
        ]
        
        valid_count = len(valid_numbers)
        if valid_count == 0:
            print("No valid entries found. Exiting...")
            return
        
        print(f"Found {valid_count} messages to send.")
        
        # Setup driver and scan QR
        driver = setup_driver()
        driver.get("https://web.whatsapp.com")
        
        # Wait for QR scan (30 seconds timeout)
        wait = WebDriverWait(driver, 30)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="chat-list"]')))
        except:
            pass  # Continue anyway as user might be already logged in
        
        # Process valid numbers
        successful = 0
        for index, row in valid_numbers.iterrows():
            try:
                message = create_message(
                    student_name=row['Student Name'],
                    subject=row['Subject'],
                    obtained_marks=row['Obtained Marks'],
                    total_marks=row['Total Marks'],
                    date=row['Date']
                )
                
                if send_whatsapp_message(driver, row['Mobile Number'], message):
                    successful += 1
                    print(f"✓ Sent to {row['Student Name']}")
                else:
                    print(f"✗ Failed for {row['Student Name']}")
                    break
                
            except Exception as e:
                print(f"Error processing {row['Student Name']}: {str(e)}")
                break
                
        print(f"\nCompleted: {successful}/{valid_count} messages sent")
        
    except Exception as e:
        print(f"Critical error: {str(e)}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    process_excel_and_send_messages()

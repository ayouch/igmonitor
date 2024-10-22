import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # Automatically manages ChromeDriver

import requests

# Telegram configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Your Telegram bot token
CHAT_ID = os.getenv("CHAT_ID")  # Your chat ID
WEBHOOK_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# URL to monitor
PAGE_URL = "https://www.instagram.com/god"  # URL to monitor
SEARCH_WORD = "sorry"  # The word to search for (checking if the page is banned)

# Function to send a Telegram message
def send_telegram_message(message):
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(WEBHOOK_URL, data=data)
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")

# Function to check the webpage using Selenium in headless mode
def check_page():
    try:
        # Set up Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

        # Initialize the Chrome WebDriver
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

        # Open the page
        driver.get(PAGE_URL)

        # Wait for the page to load completely
        time.sleep(5)  # Adjust the wait time if necessary

        # Get the page source (HTML after rendering)
        page_content = driver.page_source.lower()  # Convert to lowercase for case-insensitive search

        # Check if the word 'sorry' is in the page content
        if SEARCH_WORD in page_content:
            send_telegram_message(f"Smoked")
        else:
            print("The word 'Sorry' was not found on the page.")

        # Close the browser
        driver.quit()
    except Exception as e:
        print(f"Error checking the page: {e}")

# Main loop to check the page every 5 minutes
if __name__ == "__main__":
    while True:
        check_page()
        time.sleep(300)  # Sleep for 300 seconds (5 minutes)

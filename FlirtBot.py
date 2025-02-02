import sys, time, os, pickle, re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from dotenv import load_dotenv
from logger import logger
from OpenAiAPI import OpenAiAPI
import hashlib

# TODO: make ai to memorize previous messages
class FlirtBot:
    def __init__(self, driver):
        load_dotenv()
        self.openai_api_key = os.getenv("API_KEY")
        self.driver = driver
        self.exiting = False

    def exit(self):
        self.exiting = True
        self.driver.quit()

    def open_messenger(self):
        self.driver.get("https://www.messenger.com")
        logger.info("Opened Facebook Messenger.")

    def hash_message(self, message):
        return hashlib.sha256(message.encode('utf-8')).hexdigest()

    def login(self):
        if os.path.exists("cookies.pkl"):
            # Load cookies
            with open("cookies.pkl", "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)

            # Refresh the page to apply cookies
            self.driver.refresh()
            logger.info("Logged in using cookies.")
        else:
            # Manual login
            logger.info("Manually log in to Facebook Messenger.")
            input("Log in manually and press Enter here to continue...")

            # Save cookies
            with open("cookies.pkl", "wb") as file:
                pickle.dump(self.driver.get_cookies(), file)
            logger.info("Cookies saved.")      

    def search_user(self, user_name):
        search_box = self.driver.find_element(By.XPATH, '//input[@placeholder="Search Messenger"]')
        search_box.send_keys(user_name)
        time.sleep(5)
        search_box.send_keys(Keys.ENTER)
        time.sleep(5)
        logger.info("Navigated to conversation.")

    def wait_for_message_box(self):
        try:
            message_box = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Message" and @contenteditable="true"]'))
            )
            logger.info("Message box found.")
            return message_box
        except TimeoutException:
            logger.error("Message box not found.")
            sys.exit("Exiting script due to TimeoutException.")

    def wait_for_chat_container(self):
        try:
            chat_container = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "x78zum5 xdt5ytf x1iyjqo2 xs83m0k x1xzczws x6ikm8r x1odjw0f x1n2onr6 xh8yej3 xish69e")]'))
            )
            logger.info("Chat container found.")
            return chat_container
        except TimeoutException:
            logger.error("Chat container not found.")
            sys.exit("Exiting script due to TimeoutException.")

    def message_sanitizer(self, message):
        message = re.sub(r'\s+', ' ', message).strip()
        message = re.sub(r'\{.*?\}', '', message)
        message = re.sub(r'\(.*?\)', '', message)
        message = re.sub(r'\[.*?\]', '', message)
        message = re.sub(r'\<.*?\>', '', message)
        # Remove non-BMP characters
        message = ''.join(c for c in message if c <= '\uFFFF')
        return message

    def check_recent_chats(self):
        # Wait for the chat container to load
        chat_container = self.wait_for_chat_container()
        recent_chats = chat_container.find_elements(By.XPATH, './/div[2]/div/div[@class="x78zum5 xdt5ytf"]')
        logger.info("total recent chats: " + str(len(recent_chats)))
        # Extract the top 5 recently chatted persons
        top_5_chats = recent_chats[:5]

        check_message_interval = 30
        latest_message = ""
        openai = OpenAiAPI(api_key=self.openai_api_key)
        idle = False  # Flag to control idling
        idle_keyword = "idle"  # Keyword to idle the process
        continue_keyword = "continue"  # Keyword to continue processing
        
        for chat in top_5_chats:
            # Check if there is a new message (e.g., unread message indicator)
            try:
                person_name = chat.find_element(By.XPATH, './/div/div/div/div[1]/a/div/div/div/div[2]/div/div/div/span/span')
                logger.info("Checking " + person_name.text)
                # Check for unread message indicator
                chat.find_element(By.XPATH, './/div/div/div/div[1]/a/div[1]/div/div/div[3]/div/div/div/div/span')
                # Navigate to the chat
                chat_element = chat.find_element(By.XPATH, './/div/div/div/div[1]/a/div[1]/div/div')
                chat_element.click()
                logger.info("Navigated to the chat.")
                message_box = self.wait_for_message_box()
                message_container = self.driver.find_element(By.XPATH, '//div[@class="x78zum5 xdt5ytf x1iyjqo2 x6ikm8r x1odjw0f xish69e x16o0dkt" and @role="none"]')
                # Select divs with presentation role
                presentation_divs = message_container.find_elements(By.XPATH, '//div[contains(@class, "html-div xdj266r x11i5rnm xat24cr x1mh8g0r x14ctfv x1okitfd x6ikm8r x10wlt62 xerhiuh x1pn3fxy x12xxe5f x1szedp3 x1n2onr6 x1vjfegm x1k4qllp x1mzt3pk x13faqbe")]')
                logger.info(f"Found presentation div count: {len(presentation_divs)}")
                # Find all messages in the chat
                messages = message_container.find_elements(By.XPATH, '//div[@role="presentation"]//div[@dir="auto" and contains(@class, "x1gslohp")]')
                logger.info(f"Found message count: {len(messages)}")

                if messages:
                    # Get the last message (assuming the last one is the latest)
                    latest_message = self.message_sanitizer(messages[-1].text)
                    logger.info(f"Latest message: <<{latest_message}>>")

                    # Check if the message is sent to you
                    if "x1xr0vuk" in presentation_divs[-1].get_attribute("class"):
                        logger.info("Message is sent to me")
                        # Check for idle and continue keywords
                        if idle_keyword in latest_message.lower():
                            idle = True
                            logger.info("Idling the process.")
                        elif continue_keyword in latest_message.lower():
                            idle = False
                            logger.info("Continuing the process.")

                        # Skip processing if idle flag is set
                        if idle:
                            time.sleep(check_message_interval)
                            continue

                        # Get response from the pretrained model
                        reply_message = self.message_sanitizer(openai.chat(latest_message))
                        # Reply to the new message
                        message_box.send_keys(reply_message)
                        message_box.send_keys(Keys.ENTER)

                        time.sleep(check_message_interval)  # Check for new messages every 30 seconds
                    else:
                        logger.info("Message is sent by me")

                top_5_chats = recent_chats[:5]
            except NoSuchElementException:
                logger.info(f"No unread message found!")
                continue
            except Exception as e:
                logger.error(f"Error: {e.__class__.__name__}: {e}")
                continue
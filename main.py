import signal,web_driver,sys,time,os
from FlirtBot import FlirtBot
from logger import logger

import hashlib

def hash_message(message):
    return hashlib.sha256(message.encode('utf-8')).hexdigest()

def signal_handler(signal, frame, flirt_bot):
    print("gracefully exiting...")
    logger.info("Signal received, exiting...")
    flirt_bot.exit()
    sys.exit(0)


def main():
    # Path to ChromeDriver
    driver_path = r"C:\Users\thure\OneDrive\Desktop\Lab\FlirtBot\chromedriver-win64\chromedriver.exe"
    # Create a FlirtBot instance
    flirt_bot = FlirtBot(web_driver.getDriver(driver_path=driver_path))
    proccess_interval = 30
    
    # Register signal handler
    signal.signal(signal.SIGINT, lambda s, f: signal_handler(s, f, flirt_bot))
    signal.signal(signal.SIGTERM, lambda s, f: signal_handler(s, f, flirt_bot))

    try:
        flirt_bot.open_messenger()
        flirt_bot.login()
        time.sleep(proccess_interval)
        while True:
            flirt_bot.check_recent_chats()
            time.sleep(proccess_interval)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        flirt_bot.exit()
        sys.exit(1)

if __name__ == "__main__":
    main()
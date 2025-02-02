from datetime import datetime
import logging
import os

def setup_logger():
    # Create logs folder if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Get current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Configure logging with UTF-8 encoding and current date in filename
    log_filename = f'logs/flirtlog_{current_date}.log'
    log_handler = logging.FileHandler(log_filename, encoding='utf-8')
    log_handler.setLevel(logging.INFO)
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    log_handler.setFormatter(log_formatter)

    logger = logging.getLogger('flirtbot_logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)
    
    return logger

# Create a logger instance
logger = setup_logger()
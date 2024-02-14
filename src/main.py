import logging

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from src.db import Base, engine
from src.parser import parse_auto_ria_ua

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

LOGGER = logging.getLogger(__name__)


def initialize_driver() -> WebDriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=chrome_options,
    )
    return driver


if __name__ == '__main__':
    LOGGER.info("Started parsing ...")

    # Create missing tables
    LOGGER.info("Creating missing tables ...")
    Base.metadata.create_all(engine)

    # Initialize Selenium WebDriver
    LOGGER.info("Initializing driver ...")
    driver = initialize_driver()

    # Perform Parsing
    parse_auto_ria_ua(driver)

    LOGGER.info("Finished parsing ...")

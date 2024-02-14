from logging import getLogger

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.dal import store_car_info
from src.settings import USED_CARS_PAGE

LOGGER = getLogger(__name__)


def parse_auto_ria_ua(driver: WebDriver) -> None:
    """
        Parse the auto.ria.ua website to extract information about used cars and store it in the database.

        This function navigates through the pages of used car listings, opens each car listing, and extracts relevant
        information such as title, price, odometer reading, seller's username, image URLs, image count, car number,
        VIN (Vehicle Identification Number), and phone number. It then stores this information in the database.

        The function utilizes the Selenium WebDriver to interact with the website.

        Note:
            Ensure that the WebDriver for Chrome is installed and compatible with the system.

        Raises:
            NoSuchElementException: If any element required for parsing is not found on the page.

    """
    LOGGER.info("Opening main page...")
    driver.get(f'{USED_CARS_PAGE}/?page=1')

    last_page_number = get_last_page_number(driver)
    for i in range(1, last_page_number):
        LOGGER.info(f"Parsing page {i}")
        driver.get(f'{USED_CARS_PAGE}/?page={i}')

        cars = driver.find_elements(By.CLASS_NAME, 'ticket-item')

        for index, car in enumerate(cars):
            open_car_card(driver, index)

            title = get_car_title(driver)

            LOGGER.info(f"Parsing car: {title}")

            store_car_info(
                url=driver.current_url,
                title=title,
                price_usd=get_price_usd(driver),
                odometer=get_odo(driver),
                username=get_user_name(driver),
                image_url=get_img_url(driver),
                image_count=get_img_count(driver),
                car_number=get_car_number(driver),
                car_vin=get_car_vin(driver),
                phone_number=get_phone_number(driver),
            )

            driver.back()


def get_phone_number(driver) -> str:
    """
        Retrieve the phone number displayed on the car listing page.

        Args:
            driver: WebDriver object representing the browser session.

        Returns:
            str: The phone number extracted from the page.
    """
    driver.find_element(By.CLASS_NAME, "phone_show_link").click()

    phone_numbers = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "list-phone"))).text
    phone_numbers = ",".join(phone_numbers.split("\n")[1:])
    return phone_numbers


def get_user_name(driver) -> str:
    """
        Retrieve the name of the seller displayed on the car listing page.

        Args:
            driver: WebDriver object representing the browser session.

        Returns:
            str: The name of the seller.
    """
    return driver.find_element(By.CLASS_NAME, "seller_info_name").text


def get_car_title(driver) -> str:
    """
        Retrieve the title of the car listing.

        Args:
            driver: WebDriver object representing the browser session.

        Returns:
            str: The title of the car listing.
    """
    title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "auto-content_title"))
    ).text
    return title


def open_car_card(driver: WebDriver, index: int) -> None:
    """
        Open the detailed view of a car listing from the search results.

        Args:
            driver: WebDriver object representing the browser session.
            index (int): The index of the car listing to open in the search results.
    """
    car = driver.find_elements(By.CLASS_NAME, 'ticket-item')[index]
    car.location_once_scrolled_into_view
    car_card = WebDriverWait(car, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "head-ticket")))
    car_card.click()


def get_car_number(driver: WebDriver) -> str:
    """
        Retrieve the car number (license plate) displayed on the car listing page.

        Args:
            driver: WebDriver object representing the browser session.

        Returns:
            str: The car number if found, otherwise an empty string.
    """
    try:
        car_number = driver.find_element(By.CLASS_NAME, "state-num.ua").text
    except Exception as e:
        car_number = ""
    return car_number


def get_last_page_number(driver: WebDriver) -> int:
    """
        Retrieve the last page number from the pagination control.

        Args:
            driver: WebDriver object representing the browser session.

        Returns:
            int: The last page number as an integer.
    """
    pagination = driver.find_elements(By.CLASS_NAME, "page-link")
    last_page = pagination[-2].text
    return int(last_page.replace(" ", ""))


def get_price_usd(driver: WebDriver) -> int:
    """
        Retrieve the price of the car in USD from the car listing page.

        Args:
            driver: WebDriver object representing the browser session.

        Returns:
            int: The price of the car in USD as an integer.
    """
    price_usd = driver.find_element(By.CLASS_NAME, "price_value").text
    return int("".join(c for c in price_usd if c.isdigit()))


def get_odo(driver: WebDriver) -> int:
    """
        Retrieve the odometer reading of the car from the car listing page.

        Args:
            driver: WebDriver object representing the browser session.

        Returns:
            int: The odometer reading of the car as an integer.
    """
    odo = driver.find_element(By.CLASS_NAME, "base-information.bold").text
    return int(odo.split(" ")[0] + "000")


def get_img_url(driver: WebDriver) -> str:
    """
        Retrieve the URL of the main image of the car from the car listing page.

        Args:
            driver: WebDriver object representing the browser session.

        Returns:
            str: The URL of the main image of the car.
    """
    img_element = driver.find_element(By.CLASS_NAME, "outline")
    return img_element.get_attribute("src")


def get_img_count(driver: WebDriver) -> str:
    """
        Retrieve the count of images of the car from the car listing page.

        Args:
            driver: WebDriver object representing the browser session.

        Returns:
            str: The count of images of the car.
    """
    img_count_element = driver.find_element(By.CLASS_NAME, "count").text
    return img_count_element.split()[2]


def get_car_vin(driver: WebDriver) -> str:
    """
        Retrieve the VIN (Vehicle Identification Number) of the car from the car listing page.

        Args:
            driver: WebDriver object representing the browser session.

        Returns:
            str: The VIN of the car if found, otherwise an empty string.
    """
    try:
        car_vin = driver.find_element(By.CLASS_NAME, "label-vin").text.split()[0]
    except Exception as e:
        car_vin = ""
    return car_vin

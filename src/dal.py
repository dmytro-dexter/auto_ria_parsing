from logging import getLogger

from sqlalchemy.orm import Session

from src.db import engine, UsedCarsInfo

LOGGER = getLogger(__name__)


def store_car_info(**kwargs):
    """
        Store or update car information in the database.

        This function checks if a record with the provided URL already exists in the database. If it does, it updates
        the record with new information provided in the `kwargs`. If the record does not exist, a new record is added
        to the database with the provided information.

        Args:
            **kwargs: Keyword arguments containing the information to be stored or updated. Possible keys include:
                - url (str): The URL of the car listing.
                - title (str): The title of the car listing.
                - price_usd (int): The price of the car in USD.
                - odometer (int): The odometer reading of the car.
                - username (str): The username of the seller.
                - phone_number (str): The phone number of the seller.
                - image_url (str): The URL of the main image of the car.
                - image_count (str): The count of images of the car.
                - car_number (str): The car number (license plate) of the car.
                - car_vin (str): The VIN (Vehicle Identification Number) of the car.

    """
    car_url = kwargs.pop("url")
    if not car_url:
        LOGGER.info("There is no car url. Skipping...")
        return

    with Session(engine) as session, session.begin():
        used_cars_obj = session.query(UsedCarsInfo).filter_by(url=car_url).first()

        if used_cars_obj:
            for field, value in kwargs.items():
                setattr(used_cars_obj, field, value)
        else:
            used_cars_obj = UsedCarsInfo(
                url=car_url,
                title=kwargs.get("title"),
                price_usd=kwargs.get("price_usd"),
                odometer=kwargs.get("odometer"),
                username=kwargs.get("username"),
                image_url=kwargs.get("image_url"),
                image_count=kwargs.get("image_count"),
                car_number=kwargs.get("car_number"),
                car_vin=kwargs.get("car_vin"),
                phone_number=kwargs.get("phone_number"),
            )

        session.add(used_cars_obj)

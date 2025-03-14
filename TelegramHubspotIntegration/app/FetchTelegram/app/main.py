from app.FetchTelegram.app.utils import fetch_user_data_and_messages
from logger import logging


async def fetch_telegram_contacts_details(credentials):
    try:
        contacts_details = await fetch_user_data_and_messages(credentials=credentials)

        return contacts_details
    
    except Exception as e:
        logging.error(e)
        return []


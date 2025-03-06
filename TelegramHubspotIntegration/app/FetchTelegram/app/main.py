# from fastapi import FastAPI
from app.FetchTelegram.app.utils import fetch_user_data_and_messages
from logger import logging


# app = FastAPI()


# @app.get("/contact-details")
async def fetch_telegram_contacts_details(credentials):
    try:
        contacts_details = await fetch_user_data_and_messages(credentials=credentials)

        return contacts_details
    
    except Exception as e:
        logging.error(e)
        return []


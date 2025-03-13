from fastapi import FastAPI, Header, Depends
from app.utils import fetch_user_data_and_messages
from pydantic import BaseModel
from logger import logging
from typing import Annotated


class TelegramCredentials(BaseModel):
    api_id: str
    api_hash: str
    phone_number: str
    telegram_owner_name: str
    session_string: str


app = FastAPI()


@app.get("/contact-details")
async def fetch_telegram_contacts_details(user_credentials: Annotated[TelegramCredentials, Depends(TelegramCredentials), Header()]):
    try:
        contacts_details = await fetch_user_data_and_messages(
                                    session_string=user_credentials.session_string,
                                    api_hash=user_credentials.api_hash,
                                    api_id=user_credentials.api_id,
                                    phone_number=user_credentials.phone_number,
                                    my_name=user_credentials.telegram_owner_name
                                )

        return contacts_details
    
    except Exception as e:
        logging.error(e)


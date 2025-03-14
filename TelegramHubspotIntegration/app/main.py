import json
import asyncio
import requests
from app.FetchTelegram.app.main import fetch_telegram_contacts_details
from app.PushHubspot.app.main import push_messages_to_hubspot_notes
from fastapi import FastAPI, Header, Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated
from logger import logging


class ConnectionCredentials(BaseModel):
    telegram_api_id: str
    telegram_api_hash: str
    telegram_phone_number: str
    session_string: str
    hubspot_api_key: str
    owner_name: str = None
    hubspot_owner_id: str = None
    hubspot_time_zone: str = None


app = FastAPI()

@app.get("/telegram-hubspot/notes")
async def telegram_hubspot_integration(credentials: Annotated[ConnectionCredentials, Depends(ConnectionCredentials), Header()]):
    try:
        telegram_contact_details = await fetch_telegram_contacts_details(credentials=credentials)

        responses = []
        for contact_detail in telegram_contact_details:

            hubspot_integration_input = {
                "full_name": contact_detail["USER DETAILS"]["Name"],
                "phone_number": contact_detail["USER DETAILS"]["Phone Number"],
                "messages": contact_detail["USER MESSAGES"]
            }
            
            try:
                response = push_messages_to_hubspot_notes(credentials=credentials, contact_with_messages=hubspot_integration_input)
            except Exception as e:
                logging.error(e)
                return { "error": str(e) }
            responses.append(response)

        # print(responses)
        return responses
    
    except HTTPException as e:
        logging.error(e)
        return { "error": str(e) }

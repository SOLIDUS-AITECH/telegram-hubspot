from fastapi import FastAPI, Header, Depends
from dotenv import load_dotenv
import hubspot
from app.utils import ContactQuery, match_with_hubspot_contact, put_messages_into_notes, HubspotCredentials
from logger import logging
from typing import Annotated


app = FastAPI()



@app.post("/hubspotapi-notes")
def push_messages_to_hubspot_notes(
    credentials: Annotated[HubspotCredentials, Depends(HubspotCredentials), Header()], 
    contact_with_messages: ContactQuery
):
    hubspot_client = hubspot.Client.create(access_token=credentials.hubspot_api_key)
    try:
        hubspot_contact_id = match_with_hubspot_contact(
                            phone=contact_with_messages.phone_number, 
                            full_name=contact_with_messages.full_name,
                            hubspot_client=hubspot_client
                        )

        if not hubspot_contact_id:
            return {"message": "Contact does not exist on Hubspot. Please check contact details and try again."}

        messages = []
        for message in contact_with_messages.messages:
            messages.append(f"{message['Sender']}: {message['Message']}")
        
        return {"Note ID": put_messages_into_notes(
                                hubspot_contact_id=hubspot_contact_id, 
                                messages=messages, 
                                hubspot_owner_id=credentials.hubspot_owner_id,
                                hubspot_client=hubspot_client,
                                time_zone=credentials.time_zone,
                                my_name=credentials.hubspot_owner_name
                ),
                "Contact": contact_with_messages.full_name,
                "Messages": contact_with_messages.messages}
    
    except Exception as e:
        logging.error(e)
        return {"Error": str(e)}

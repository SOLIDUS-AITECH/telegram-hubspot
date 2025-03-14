# from fastapi import FastAPI
from dotenv import load_dotenv
from app.PushHubspot.app.utils import match_with_hubspot_contact, put_messages_into_notes
import hubspot
from logger import logging



def push_messages_to_hubspot_notes(credentials, contact_with_messages):
    try:
        hubspot_client = hubspot.Client.create(access_token=credentials.hubspot_api_key)
        hubspot_contact_id = match_with_hubspot_contact(
                                phone=contact_with_messages["phone_number"], 
                                full_name=contact_with_messages["full_name"],
                                hubspot_client=hubspot_client
                            )
        # print(f"\nCONTACT ID: {hubspot_contact_id}\n")
        if not hubspot_contact_id:
            return {"message": "Contact does not exist on Hubspot. Please check contact details and try again."}

        messages = []
        for message in contact_with_messages["messages"]:
            messages.append(f"{message['Sender']}: {message['Message']}")
        
        return {
            "Note ID": put_messages_into_notes(
                        hubspot_contact_id=hubspot_contact_id, 
                        messages=messages, 
                        hubspot_client=hubspot_client,
                        hubspot_owner_id=credentials.hubspot_owner_id,
                        hubspot_time_zone=credentials.hubspot_time_zone,
                        hubspot_user_name=credentials.owner_name
                    ),
            "Contact Name": contact_with_messages["full_name"],
            "Phone Number": contact_with_messages["phone_number"]
        }
    
    except Exception as e:
        logging.error(e)
        return { "error": str(e) }


import hubspot
from hubspot.crm.contacts import ApiException
from hubspot.crm.objects.notes import SimplePublicObjectInputForCreate
import re
from datetime import datetime
import pytz
from fuzzywuzzy import fuzz
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from pathlib import Path
from logger import logging


# env_path = Path(__file__).parents[3] / '.env'
# load_dotenv(dotenv_path=env_path)


# hubspot_api_key = os.getenv("hubspot_api_key")
# hubspot_owner_id = os.getenv("hubspot_owner_id")
# hubspot_time_zone = os.getenv("hubspot_time_zone")
# hubspot_user_name = os.getenv("hubspot_user_name")


# hubspot_client = hubspot.Client.create(access_token=hubspot_api_key)


# class ContactQuery(BaseModel):
#     full_name: str
#     phone_number: str
#     messages: list[dict[str, str]] = None


def put_messages_into_notes(
    hubspot_contact_id, 
    messages, 
    hubspot_client, 
    hubspot_owner_id=None, 
    hubspot_time_zone=None, 
    hubspot_user_name=None
):
    try:
        if not hubspot_time_zone:
            hubspot_time_zone = "America/Chicago"

        if not hubspot_user_name:
            hubspot_user_name = "Me"

        # print("PUT:\n")
        time_now = datetime.now(pytz.timezone(hubspot_time_zone)).astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        hs_note_body = f"Conversation with {hubspot_user_name}: <br>" + "<br>".join(messages)

        properties = {
            "hs_timestamp": f"{time_now}",
            "hs_note_body": hs_note_body,
            # "hubspot_owner_id": hubspot_owner_id,
            # "hs_attachment_ids": "24332474034;24332474044"
        }
        if hubspot_owner_id:
            properties["hubspot_owner_id"] = hubspot_owner_id

        associations=[{"to":{"id":f"{hubspot_contact_id}"},
                    "types":[{"associationCategory":"HUBSPOT_DEFINED","associationTypeId":202}]}]
        
        simple_public_object_input_for_create = SimplePublicObjectInputForCreate(associations=associations, properties=properties)
        
        create_note_response = hubspot_client.crm.objects.notes.basic_api.create(simple_public_object_input_for_create=
                                                                                simple_public_object_input_for_create)
        
        # print(f"NOTE ADDED:\n {create_note_response}\n")
        return create_note_response.to_dict()["id"]
    
    except ApiException as e:
        logging.error(e)
        return {"error": str(e)}


def match_with_hubspot_contact(phone, full_name, hubspot_client):
    try:
        # print("MATCH:\n")
        properties = ["firstname", "lastname", "phone"]
        phone = normalize_phone_number(phone)
        contacts = hubspot_client.crm.contacts.basic_api.get_page(limit=None, archived=False, properties=properties)
        contacts = contacts.to_dict()

        # print(contacts.results)
        for contact in contacts["results"]:
            # print(f"CONTACT DETAILS: {contact.properties['phone']}\n{phone}") 
            hubspot_phone = contact["properties"]['phone']
            # print(f"HUSPOT: {hubspot_phone}")
            if hubspot_phone and normalize_phone_number(hubspot_phone) == phone:
                hubspot_firstname = contact["properties"]['firstname'] if contact["properties"]['firstname'] else ""
                hubspot_lastname = contact["properties"]['lastname'] if contact["properties"]['lastname'] else ""
                hubspot_full_name = f"{hubspot_firstname} {hubspot_lastname}"
                # print(hubspot_full_name)
                if fuzz.partial_ratio(hubspot_full_name, full_name) >= 30:
                    # print(f"CONTACT DETAILS: {contact['properties']}\n")
                    # print(f"FUZZY MATCH SCORE: {fuzz.partial_ratio(hubspot_full_name, full_name)}")
                    return contact["id"]
                else:
                    print("Names do not match\n")
                    return None
            
        return None
    
    except ApiException as e:
        logging.error(e)
        return None


def normalize_phone_number(phone):
    """Removes special characters and ensures consistent phone format."""
    if phone:
        phone = re.sub(r'\D', '', phone)  # Remove non-numeric characters
        return phone[-15:]  # Keep last 10 digits
    return None
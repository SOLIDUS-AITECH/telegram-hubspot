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
from logger import logging



class HubspotCredentials(BaseModel):
    hubspot_api_key: str
    hubspot_owner_id: str = None
    time_zone: str = None
    hubspot_owner_name: str = None

class ContactQuery(BaseModel):
    full_name: str
    phone_number: str
    messages: list[dict[str, str]] = None


def put_messages_into_notes(hubspot_contact_id, messages, hubspot_client, hubspot_owner_id=None, time_zone=None, my_name=None):
    try:
        if not time_zone:
            time_zone = "America/Chicago"

        if not my_name:
            my_name = "Me"

        time_now = datetime.now(pytz.timezone(time_zone)).astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        hs_note_body = f"Conversation with {my_name}: <br>" + "<br>".join(messages)

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
        phone = normalize_phone_number(phone)
        print(f"Input Phone: {phone}")

        properties = ["firstname", "lastname", "phone"]

        contacts = hubspot_client.crm.contacts.basic_api.get_page(limit=None, archived=False, properties=properties)
        contacts = contacts.to_dict()

        # print(contacts.results)
        for contact in contacts["results"]:
            # logging.info(f"CONTACT DETAILS: {contact.properties['phone']}\n{phone}") 
            hubspot_phone = contact["properties"]['phone']
            print(f"hub Phone: {normalize_phone_number(hubspot_phone)}")
            if hubspot_phone and normalize_phone_number(hubspot_phone) == phone:
                hubspot_firstname = contact["properties"]['firstname'] if contact["properties"]['firstname'] else ""
                hubspot_lastname = contact["properties"]['lastname'] if contact["properties"]['lastname'] else ""
                hubspot_full_name = f"{hubspot_firstname} {hubspot_lastname}"
                if fuzz.partial_ratio(hubspot_full_name, full_name) >= 30:
                    # logging.info(f"CONTACT DETAILS: {contact['properties']}\n")
                    # logging.info(f"FUZZY MATCH SCORE: {fuzz.partial_ratio(hubspot_full_name, full_name)}")
                    return contact["id"]
                else:
                    logging.info("Names do not match")
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
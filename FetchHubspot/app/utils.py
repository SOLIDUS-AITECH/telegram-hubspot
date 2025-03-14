import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import hubspot
from hubspot.crm.contacts import ApiException
import re
from fuzzywuzzy import fuzz
from logger import logging


class HubspotCredentials(BaseModel):
    hubspot_api_key: str

class QueryContact(BaseModel):
    full_name: str = None
    phone_number: str
    # hubspot_api_key: str


def get_engagements_for_contacts(contact_id, hubspot_api_key):
    try:
        url = "https://api.hubapi.com/engagements/v1/engagements/paged?limit=10"
        headers = {"Authorization": f"Bearer {hubspot_api_key}", "Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        engagements = response.json()

        results = []
        for result in engagements['results']:
            contact_ids = result['associations']['contactIds']

            if int(contact_id) in contact_ids:
                results.append(result)

        return results
    
    except ApiException as e:
        logging.error(e)
        return {"message": str(e)}


def get_contacts(hubspot_api_key, contact_query: QueryContact=None):
    client = hubspot.Client.create(access_token=hubspot_api_key)
    properties = ["firstname", "lastname", "phone", "email", "lifecyclestage", "hs_lead_status", "company"]

    try:
        contacts = client.crm.contacts.basic_api.get_page(limit=None, archived=False, properties=properties)
        contacts = contacts.to_dict()

        if contact_query:
            for contact in contacts["results"]:
            # print(f"CONTACT DETAILS: {contact}\n")
                full_name = f"{contact['properties']['firstname']} {contact['properties']['lastname']}"

                if normalize_phone_number(contact['properties']['phone']) == normalize_phone_number(contact_query.phone_number) \
                and fuzz.partial_ratio(full_name, contact_query.full_name) >= 35:
                    contact_results = {}
                    contact_results["CONTACT DETAILS"] = contact

                    engagement_details = []
                    engagements = get_engagements_for_contacts(contact["id"], hubspot_api_key=hubspot_api_key)
                    for engagement in engagements:
                        # print(f"ENGAGEMENT: Type:{engagement['engagement']['type']}, Company:{engagement['associations']['companyIds']}, Deals:{engagement['associations']['dealIds']}")
                        results = {}
                        results["Type"] = engagement['engagement']['type']
                        results["Company"] = engagement['associations']['companyIds']
                        results["Deals"] = engagement['associations']['dealIds']
                        
                        engagement_details.append(results)

                    contact_results["ENGAGEMENT DETAILS"] = engagement_details
                    return contact_results
            
            return {"message": "Contact not found on Hubspot."}

        else:
            contact_results = []
            for contact in contacts["results"]:
                contact_details = {}
                contact_details["CONTACT DETAILS"] = contact

                engagement_details = []
                engagements = get_engagements_for_contacts(contact["id"], hubspot_api_key=hubspot_api_key)
                for engagement in engagements:
                    # print(f"ENGAGEMENT: Type:{engagement['engagement']['type']}, Company:{engagement['associations']['companyIds']}, Deals:{engagement['associations']['dealIds']}")
                    results = {}
                    results["Type"] = engagement['engagement']['type']
                    results["Company"] = engagement['associations']['companyIds']
                    results["Deals"] = engagement['associations']['dealIds']
                    
                    engagement_details.append(results)

                contact_details["ENGAGEMENT DETAILS"] = engagement_details
                contact_results.append(contact_details)
            
            return contact_results

    except ApiException as e:
        logging.error(e)
        return {"message": str(e)}


def normalize_phone_number(phone):
    """Removes special characters and ensures consistent phone format."""
    if phone:
        phone = re.sub(r'\D', '', phone)  # Remove non-numeric characters
        return phone[-15:]  # Keep last 10 digits
    return None
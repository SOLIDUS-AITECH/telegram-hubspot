from hubspot.crm.contacts import ApiException
from app.utils import QueryContact, get_contacts, HubspotCredentials
from fastapi import FastAPI, Header, Depends
from logger import logging
from typing import Annotated


app = FastAPI()


@app.post("/contacts/details")
def get_single_contact_by_details(credentials: Annotated[HubspotCredentials, Depends(HubspotCredentials), Header()], contact_detail: QueryContact):
    try:
        return get_contacts(hubspot_api_key=credentials.hubspot_api_key, contact_query=contact_detail)    
        
    except ApiException as e:
        logging.error(e)
        return {"message": str(e)}


@app.get("/contacts")
def get_all_contacts(credentials: Annotated[HubspotCredentials, Depends(HubspotCredentials), Header()]):
    try:
        return get_contacts(hubspot_api_key=credentials.hubspot_api_key)

    except ApiException as e:
        logging.error(e)
        return {"message": str(e)}


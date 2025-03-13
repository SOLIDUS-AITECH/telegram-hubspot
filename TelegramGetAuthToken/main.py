from telethon import TelegramClient
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv
import asyncio
import time
from typing import Annotated
from fastapi import FastAPI, Header, Depends, HTTPException
from pydantic import BaseModel
from logger import logging

# load_dotenv()

# api_id = os.getenv("api_id")   
# api_hash = os.getenv("api_hash")
# phone_number = os.getenv("phone_number")  
# my_name = os.getenv("my_name")


CODE_FILE = "app/code.txt"
SESSION_FILE = "app/session_string.txt"

class AuthCode(BaseModel):
    code: str=None


class TelegramCredentials(BaseModel):
    api_id: str
    api_hash: str
    phone_number: str

app = FastAPI()


@app.get("/get-token")
async def connect_and_fetch_auth_token(credentials: Annotated[TelegramCredentials, Depends(TelegramCredentials), Header()]):
    client = TelegramClient(
        StringSession(), 
        api_id=credentials.api_id, 
        api_hash=credentials.api_hash,
    )

    try:
        if client:
            await client.connect()

            if not await client.is_user_authorized():
                await client.send_code_request(credentials.phone_number)

                code = None
                timeout = 60
                start_time = time.time()

                with open(CODE_FILE, "w") as f:
                    pass

                while time.time() - start_time < timeout:
                    try:
                        with open(CODE_FILE, "r") as f:
                            code = f.read().strip()

                        if not code:
                            await asyncio.sleep(5)
                        else:
                            logging.info(f"CODE: {code}")
                            break

                    except FileNotFoundError as e:
                        logging.error(e)
                    
                try:
                    await client.sign_in(credentials.phone_number, code)

                except Exception as e:
                    logging.error("Sign in failed: ", e)
                    return { "message": f"Sign in failed. {str(e)}"}


            if await client.is_user_authorized():
                logging.info("Session is valid")
            else:
                logging.info("Session expired or invalid!")

            session_string = client.session.save()
            try:
                with open(SESSION_FILE, "w") as f:
                    f.write(session_string)
                logging.info("Session string saved successfully.")
            except Exception as e:
                logging.error(f"Could not save session string. Please try again later...")
                logging.error(e)
                return {
                    "message": f"Could not save session string. Please try again later...",
                    "error": {str(e)} 
                }

            await client.disconnect()
            # await client.log_out()

            try:
                with open(SESSION_FILE, "r") as f:
                    session_string = f.read().strip()
            except Exception as e:
                logging.error(f"Could not fetch session string. {str(e)}")
                return {
                    "message": "Could not fetch session string.",
                    "error": str(e)
                }
            
            logging.info(f"AUTH TOKEN: {session_string}")

            return {"Auth Token": session_string}

    except Exception as e:
        logging.error(e)
        return { "message": f"No Auth Token generated. Error: {str(e)}" }


@app.post("/code")
async def store_code(auth_code: AuthCode):
    with open(CODE_FILE, "w") as f:
        f.write(auth_code.code)

    return {"code": auth_code.code}
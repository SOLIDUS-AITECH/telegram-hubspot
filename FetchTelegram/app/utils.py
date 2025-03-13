from telethon import TelegramClient
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv
from logger import logging


# load_dotenv()

# api_id = os.getenv("api_id")   
# api_hash = os.getenv("api_hash")
# phone_number = os.getenv("phone_number")  
# my_name = os.getenv("my_name")
# session_string = os.getenv("session_string")


async def fetch_user_data_and_messages(session_string, api_id, api_hash, phone_number, my_name):
    try:
        # async with TelegramClient(session_name, api_id=api_id, api_hash=api_hash).start(phone=phone_number) as client:
        async with TelegramClient(
            StringSession(session_string), 
            api_id=api_id, 
            api_hash=api_hash
        ) as client:
            # await client.connect()

            if await client.is_user_authorized():
                logging.info("Session is valid")
            else:
                logging.info("Session expired or invalid!")

            await client.start(phone=phone_number)

            dialogs = await client.get_dialogs()
            all_users_details = []

            for dialog in dialogs:
                if dialog.is_user and dialog.entity.contact and not dialog.message.action:

                    name = dialog.name if dialog.name else "No Name available"
                    user_name = dialog.entity.username if dialog.entity.username else "No username"
                    peer_phone_number = f"+{dialog.entity.phone}" if dialog.entity.phone else "Private"
                    chat_id = dialog.id
                    # logging.info(phone_number)

                    users_details = {}
                    user_data = {
                        "Peer ID": dialog.entity.id,
                        "Name": name,
                        "UserName": user_name,
                        "Phone Number": peer_phone_number,
                        "Chat ID": chat_id
                    }
                    users_details['USER DETAILS'] = user_data
                    # logging.info(user_data)

                    messages = []
                    async for message in client.iter_messages(entity=chat_id, limit=None):
                        if message.text:
                            peer = user_data["Name"]
                            if message.out:
                                sender = my_name
                                receiver = peer
                            else:
                                sender = peer
                                receiver = my_name

                            message_details = {
                                "Chat ID": chat_id,
                                "Sender": sender,
                                "Receiver": receiver,
                                "Messages": message.text
                            }
                            messages.append(message_details)
                    
                    users_details["USER MESSAGES"] = messages
                    all_users_details.append(users_details)

            # logging.info(all_users_details)
            logging.info(f"AUTH TOKEN: {client.session.save()}")
            # await client.disconnect()
            return all_users_details
        
    except Exception as e:
        logging.info(e)
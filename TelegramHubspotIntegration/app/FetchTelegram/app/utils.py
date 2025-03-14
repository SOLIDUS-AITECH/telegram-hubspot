from telethon import TelegramClient
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv
from pathlib import Path
from logger import logging



async def fetch_user_data_and_messages(credentials):
    try:
        if not credentials.owner_name:
            credentials.owner_name = "Me"

        async with TelegramClient(StringSession(credentials.session_string), api_id=credentials.telegram_api_id, api_hash=credentials.telegram_api_hash) as client:

            if await client.is_user_authorized():
                logging.info("Session is valid")
            else:
                logging.info("Session expired or invalid!")
                return {"message" : "Get Authenticated Session String using Telegram Auth Token Agent to establish Telegram connection."}

            try:
                await client.start(phone=credentials.telegram_phone_number)
            except Exception as e:
                logging.error("Could not connect with Telegram Client. Exiting...")
                
                return { "message": "Could not connect with Telegram Client. Exiting...",
                        "error": str(e)}

            dialogs = await client.get_dialogs()
            all_users_details = []

            for dialog in dialogs:
                if dialog.is_user and dialog.entity.contact and not dialog.message.action:

                    name = dialog.name if dialog.name else "No Name available"
                    user_name = dialog.entity.username if dialog.entity.username else "No username"
                    peer_phone_number = f"+{dialog.entity.phone}" if dialog.entity.phone else "Private"
                    chat_id = dialog.id
                    # print(phone_number)

                    users_details = {}
                    user_data = {
                        "Peer ID": dialog.entity.id,
                        "Name": name,
                        "UserName": user_name,
                        "Phone Number": peer_phone_number,
                        "Chat ID": chat_id
                    }
                    users_details['USER DETAILS'] = user_data
                    # print(user_data)

                    messages = []
                    async for message in client.iter_messages(entity=chat_id, limit=None):
                        if message.text:
                            peer = user_data["Name"]
                            if message.out:
                                sender = credentials.owner_name
                                receiver = peer
                            else:
                                sender = peer
                                receiver = credentials.owner_name

                            message_details = {
                                "Chat ID": chat_id,
                                "Sender": sender,
                                "Receiver": receiver,
                                "Message": message.text
                            }
                            messages.append(message_details)
                    
                    users_details["USER MESSAGES"] = messages
                    all_users_details.append(users_details)

            # print(all_users_details)
            # print(client.session.save())
            # await client.disconnect()
            return all_users_details
        
    except Exception as e:
        logging.error(e)
        return { "error": str(e) }
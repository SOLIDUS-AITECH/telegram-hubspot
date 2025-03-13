import uvicorn
# import asyncio
# from app.main import fetch_telegram_contacts_details

if __name__=="__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001)
    # asyncio.run(fetch_telegram_contacts_details())
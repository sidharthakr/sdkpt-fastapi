from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

@app.post("/whatsapp")
async def whatsapp_webhook(
    request: Request,
    Body: str = Form(...),
    From: str = Form(...)
):
    print(f"📨 Received from {From}: {Body}")

    # GPT Reply
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": Body}]
        )
        gpt_reply = response.choices[0].message.content.strip()
    except Exception as e:
        gpt_reply = f"Error from GPT: {str(e)}"

    # TwiML XML Response (required by Twilio)
    reply_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{gpt_reply}</Message>
</Response>"""

    return Response(content=reply_xml, media_type="application/xml")

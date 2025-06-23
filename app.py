from flask import Flask, request
import requests

app = Flask(__name__)

CHATBASE_API_KEY = "s1a31qb7zxj729n5bs03maetnftd0w5q"
CHATBOT_ID = "sBI09bpZvhDSPHIoIy08l"

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get('Body', '')
    sender = request.values.get('From', '')

    # Enviar mensaje a Chatbase
    res = requests.post(
        "https://www.chatbase.co/api/v1/chat",
        headers={"Authorization": f"Bearer {CHATBASE_API_KEY}"},
        json={
            "messages": [{"content": incoming_msg, "role": "user"}],
            "chatbot_id": CHATBOT_ID
        }
    )

    reply = res.json().get("messages", [{"content": "Lo siento, no pude entenderte."}])[0]["content"]

    # Respuesta XML para Twilio
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>""", 200, {'Content-Type': 'text/xml'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

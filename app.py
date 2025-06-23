from flask import Flask, request
import requests

app = Flask(__name__)

CHATBASE_API_KEY = "s1a31qb7zxj729n5bs03maetnftd0w5q"
CHATBOT_ID = "sBI09bpZvhDSPHIoIy08l"

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get('Body', '').strip()

    try:
        res = requests.post(
            "https://www.chatbase.co/api/v1/chat",
            headers={"Authorization": f"Bearer s1a31qb7zxj729n5bs03maetnftd0w5q"},
            json={
                "chatbot_id": CHATBOT_ID,
                "messages": [{"role": "user", "content": incoming_msg}],
                "language": "es"
            },
            timeout=10
        )
        res.raise_for_status()
        data = res.json()
        bot_message = data.get("messages")[0]["content"]  # Asumimos que siempre hay mensajes
    except Exception as e:
        print("Error la recepción del mensaje:", e)
        bot_message = "Ha ocurrido un error. Por favor, inténtalo de nuevo."

    response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{bot_message}</Message>
</Response>"""

    return response_xml, 200, {'Content-Type': 'text/xml'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


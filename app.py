import os
import requests
from flask import Flask, request

app = Flask(__name__)

DIFY_API_KEY = os.getenv("DIFY_API_KEY")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
DIFY_CHAT_ENDPOINT = "https://api.dify.ai/v1/chat-messages"
LINE_REPLY_ENDPOINT = "https://api.line.me/v2/bot/message/reply"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if "events" in data and len(data["events"]) > 0 and "message" in data["events"][0]:
        user_message = data["events"][0]["message"]["text"]
        reply_token = data["events"][0]["replyToken"]
        user_id = data["events"][0]["source"]["userId"]

        # Difyに送るリクエストのヘッダー
        dify_headers = {
            "Authorization": f"Bearer {DIFY_API_KEY}",
            "Content-Type": "application/json",
        }

        # Difyに送るリクエストのボディ（inputsで囲むのが超重要！）
        payload = {
            "inputs": {
                "query": user_message
            },
            "user": user_id
        }

        dify_response = print(payload)
　　　　　　　　requests.post(DIFY_CHAT_ENDPOINT, headers=dify_headers, json=payload)

        # Difyのレスポンスを処理
        if dify_response.status_code == 200:
            dify_reply_text = dify_response.json().get("answer", "すみません、うまく返答できませんでした。")
        else:
            dify_reply_text = f"Difyエラーが発生しました: {dify_response.text}"

        # LINEに返す
        line_headers = {
            "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }
        body = {
            "replyToken": reply_token,
            "messages": [{
                "type": "text",
                "text": dify_reply_text
            }]
        }
        requests.post(LINE_REPLY_ENDPOINT, headers=line_headers, json=body)

    return "OK"

if __name__ == "__main__":
    app.run(port=10000)


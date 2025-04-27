from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 必要な環境変数（Renderなら環境に登録してもOK）
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_REPLY_ENDPOINT = "https://api.line.me/v2/bot/message/reply"
DIFY_API_KEY = "app-ZYzTMtuYuPgJW1soMU4ymbtN"  

DIFY_CHAT_ENDPOINT = "https://api.dify.ai/v1/chat-messages"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if "events" in data and len(data["events"]) > 0 and "message" in data["events"][0]:
        user_message = data["events"][0]["message"]["text"]
        reply_token = data["events"][0]["replyToken"]

        # ① Difyにメッセージ送信
        headers = {
            "Authorization": f"Bearer {DIFY_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
    "query": user_message
}

        }
        dify_response = requests.post(DIFY_CHAT_ENDPOINT, headers=headers, json=payload)

        # ② Difyの返答を取得
        if dify_response.status_code == 200:
            dify_reply_text = dify_response.json().get("answer", "すみません、うまく返事できませんでした。")
        else:
    dify_reply_text = f"Difyエラーが発生しました: {dify_response.text}"


        # ③ LINEに返信
        headers = {
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
        requests.post(LINE_REPLY_ENDPOINT, headers=headers, json=body)

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
    LINE_CHANNEL_ACCESS_TOKEN 


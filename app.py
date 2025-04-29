from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 環境変数やハードコードでもOK（セキュリティには注意）
DIFY_API_KEY = os.environ.get("DIFY_API_KEY", "あなたのDifyのAPIキー")
DIFY_CHAT_ENDPOINT = os.environ.get("DIFY_CHAT_ENDPOINT", "https://api.dify.ai/v1/chat-messages")  # 必ずエンドポイント確認
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "あなたのLINEチャネルアクセストークン")
LINE_REPLY_ENDPOINT = "https://api.line.me/v2/bot/message/reply"


@app.route("/webhook", methods=["POST"])
def webhook():
    # LINEからのデータを受け取る
    data = request.json
    print(f"📩 LINE受信: {data}")

    reply_token = data["events"][0]["replyToken"]
    user_message = data["events"][0]["message"]["text"]
    user_id = data["events"][0]["source"]["userId"]

    # Difyに送るデータ構造
    payload = {
        "inputs": {
            "query": user_message
        },
        "user": user_id
    }

    dify_headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }

    print(f"📤 Dify送信: {payload}")

    dify_response = requests.post(DIFY_CHAT_ENDPOINT, headers=dify_headers, json=payload)
    print(f"📥 Dify返答: {dify_response.status_code} | 内容: {dify_response.text}")

    # レスポンスが正常なら回答を抽出、エラーならその旨返す
    if dify_response.status_code == 200:
        answer = dify_response.json().get("answer", "すみません、うまく答えられませんでした。")
    else:
        answer = f"Difyエラーが発生しました: {dify_response.text}"

    # LINEに返答する
    line_headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {
        "replyToken": reply_token,
        "messages": [{
            "type": "text",
            "text": answer
        }]
    }

    requests.post(LINE_REPLY_ENDPOINT, headers=line_headers, json=body)

    return "OK"


if __name__ == "__main__":
    app.run(port=10000)

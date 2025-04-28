@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if "events" in data and len(data["events"]) > 0 and "message" in data["events"][0]:
        user_message = data["events"][0]["message"]["text"]
        reply_token = data["events"][0]["replyToken"]
        user_id = data["events"][0]["source"]["userId"]  # ⭐️ここ！

        # ① Difyへメッセージ送信
        dify_headers = {
            "Authorization": f"Bearer {DIFY_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "inputs": {
                "query": user_message
            },
            "user": user_id  # ⭐️ここ！
        }

        dify_response = requests.post(DIFY_CHAT_ENDPOINT, headers=dify_headers, json=payload)

        # ② Difyの返答を取得
        if dify_response.status_code == 200:
            dify_reply_text = dify_response.json().get("answer", "すみません、うまく返答できませんでした。")
        else:
            dify_reply_text = f"Difyエラーが発生しました: {dify_response.text}"

        # ③ LINEに返信
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


from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    
    if "events" in data and len(data["events"]) > 0 and "message" in data["events"][0] and "text" in data["events"][0]["message"]:
        user_message = data["events"][0]["message"]["text"]
        
        # （以下、あなたが書いてたOpenAIへのリクエスト処理！）
        prompt = f"""あなたはプロの英語トレーナーです。
        この日本語を2パターンの英語に翻訳してください。
        1. 日常英会話バージョン
        2. ビジネス英語版
        日本語: {user_message}
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        reply_text = response["choices"][0]["message"]["content"]

        return jsonify({"reply": reply_text})
    else:
        return "ok"
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


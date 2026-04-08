import json
import os
import hashlib
import time

from flask import Flask, request, jsonify
import requests

# ====== 配置 ======
# 从飞书开放平台获取，填入你的 App ID 和 App Secret
APP_ID = os.environ.get("FEISHU_APP_ID", "cli_a95f790f44795bc3")
APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "IUtOH2gzsfmz9xaqwdXfOflC5727Su8b")

BASE_URL = "https://open.feishu.cn/open-apis"

# ====== 加载问答表 ======
QA_PATH = os.path.join(os.path.dirname(__file__), "qa.json")
with open(QA_PATH, "r", encoding="utf-8") as f:
    QA_LIST = json.load(f)

DEFAULT_REPLY = "暂无相关信息，请联系管理员。"

# ====== 去重：防止重复处理同一条消息 ======
SEEN_MESSAGES = set()

app = Flask(__name__)


def get_tenant_access_token():
    """获取飞书 tenant_access_token"""
    resp = requests.post(f"{BASE_URL}/auth/v3/tenant_access_token/internal", json={
        "app_id": APP_ID,
        "app_secret": APP_SECRET,
    })
    return resp.json().get("tenant_access_token")


def send_reply(chat_id, text):
    """发送文本消息到群"""
    token = get_tenant_access_token()
    requests.post(
        f"{BASE_URL}/im/v1/messages",
        params={"receive_id_type": "chat_id"},
        headers={"Authorization": f"Bearer {token}"},
        json={
            "receive_id": chat_id,
            "msg_type": "text",
            "content": json.dumps({"text": text}),
        },
    )


def match_qa(question):
    """匹配问答表，返回最佳答案"""
    question = question.lower()
    best_match = None
    best_count = 0

    for qa in QA_LIST:
        count = sum(1 for kw in qa["keywords"] if kw.lower() in question)
        if count > best_count:
            best_count = count
            best_match = qa["answer"]

    return best_match


def extract_text(content):
    """从飞书消息内容中提取纯文本（去掉 @mention）"""
    try:
        content_obj = json.loads(content)
        return content_obj.get("text", "").strip()
    except (json.JSONDecodeError, AttributeError):
        return ""


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    # 飞书 URL 验证（首次配置回调地址时）
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    # 处理事件
    header = data.get("header", {})
    event = data.get("event", {})

    # 只处理消息事件
    if header.get("event_type") != "im.message.receive_v1":
        return jsonify({"code": 0})

    message = event.get("message", {})
    msg_id = message.get("message_id", "")

    # 去重
    if msg_id in SEEN_MESSAGES:
        return jsonify({"code": 0})
    SEEN_MESSAGES.add(msg_id)
    # 限制集合大小
    if len(SEEN_MESSAGES) > 1000:
        SEEN_MESSAGES.clear()

    # 只处理群聊中 @机器人 的文本消息
    chat_type = message.get("chat_type", "")
    msg_type = message.get("message_type", "")
    mentions = message.get("mentions", [])

    if chat_type != "group" or msg_type != "text":
        return jsonify({"code": 0})

    if not mentions:
        return jsonify({"code": 0})

    # 提取问题文本
    question = extract_text(message.get("content", ""))
    # 去掉 @xxx 标记
    for mention in mentions:
        at_key = mention.get("key", "")
        question = question.replace(at_key, "").strip()

    if not question:
        send_reply(message["chat_id"], "请输入你的问题，例如：@机器人 支付流程")
        return jsonify({"code": 0})

    # 匹配问答
    answer = match_qa(question)
    send_reply(message["chat_id"], answer or DEFAULT_REPLY)

    return jsonify({"code": 0})


if __name__ == "__main__":
    print(f"已加载 {len(QA_LIST)} 条问答")
    print("飞书机器人启动，监听端口 9000...")
    port = int(os.environ.get("PORT", 9001))
    app.run(host="0.0.0.0", port=port)

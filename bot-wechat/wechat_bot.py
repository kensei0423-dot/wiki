import json
import os
import hashlib
import time
import base64
import struct
import xml.etree.ElementTree as ET

from flask import Flask, request, make_response
import requests
from Crypto.Cipher import AES

# ====== 配置 ======
CORP_ID = os.environ.get("WECHAT_CORP_ID", "ww69cc47dd4dda0fd2")
AGENT_ID = os.environ.get("WECHAT_AGENT_ID", "1000002")
SECRET = os.environ.get("WECHAT_SECRET", "rzMDhXFJ33u1jyWqV5VEmsOgyVbDYgwCajyzOj356po")
TOKEN = os.environ.get("WECHAT_TOKEN", "umdBc7cmOI6F")
ENCODING_AES_KEY = os.environ.get("WECHAT_ENCODING_AES_KEY", "X8uPufbdGb1xlVIP0F3bLwYJeFSGRiglQCdLB6BuXKE")

BASE_URL = "https://qyapi.weixin.qq.com/cgi-bin"

# ====== 加载问答表（复用飞书版 qa/ 目录）======
def load_qa():
    qa_dir = os.path.join(os.path.dirname(__file__), "qa")
    qa_list = []
    for filename in sorted(os.listdir(qa_dir)):
        if filename.endswith(".json"):
            with open(os.path.join(qa_dir, filename), "r", encoding="utf-8") as f:
                qa_list.extend(json.load(f))
    return qa_list

QA_LIST = load_qa()
DEFAULT_REPLY = "暂无相关信息，请联系管理员。"

# ====== 去重 ======
SEEN_MESSAGES = set()

# ====== access_token 缓存 ======
_token_cache = {"token": None, "expires": 0}

app = Flask(__name__)


# ====== 企业微信消息加解密 ======
class WXBizMsgCrypt:
    def __init__(self, token, encoding_aes_key, corp_id):
        self.token = token
        self.corp_id = corp_id
        self.aes_key = base64.b64decode(encoding_aes_key + "=")

    def _sign(self, timestamp, nonce, encrypt):
        items = sorted([self.token, timestamp, nonce, encrypt])
        return hashlib.sha1("".join(items).encode("utf-8")).hexdigest()

    def verify_url(self, msg_signature, timestamp, nonce, echostr):
        signature = self._sign(timestamp, nonce, echostr)
        if signature != msg_signature:
            return None
        return self._decrypt(echostr)

    def decrypt_msg(self, post_data, msg_signature, timestamp, nonce):
        root = ET.fromstring(post_data)
        encrypt = root.find("Encrypt").text
        signature = self._sign(timestamp, nonce, encrypt)
        if signature != msg_signature:
            return None
        return self._decrypt(encrypt)

    def _decrypt(self, text):
        cipher = AES.new(self.aes_key, AES.MODE_CBC, self.aes_key[:16])
        plain = cipher.decrypt(base64.b64decode(text))
        # 去除 PKCS7 padding
        pad_len = plain[-1]
        content = plain[:-pad_len]
        # 跳过 16 字节随机串 + 4 字节消息长度
        msg_len = struct.unpack(">I", content[16:20])[0]
        msg = content[20:20 + msg_len].decode("utf-8")
        return msg


crypt = WXBizMsgCrypt(TOKEN, ENCODING_AES_KEY, CORP_ID)


# ====== 获取 access_token ======
def get_access_token():
    now = time.time()
    if _token_cache["token"] and now < _token_cache["expires"]:
        return _token_cache["token"]

    resp = requests.get(f"{BASE_URL}/gettoken", params={
        "corpid": CORP_ID,
        "corpsecret": SECRET,
    }).json()

    _token_cache["token"] = resp.get("access_token")
    _token_cache["expires"] = now + resp.get("expires_in", 7200) - 300
    return _token_cache["token"]


# ====== 发送消息 ======
def send_reply(chat_id, text):
    token = get_access_token()
    requests.post(
        f"{BASE_URL}/message/send",
        params={"access_token": token},
        json={
            "chatid": chat_id,
            "msgtype": "text",
            "text": {"content": text},
        },
    )


def send_reply_to_user(user_id, text):
    """回复用户"""
    token = get_access_token()
    print(f"[DEBUG] access_token: {token[:10]}... user: {user_id}")
    resp = requests.post(
        f"{BASE_URL}/message/send",
        params={"access_token": token},
        json={
            "touser": user_id,
            "msgtype": "text",
            "agentid": int(AGENT_ID),
            "text": {"content": text},
        },
    )
    print(f"[DEBUG] send result: {resp.json()}")


# ====== 匹配问答 ======
def match_qa(question):
    question = question.lower()
    best_match = None
    best_count = 0
    for qa in QA_LIST:
        count = sum(1 for kw in qa["keywords"] if kw.lower() in question)
        if count > best_count:
            best_count = count
            best_match = qa["answer"]
    return best_match


# ====== Webhook ======
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    msg_signature = request.args.get("msg_signature", "")
    timestamp = request.args.get("timestamp", "")
    nonce = request.args.get("nonce", "")

    # GET: URL 验证
    if request.method == "GET":
        echostr = request.args.get("echostr", "")
        result = crypt.verify_url(msg_signature, timestamp, nonce, echostr)
        if result:
            return make_response(result)
        return "verification failed", 403

    # POST: 接收消息
    raw_data = request.data.decode("utf-8")
    xml_msg = crypt.decrypt_msg(raw_data, msg_signature, timestamp, nonce)
    if not xml_msg:
        return "decrypt failed", 400

    root = ET.fromstring(xml_msg)
    msg_type = root.find("MsgType").text
    msg_id = root.find("MsgId").text if root.find("MsgId") is not None else ""

    # 去重
    if msg_id in SEEN_MESSAGES:
        return "ok"
    SEEN_MESSAGES.add(msg_id)
    if len(SEEN_MESSAGES) > 1000:
        SEEN_MESSAGES.clear()

    # 只处理文本消息
    if msg_type != "text":
        return "ok"

    content = root.find("Content").text or ""
    from_user = root.find("FromUserName").text or ""

    # 匹配问答
    answer = match_qa(content)
    reply = answer or DEFAULT_REPLY

    # 企业微信应用消息回复给用户
    send_reply_to_user(from_user, reply)

    return "ok"


if __name__ == "__main__":
    print(f"已加载 {len(QA_LIST)} 条问答")
    print("企业微信机器人启动...")
    port = int(os.environ.get("PORT", 9002))
    app.run(host="0.0.0.0", port=port)

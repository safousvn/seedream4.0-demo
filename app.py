{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww28900\viewh18080\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import requests\
import time\
import random\
import hashlib\
\
\
# --------------------------\
# Utility: generate sign\
# --------------------------\
def gen_sign(nonce, security_key, timestamp):\
    keys = [str(nonce), str(security_key), str(timestamp)]\
    keys.sort()\
    key_str = ''.join(keys).encode('utf-8')\
    signature = hashlib.sha1(key_str).hexdigest()\
    return signature.lower()\
\
\
# --------------------------\
# API call function\
# --------------------------\
def submit_task(api_key, security_key, image_url, audio_url):\
    req_url = "https://cv-api.byteintlapi.com/api/common/v2/submit_task"\
    timestamp = int(time.time())\
    nonce = random.randint(0, (1 << 31) - 1)\
\
    req_params = \{\
        "api_key": api_key,\
        "timestamp": str(timestamp),\
        "nonce": str(nonce),\
        "sign": gen_sign(nonce, security_key, timestamp),\
    \}\
\
    req_headers = \{"Content-Type": "application/json"\}\
\
    req_body = \{\
        "req_key": "realman_avatar_picture_omni_cv",\
        "image_url": image_url,\
        "audio_url": audio_url,\
    \}\
\
    resp = requests.post(req_url, params=req_params, headers=req_headers, json=req_body)\
    resp.raise_for_status()\
    return resp.json()\
\
\
# --------------------------\
# Streamlit UI\
# --------------------------\
st.set_page_config(page_title="ByteDance API Demo", layout="centered")\
st.title("\uc0\u9889  ByteDance Avatar + Audio API Demo")\
\
st.write("Enter your API credentials and media links below:")\
\
api_key = st.text_input("API Key (ak)", type="password")\
security_key = st.text_input("Security Key (sk)", type="password")\
image_url = st.text_input("Image URL", value="https://xxxxx.jpg")\
audio_url = st.text_input("Audio URL", value="https://xxxxx.mp3")\
\
if st.button("Submit Task"):\
    if not api_key or not security_key:\
        st.error("Please provide both API Key and Security Key.")\
    else:\
        with st.spinner("Submitting task to API..."):\
            try:\
                result = submit_task(api_key, security_key, image_url, audio_url)\
                st.success("\uc0\u9989  API call successful!")\
                st.subheader("API Response")\
                st.json(result)\
            except Exception as e:\
                st.error(f"API call failed: \{e\}")\
}
import streamlit as st
import datetime
import requests # 通信用ライブラリ
import json
import uuid # ユーザー識別用

GAS_URL = "https://script.google.com/macros/s/AKfycbxoJpPCoQ3xAE2gYYB5jUz6yY94rqJHsAjE0L_O6-E0kRZLNqP7nwSY-0eZ9_fnyKkJ/exec"

# --- 設定 ---
st.set_page_config(page_title="対話システム3", page_icon="T", layout="wide")

# 質問リスト
STRUCTURED_QUESTIONS = [
    "こんにちは。あなたが辛いと思っていることや悩みを私に教えてください。",
    "そのとき、どんな気分になりましたか？",
    "その気分の強さは０から１００で表すとどれくらいですか？",
    "その出来事に直面した際、どのような考えが頭にぱっと浮かびましたか？",
    "その考えが正しいとしたら、それを裏付ける根拠や事実はどのようなことが考えられますか？",
    "ありがとうございます。では逆に、その考えが１００％正しいわけではないとしたら、どのような考えを弱める出来事や理由が考えられますか？",
    "ありがとうございます。これまでの会話を踏まえて、最もバランスの取れた現実的な考え方はどのようなものだと考えられますか？",
    "なるほど、ありがとうございます。今はどのような気分ですか？その気分の強さも０から１００で教えてください。",
    "これで対話は終了です。お疲れさまでした。"
]

# --- メイン処理 ---
st.title("対話システム3")
st.caption("質問を行います。")

# セッション初期化
if "messages" not in st.session_state:
    st.session_state.messages = []
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "first_turn" not in st.session_state:
    st.session_state.first_turn = True
# ユーザーごとに適当なIDを割り振る
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]

# サイドバー
with st.sidebar:
    st.header("設定")
    if st.button("リセット / 最初から"):
        st.session_state.messages = []
        st.session_state.question_index = 0
        st.session_state.first_turn = True
        st.session_state.user_id = str(uuid.uuid4())[:8] # IDも更新
        st.rerun()

    st.markdown("---")

    # 自動送信ボタン
    if len(st.session_state.messages) > 1: # 会話が少しでもあれば表示
        if st.button("実験データを送信して終了"):
            with st.spinner("データを送信しています..."):
                try:
                    # 送信するデータを作成
                    payload = {
                        "user_id": st.session_state.user_id,
                        "logs": st.session_state.messages
                    }
                    # GASに送信
                    response = requests.post(GAS_URL, json=payload)
                    
                    if response.status_code == 200:
                        st.success("送信が完了しました！ご協力ありがとうございました。ブラウザを閉じて終了してください。")
                    else:
                        st.error("送信に失敗しました。もう一度押してみてください。")
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")

# 自動開始処理
if st.session_state.first_turn:
    st.session_state.first_turn = False
    initial_msg = STRUCTURED_QUESTIONS[0]
    st.session_state.messages.append({"role": "assistant", "content": initial_msg})
    st.rerun()

# 履歴表示
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 入力処理
if user_input := st.chat_input("..."):
    # ユーザー
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # システム
    with st.chat_message("assistant"):
        if st.session_state.question_index < len(STRUCTURED_QUESTIONS) - 1:
            st.session_state.question_index += 1
        
        idx = st.session_state.question_index
        final_response = STRUCTURED_QUESTIONS[idx]
        
        st.write(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})




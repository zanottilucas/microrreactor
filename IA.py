import streamlit as st
import google.genai as genai
from io import BytesIO
import base64

API_KEY = "AIzaSyC1aVfI7VjchZkrGco4PFricye80i29WmQ"
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="Chat com Gemini – imagens", page_icon="💬")
st.title("💬 Chat com Gemini 2.5 – com imagens 📎")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("image"):
            st.image(msg["image"], caption="📷 Imagem enviada", use_container_width=True)
        st.markdown(msg["content"])

user_input = st.chat_input(
    placeholder="Digite algo ou envie uma imagem...",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"]
)

if user_input:
    text = getattr(user_input, "text", "")
    files = getattr(user_input, "files", [])

    with st.chat_message("user"):
        if text:
            st.markdown(text)
        for f in files:
            st.image(f, caption=f.name, use_container_width=True)

    msg_dict = {"role": "user", "content": text}
    if files:
        msg_dict["image"] = files[0]
    st.session_state.messages.append(msg_dict)

    contexto = "\n".join(f"{m['role']}: {m['content']}" for m in st.session_state.messages if m["content"])

    with st.chat_message("assistant"):
        with st.spinner("💭 Gemini está processando..."):
            try:
                # Monta estrutura contents conforme documentação
                contents = [contexto]

                if files:
                    f0 = files[0]
                    image_bytes = f0.read()
                    # converte para base64
                    b64 = base64.b64encode(image_bytes).decode("utf‑8")
                    # adiciona como dict com inlineData
                    contents.append({
                        "inlineData": {
                            "mimeType": f0.type,
                            "data": b64
                        }
                    })

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents,
                )
                resposta = response.text.strip()
            except Exception as e:
                resposta = f"⚠️ Erro: {e}"

        st.markdown(resposta)
        st.session_state.messages.append({"role": "assistant", "content": resposta})

import streamlit as st
import google.generativeai as genai

# Sayfa Başlığı ve İkonu
st.set_page_config(page_title="Benim AI Asistanım", page_icon="🤖")

st.title("🤖 Yapay Zeka Asistanım")
st.write("Aşağıya sorunu yaz, cevaplasın!")

# 1. ADIM: API Anahtarını Alıyoruz
# (Güvenlik için şifre gibi gizli giriş yaptık)
api_key = st.text_input("Google AI Studio'dan aldığın API Key'i buraya yapıştır:", type="password")

if api_key:
    # 2. ADIM: Yapay Zekayı Hazırlıyoruz
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # Sohbet geçmişini tutmak için bir hafıza oluşturuyoruz
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Eski mesajları ekrana yazdır
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 3. ADIM: Kullanıcıdan Soru Alıyoruz
        if prompt := st.chat_input("Bir şeyler sor..."):
            # Kullanıcının sorusunu ekrana yaz
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Yapay zekadan cevap al
            with st.spinner("Düşünüyorum..."):
                response = model.generate_content(prompt)
                ai_response = response.text
                
                # Cevabı ekrana yaz
                with st.chat_message("assistant"):
                    st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})

    except Exception as e:
        st.error(f"Bir hata oluştu. API Key doğru mu? Hata detayı: {e}")

else:
    st.info("Devam etmek için lütfen API Key giriniz.")
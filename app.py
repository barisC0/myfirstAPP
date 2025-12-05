import streamlit as st
import google.generativeai as genai

# --- Sayfa Ayarları ---
st.set_page_config(
    page_title="AI Şehir Rehberi",
    page_icon="🏙️",
    layout="centered"
)

# --- Modern Tasarım İçin CSS (Görsel Düzenleme) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #2dd4bf, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-text {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .suggestion-btn {
        display: inline-block;
        margin: 5px;
        padding: 8px 16px;
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 20px;
        color: #94a3b8;
        font-size: 0.8rem;
        text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- Ana Başlık ---
st.markdown('<div class="main-header">AI Şehir Rehberi</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">"Sessiz bir kahveci", "Jazz müzik" veya "Deniz kenarı".<br>Sen modunu söyle, biz mekanı bulalım.</div>', unsafe_allow_html=True)

# --- Sidebar (API Anahtarı Girişi) ---
with st.sidebar:
    st.header("⚙️ Ayarlar")
    api_key = st.text_input("Google API Key", type="password", help="Google AI Studio'dan aldığın anahtar")
    if not api_key:
        st.warning("Lütfen başlamak için API anahtarını gir.")
        st.stop()

# --- Yapay Zeka Kurulumu ---
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"API Anahtarı hatası: {e}")

# --- Kullanıcı Girişleri ---
col1, col2 = st.columns([1, 2])
with col1:
    sehir = st.text_input("Hangi Şehirdesin?", placeholder="Örn: İstanbul, Kadıköy")
with col2:
    mod = st.text_input("Bugün Modun Ne?", placeholder="Örn: Ders çalışabileceğim sessiz bir yer")

# --- Hızlı Öneriler (Butonlar) ---
st.write("Veya şunlardan birini seç:")
cols = st.columns(4)
if cols[0].button("☕ Sessiz Çalışma"):
    mod = "Sessiz, wifi olan, ders çalışmaya uygun kahveci"
if cols[1].button("🍔 Uygun Fiyat"):
    mod = "Öğrenci dostu, uygun fiyatlı, lezzetli yemek"
if cols[2].button("b Romantik"):
    mod = "Şık, manzaralı, romantik akşam yemeği"
if cols[3].button("🌳 Açık Hava"):
    mod = "Park, bahçe, doğa ile iç içe"

# --- Arama Butonu ve Sonuçlar ---
if st.button("🔍 Mekan Bul", type="primary", use_container_width=True):
    if not sehir or not mod:
        st.warning("Lütfen hem şehir hem de mod bilgisini gir.")
    else:
        with st.spinner(f"{sehir} şehrinde senin için harika yerler aranıyor..."):
            try:
                # Yapay Zekaya Giden Emir (Prompt)
                prompt = f"""
                Sen yerel bir şehir rehberisin.
                Şehir: {sehir}
                Kullanıcı İsteği/Modu: {mod}

                Lütfen bu şehirde bu moda en uygun 3 mekanı öner.
                Her mekan için şu formatı kullan:
                
                ### 1. Mekan Adı
                **Neden Burası:** (Kısa ve samimi bir açıklama)
                **Fiyat Aralığı:** (₺, ₺₺, ₺₺₺)
                **Adres Tarifi:** (Kısaca nerede olduğu)
                
                Cevabı samimi ve yardımsever bir dille yaz.
                """
                
                response = model.generate_content(prompt)
                
                # Sonuçları Göster
                st.markdown("---")
                st.success("İşte senin için seçtiklerim!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")

# --- Alt Bilgi ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748b; font-size: 0.8rem;'>Google Gemini ile güçlendirilmiştir</div>", unsafe_allow_html=True)

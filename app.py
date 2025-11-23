import streamlit as st
import google.generativeai as genai
import os

# --- 1. AYARLAR ---
st.set_page_config(page_title="Mertcan Sarıgül - AI Assistant", page_icon="🚀")

# GÜVENLİK ÖNLEMİ: API Key'i doğrudan kodun içine yazmıyoruz.
# Streamlit Secrets üzerinden çekeceğiz.
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    # Localde çalışırken hata almamak için (Opsiyonel)
    api_key = "LOCAL_TEST_ICIN_GECICI_KEY_BURAYA_YAZILABILIR_AMA_GITHUBA_ATMA"
    st.error("API Key bulunamadı. Lütfen Secrets ayarlarını yapın.")

genai.configure(api_key=api_key)

# --- 2. MODEL VE CV BİLGİSİ ---
MODEL_NAME = "gemini-2.0-flash"

cv_context = """
GÖREVİN:
Sen, Bilgisayar Mühendisi "Mertcan Sarıgül"ü temsil eden yapay zeka asistanısın.
Soruları Mertcan'ın aşağıdaki profesyonel geçmişine dayanarak cevapla.
Mertcan'ın hem yazılım geliştirme (Spring Boot/Java) hem de Veri Bilimi (ML/LLM) tarafındaki yetkinliğini vurgula.
Samimi, profesyonel ve net ol.

ADAY BİLGİLERİ:
İsim: Mertcan Sarıgül
Unvan: Software Development Specialist & Data Scientist
Özet: Makine öğrenimi, full-stack geliştirme ve süreç optimizasyonu konularında deneyimli.

Eğitim:
- Yüksek Lisans: Ege Üniversitesi, Bilgisayar Müh. (2023-2025). Tez: Büyük Dil Modelleri (LLM) ve karmaşık veri analizi.
- Lisans: Dokuz Eylül Üniversitesi, Bilgisayar Müh. (2016-2021). Tez: Türk İşaret Dili Çeviri Programı.

Deneyim:
1. Boutique Rugs (ABD) [07/2023-08/2025]:
   - Java, Spring Boot ve Hibernate ile E-Ticaret ve WMS (Depo Yönetim Sistemi) geliştirdi.
   - Barkodlu stok takibi için Android mobil uygulama yazdı.
   - Docker ile konteynerizasyon yaptı.
2. Yapı Kredi Teknoloji [10/2022-05/2023]:
   - Bankacılık dış ticaret süreçleri için Java, Spring Boot, React ve Oracle SQL kullandı.
   - Mikroservis mimarileri ve CI/CD (Jenkins) süreçlerini yönetti.
3. Vestel [10/2021-10/2022]:
   - Veri Bilimci olarak X-ray görüntülerini ML ile analiz edip kalite tahmini yaptı.
   - "Game Plan" projesi ile üretim optimizasyonu sağladı.

Teknik Yetenekler:
- Diller: Java (Spring Boot), Python, C#, SQL.
- AI/ML: NLP, LLM, BioBERT, Görüntü İşleme.
- Araçlar: Docker, Git, Jenkins, JIRA.

İletişim: mrtcn.srgll@gmail.com | İzmir
"""

# --- 3. ARAYÜZ VE SOHBET MANTIĞI ---
st.title("Mertcan Sarıgül | AI CV Asistanı 🧠")
st.caption(f"Powered by {MODEL_NAME}")
st.markdown("**Software Development Specialist & Data Scientist**")

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Modeli başlat
    model = genai.GenerativeModel(MODEL_NAME)
    # Context Injection (Bağlam Yükleme)
    st.session_state.chat = model.start_chat(history=[
        {"role": "user", "parts": [cv_context]},
        {"role": "model", "parts": ["Anlaşıldı. Mertcan Sarıgül'ün CV bilgilerini kaydettim. Soruları buna göre cevaplayacağım."]}
    ])
    st.session_state.messages.append({"role": "assistant", "content": "Merhaba! Ben Mertcan'ın AI asistanıyım. Tecrübelerim, projelerim veya teknik yeteneklerim hakkında ne sormak istersiniz?"})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Sorunuzu buraya yazın..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Bir hata oluştu. API Key ayarlarını kontrol edin. Hata: {e}")
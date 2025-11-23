import streamlit as st
import google.generativeai as genai
import json

# --- 1. AYARLAR VE KURULUM ---
st.set_page_config(page_title="Mertcan Sarıgül - AI Resume", page_icon="🌍", layout="centered")

# API Key Yönetimi (Streamlit Secrets veya Local)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    # Buraya test için key yazabilirsiniz ama GitHub'a atarken silin!
    st.error("API Key bulunamadı! Lütfen Streamlit Secrets ayarını yapın.")
    st.stop()

genai.configure(api_key=api_key)
MODEL_NAME = "gemini-2.0-flash" # Hız ve performans için ideal

# --- 2. HAFIZA: YAPILANDIRILMIŞ CV VERİSİ (JSON) ---
# Bu yapı, botun verileri karıştırmadan %100 doğru çekmesini sağlar.
cv_data = {
    "TR": {
        "system_prompt": "Sen Mertcan Sarıgül'ün yapay zeka asistanısın. Türkçe cevap ver. Cevapların profesyonel, samimi ve sadece verilen JSON verisine dayalı olsun.",
        "greeting": "Merhaba! Ben Mertcan'ın AI asistanıyım. Sol menüden dil seçebilirsiniz. Size nasıl yardımcı olabilirim?",
        "data": """
        {
          "profil": {
            "isim": "Mertcan Sarıgül",
            "unvan": "Yazılım Geliştirme Uzmanı & Veri Bilimci",
            "ozet": "Büyük ölçekli yazılım projeleri, bankacılık uygulamaları ve üretim planlama sistemlerinde 4+ yıl deneyim. Spring Boot, Microservisler ve LLM konularında uzman."
          },
          "egitim": [
            {"okul": "Ege Üniversitesi", "derece": "Yüksek Lisans - Bilgisayar Müh.", "tarih": "2023-2025", "not": "Tez konusu: Büyük Dil Modelleri (LLM) ve karmaşık veri analizi."},
            {"okul": "Dokuz Eylül Üniversitesi", "derece": "Lisans - Bilgisayar Müh.", "tarih": "2016-2021", "not": "Tez: İşaret Dili Çeviri Programı."}
          ],
          "deneyim": [
            {
              "firma": "Boutique Rugs (ABD)",
              "pozisyon": "Yazılım Geliştirme Uzmanı",
              "tarih": "07/2023 - 08/2025",
              "detaylar": "Java, Spring Boot ve Hibernate ile E-Ticaret ve WMS geliştirdi. Barkodlu stok takibi için Android uygulama yazdı. Docker kullandı."
            },
            {
              "firma": "Yapı Kredi Teknoloji",
              "pozisyon": "Yazılım Geliştirici",
              "tarih": "10/2022 - 05/2023",
              "detaylar": "Bankacılık dış ticaret süreçleri. Java, Spring Boot, React, Oracle SQL, Microservices, Jenkins."
            },
            {
              "firma": "Vestel",
              "pozisyon": "Veri Bilimci & Jr. Yazılım Geliştirici",
              "tarih": "10/2021 - 10/2022",
              "detaylar": "X-ray görüntü işleme (ML) ile kalite tahmini. 'Game Plan' projesi ile üretim optimizasyonu."
            }
          ],
          "teknolojiler": ["Java", "Spring Boot", "Python", "SQL", "Docker", "Machine Learning", "NLP", "LLM", "React", "Jenkins", "Git"]
        }
        """
    },
    "ENG": {
        "system_prompt": "You are Mertcan Sarıgül's AI assistant. Answer in English. Be professional, concise, and strictly base your answers on the provided JSON data.",
        "greeting": "Hello! I am Mertcan's AI assistant. You can ask me about his projects, skills, or experience.",
        "data": """
        {
          "profile": {
            "name": "Mertcan Sarıgül",
            "title": "Software Development Specialist & Data Scientist",
            "summary": "4+ years of experience in large-scale software projects, banking applications, and operational technologies. Expert in Spring Boot, Microservices, and LLMs."
          },
          "education": [
            {"school": "Ege University", "degree": "M.Sc. Computer Engineering", "date": "2023-2025", "note": "Thesis: Large Language Models (LLM) and complex dataset analysis."},
            {"school": "Dokuz Eylul University", "degree": "B.Sc. Computer Engineering", "date": "2016-2021", "note": "Thesis: Sign Language Translation Program."}
          ],
          "experience": [
            {
              "company": "Boutique Rugs (USA)",
              "position": "Software Development Specialist",
              "date": "07/2023 - 08/2025",
              "details": "Developed E-Commerce and WMS using Java, Spring Boot, Hibernate. Built Android app for barcode tracking. Used Docker."
            },
            {
              "company": "Yapi Kredi Technology",
              "position": "Software Developer",
              "date": "10/2022 - 05/2023",
              "details": "Banking foreign trade processes. Java, Spring Boot, React, Oracle SQL, Microservices, Jenkins."
            },
            {
              "company": "Vestel",
              "position": "Data Scientist & Jr. Software Developer",
              "date": "10/2021 - 10/2022",
              "details": "Predicted product quality using ML on X-ray images. Developed 'Game Plan' optimization project."
            }
          ],
          "skills": ["Java", "Spring Boot", "Python", "SQL", "Docker", "Machine Learning", "NLP", "LLM", "React", "Jenkins", "Git"]
        }
        """
    }
}

# --- 3. ARAYÜZ VE DİL SEÇİMİ ---
# Yan menü oluşturuyoruz
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1998/1998664.png", width=100) # Profil resmi veya ikon
    st.title("Settings / Ayarlar")
    language = st.radio("Select Language / Dil Seçimi:", ["Türkçe", "English"])
    
    st.markdown("---")
    st.caption("Developed by Mertcan Sarıgül")
    st.caption("Powered by Gemini 2.0")
    
    # İletişim Butonları
    st.link_button("LinkedIn Profilim", "https://www.linkedin.com/in/mertcan-sarigül-2213341b6")
    st.link_button("Email Gönder", "mailto:mrtcn.srgll@gmail.com")

# Dil değişirse hafızayı temizle (Yoksa Türkçe sorup İngilizce cevap alırsınız)
if "last_language" not in st.session_state:
    st.session_state.last_language = language

if st.session_state.last_language != language:
    st.session_state.messages = []
    st.session_state.chat = None
    st.session_state.last_language = language
    st.rerun()

# Seçilen dilin verisini çek
current_context = cv_data["TR"] if language == "Türkçe" else cv_data["ENG"]

# --- 4. CHAT BAŞLATMA ---
st.title(f"Mertcan Sarıgül | AI Resume 🧠")
st.markdown(f"**{current_context['data'].split('unvan')[1].split('ozet')[0].replace(':', '').replace('\"', '').replace(',', '').strip() if language == 'TR' else 'Software Development Specialist & Data Scientist'}**")

if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = []
    
    # Modeli başlat ve JSON verisini "System Instruction" gibi ver
    model = genai.GenerativeModel(MODEL_NAME)
    st.session_state.chat = model.start_chat(history=[
        {"role": "user", "parts": [f"{current_context['system_prompt']} \n\n DATA: {current_context['data']}"]},
        {"role": "model", "parts": ["OK. I am ready."]}
    ])
    
    # İlk karşılama mesajı
    st.session_state.messages.append({"role": "assistant", "content": current_context['greeting']})

# Geçmiş mesajları yazdır
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan girdi al
prompt_text = "Sorunuzu buraya yazın..." if language == "Türkçe" else "Ask a question here..."
if prompt := st.chat_input(prompt_text):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")

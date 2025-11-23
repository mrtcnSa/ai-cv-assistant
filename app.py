import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR ---
st.set_page_config(page_title="Mertcan Sarıgül - AI Resume", page_icon="🧠", layout="wide")

# API Key Kontrolü
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    # GitHub'a atarken burayı silebilirsiniz, local test içindir.
    st.error("API Key bulunamadı! Lütfen Streamlit Secrets ayarlarını kontrol edin.")
    st.stop()

genai.configure(api_key=api_key)
MODEL_NAME = "gemini-2.0-flash"

# --- 2. DETAYLANDIRILMIŞ HAFIZA (FULL İÇERİK) ---
cv_data = {
    "TR": {
        "system_prompt": "Sen Mertcan Sarıgül'ün yapay zeka asistanısın. Türkçe cevap ver. Cevapların profesyonel ve samimi olsun. Aşağıdaki veriler Mertcan'ın gerçek CV'sidir, detayları atlamadan kullan.",
        "greeting": "Merhaba! Ben Mertcan'ın AI asistanıyım. Sol menüden dil seçebilirsiniz. Mertcan'ın projeleri, teknik yetenekleri veya deneyimleri hakkında bana her şeyi sorabilirsiniz.",
        "data": """
        {
          "profil": {
            "isim": "Mertcan Sarıgül",
            "unvan": "Yazılım Geliştirme Uzmanı & Veri Bilimci",
            "ozet": "Makine öğrenimi, full-stack geliştirme ve süreç optimizasyonu konularında geniş deneyime sahip. Tahmine dayalı analitik ve özel yazılım çözümleri ile operasyonel verimliliği artırmaya odaklı. Problem çözme, işbirliği ve sürekli öğrenme zihniyetine sahip.",
            "motivasyon": "Sorumluluk, takım çalışması ve sürekli gelişime değer veren ortamlarda başarılı olurum. Karmaşık zorlukları çözmekten ve deneyimli mentorlardan öğrenmekten keyif alırım."
          },
          "egitim": [
            {
              "okul": "Ege Üniversitesi",
              "derece": "Yüksek Lisans - Bilgisayar Mühendisliği",
              "tarih": "2023-2025",
              "gpa": "3.60/4.00",
              "detay": "Tez Konusu: Büyük Dil Modelleri (LLM) ve bunların karmaşık veri setlerini anlama ve analiz etmedeki uygulamaları."
            },
            {
              "okul": "Dokuz Eylül Üniversitesi",
              "derece": "Lisans - Bilgisayar Mühendisliği",
              "tarih": "2016-2021",
              "gpa": "3.28/4.00",
              "detay": "Tez Projesi: Türkçe metinleri işaret diline çeviren bir program geliştirilmesi."
            }
          ],
          "deneyim": [
            {
              "firma": "Boutique Rugs (ABD)",
              "pozisyon": "Yazılım Geliştirme Uzmanı",
              "tarih": "07/2023 - 08/2025",
              "sorumluluklar": [
                "Java, Spring Boot ve Hibernate (hem eski hem yeni sürümler) kullanarak kapsamlı bir E-Ticaret ve Depo Yönetim Sistemi (WMS) geliştirdi ve bakımını yaptı.",
                "WMS operasyonları için barkod tarayıcı özellikli bir Android mobil uygulama geliştirdi ve optimize etti.",
                "Satınalma Siparişi (PO) süreçlerini tasarladı ve iş akışını otomatikleştirerek manuel hataları azalttı.",
                "Mobil uygulama ve WMS arasında gerçek zamanlı veri senkronizasyonu sağladı.",
                "Depo personelinin stok seviyelerini ve sipariş durumlarını izlemesi için detaylı raporlama özellikleri ekledi.",
                "Uygulamaların tutarlılığı ve ölçeklenebilirliği için Docker kullandı."
              ]
            },
            {
              "firma": "Yapı Kredi Teknoloji",
              "pozisyon": "Yazılım Geliştirici",
              "tarih": "10/2022 - 05/2023",
              "sorumluluklar": [
                "Bankacılık dış ticaret süreçleri için Java, Spring Boot, React ve Oracle SQL kullanarak yazılım çözümleri geliştirdi.",
                "Monolitik ve Mikroservis mimarileri üzerinde çalışarak sistem esnekliğini artırdı.",
                "Veri akışını ve performansı optimize etmek için veritabanlarını yönetti.",
                "Jenkins ve Docker kullanarak CI/CD süreçlerini (otomatik test, derleme, dağıtım) uyguladı.",
                "Agile/Scrum ortamında çalışarak sprint teslimatlarına katkıda bulundu."
              ]
            },
            {
              "firma": "Vestel",
              "pozisyon": "Veri Bilimci & Jr. Yazılım Geliştirici",
              "tarih": "10/2021 - 10/2022",
              "sorumluluklar": [
                "X-ray görüntülerini analiz ederek ürün kalite sonuçlarını tahmin eden Makine Öğrenmesi (ML) modelleri geliştirdi.",
                "ASP.NET MVC (C# ve MSSQL) kullanarak üretim geri bildirim süreçlerini dijitalleştirdi.",
                "Üretim hattı planlaması için CPLEX tabanlı matematiksel optimizasyon uyguladı.",
                "'Game Plan' projesi: TV üretim izlenebilirliği için büyük ölçekli bir optimizasyon uygulaması geliştirdi. Bu sistem, her istasyon ve banttaki üretim aşamalarını takip etti."
              ]
            }
          ],
          "stajlar": [
            {"firma": "Innosa IT", "pozisyon": "Jr. DBA", "tarih": "05/2021-07/2021"},
            {"firma": "Dokuz Eylül Üni", "pozisyon": "Jr. Data Scientist", "tarih": "08/2020-09/2020"},
            {"firma": "Elsis Energy Systems", "pozisyon": "Donanım Asistanı", "tarih": "07/2019-08/2019"}
          ],
          "teknik_yetenekler": {
            "diller": ["Java", "Python", "C#", "PySpark", "SQL"],
            "veritabani": ["SQL Server (İleri)", "Oracle SQL", "PostgreSQL", "MongoDB", "MySQL"],
            "ai_ml": ["Veri Madenciliği", "ML Algoritmaları", "Karar Destek Sistemleri", "LLM", "Apache Spark", "BioBERT"],
            "araclar": ["Docker", "Jenkins", "Git", "JIRA", "Confluence", "VS Code", "Eclipse", "Jupyter", "Spyder"],
            "yabanci_dil": ["Türkçe (Anadil)", "İngilizce (Konuşma Düzeyi)", "Almanca (Temel)"]
          }
        }
        """
    },
    "ENG": {
        "system_prompt": "You are Mertcan Sarıgül's AI assistant. Answer in English. Be professional and friendly. The following data is Mertcan's actual resume, use all details provided.",
        "greeting": "Hello! I am Mertcan's AI assistant. You can change the language from the sidebar. Feel free to ask me anything about Mertcan's projects, skills, or background.",
        "data": """
        {
          "profile": {
            "name": "Mertcan Sarıgül",
            "title": "Software Development Specialist & Data Scientist",
            "summary": "Driven Data Scientist and Software Developer with extensive experience in machine learning, full-stack development, and process optimization. Skilled in leveraging predictive analytics and custom software solutions to enhance operational efficiency. Known for delivering impactful results through collaboration, problem-solving, and a continuous learning mindset.",
            "motivation": "I thrive in environments that value responsibility, teamwork, and continuous improvement. I enjoy tackling complex challenges in a collaborative environment."
          },
          "education": [
            {
              "school": "Ege University",
              "degree": "Master's in Computer Engineering",
              "date": "2023-2025",
              "gpa": "3.60/4.00",
              "detail": "Thesis: Focused on Large Language Models (LLM) and their application in understanding and analyzing complex datasets."
            },
            {
              "school": "Dokuz Eylul University",
              "degree": "B.Sc. in Computer Engineering",
              "date": "2016-2021",
              "gpa": "3.28/4.00",
              "detail": "Thesis: Developed a program that translates Turkish texts into sign language."
            }
          ],
          "experience": [
            {
              "company": "Boutique Rugs (USA)",
              "position": "Software Development Specialist",
              "date": "07/2023 - 08/2025",
              "responsibilities": [
                "Developed and maintained a comprehensive e-Commerce and Warehouse Management System (WMS) in Java, using both old and new versions of Hibernate with Spring Boot.",
                "Built and optimized an Android mobile application for WMS operations with barcode scanner functionality.",
                "Led the design and implementation of Purchase Order (PO) processes, automating workflows.",
                "Integrated real-time data synchronization between the mobile app and WMS.",
                "Enhanced barcode scanning capabilities for faster inventory management.",
                "Utilized Docker for containerization of Java applications."
              ]
            },
            {
              "company": "Yapi Kredi Technology (Turkey)",
              "position": "Software Developer",
              "date": "10/2022 - 05/2023",
              "responsibilities": [
                "Developed software solutions for banking foreign trade processes using Java, Spring Boot, React, and Oracle SQL.",
                "Built and maintained both monolithic and microservices architectures with Spring Boot.",
                "Managed databases to optimize data flow and performance.",
                "Implemented CI/CD pipelines using Jenkins and Docker.",
                "Worked in a Scrum environment, collaborating in agile sprints."
              ]
            },
            {
              "company": "Vestel (Turkey)",
              "position": "Data Scientist & Jr. Software Developer",
              "date": "10/2021 - 10/2022",
              "responsibilities": [
                "Predicted product quality outcomes using machine learning models to analyze X-ray images.",
                "Digitalized production feedback processes through an ASP.NET MVC web application, utilizing C# and MSSQL.",
                "Led the implementation of CPLEX-based mathematical optimization for production line planning.",
                "Took a leading role in 'Game Plan', a large-scale optimization application for TV production traceability."
              ]
            }
          ],
          "internships": [
            {"company": "Innosa IT", "position": "Jr. DBA", "date": "05/2021-07/2021"},
            {"company": "Dokuz Eylul University", "position": "Jr. Data Scientist", "date": "08/2020-09/2020"},
            {"company": "Elsis Energy Systems", "position": "Hardware Assistant Specialist", "date": "07/2019-08/2019"}
          ],
          "technical_skills": {
            "programming": ["Python", "C#", "Java", "PySpark"],
            "databases": ["SQL Server (Advanced)", "Oracle SQL", "PostgreSQL", "MongoDB", "MySql"],
            "ml_data": ["Data Mining", "ML Algorithms", "Decision Support Systems", "LLM", "Apache Spark"],
            "tools": ["Jupyter", "Spyder", "VS Code", "Eclipse", "Docker", "Jenkins", "Git", "JIRA", "Bitbucket"],
            "languages": ["Turkish (Native)", "English (Conversational)", "German (Basic)"]
          }
        }
        """
    }
}

# --- 3. ARAYÜZ VE MANTIK ---

# Kenar Çubuğu
with st.sidebar:
    st.header("⚙️ Ayarlar / Settings")
    # Dil Seçimi
    language = st.radio("Dil Seçin / Select Language:", ["Türkçe", "English"])
    
    st.markdown("---")
    st.markdown("**Mertcan Sarıgül**")
    st.caption("Software Development Specialist\n& Data Scientist")
    
    # İletişim Linkleri
    st.link_button("🚀 LinkedIn", "https://www.linkedin.com/in/mertcan-sarigül-2213341b6")
    st.link_button("📧 Send Email", "mailto:mrtcn.srgll@gmail.com")

# Dil Değişikliği Kontrolü (Hafızayı sıfırlamak için)
if "last_language" not in st.session_state:
    st.session_state.last_language = language

if st.session_state.last_language != language:
    st.session_state.messages = []
    st.session_state.chat = None
    st.session_state.last_language = language
    st.rerun()

# Seçili veriyi al
current_context = cv_data["TR"] if language == "Türkçe" else cv_data["ENG"]

# Ana Başlık
st.title("Mertcan Sarıgül | AI Resume 🤖")
st.markdown(f"**{current_context['data'].split('unvan')[1].split('ozet')[0].replace(':', '').replace('\"', '').replace(',', '').strip() if language == 'Türkçe' else 'Software Development Specialist & Data Scientist'}**")

# Chat Başlatma
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = []
    
    model = genai.GenerativeModel(MODEL_NAME)
    # Bağlam Yükleme (Context Injection)
    st.session_state.chat = model.start_chat(history=[
        {"role": "user", "parts": [f"{current_context['system_prompt']} \n\n DATA: {current_context['data']}"]},
        {"role": "model", "parts": ["Anlaşıldı. Verileri kaydettim." if language == "Türkçe" else "Understood. Data loaded."]}
    ])
    
    # Karşılama Mesajı
    st.session_state.messages.append({"role": "assistant", "content": current_context['greeting']})

# Mesajları Ekrana Basma
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı Girdisi
placeholder = "Mertcan hakkında bir soru sorun..." if language == "Türkçe" else "Ask a question about Mertcan..."
if prompt := st.chat_input(placeholder):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Hata/Error: {e}")

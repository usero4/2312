import streamlit as st
from pathlib import Path
import google.generativeai as genai
import os
from weasyprint import HTML

# تكوين مفتاح الـ API من متغير بيئي
API_KEY = 'AIzaSyC0US-sr4H1Y-BS4vFuGsB81Oxaqy6pixA'
if not API_KEY:
    raise ValueError("API key is not set. Please set the GOOGLE_API_KEY environment variable.")
genai.configure(api_key=API_KEY)

# تكوين الإنتاج
generation_config = {
    "temperature": 1,  # درجة الحرارة، تحكم تباين الإخراج
    "top_p": 0.95,  # أعلى احتمال تراكمي
    "top_k": 1,  # أعلى قيمة k
    "max_output_tokens": 8192,  # الحد الأقصى لعدد التوكنات في الإخراج
    "response_mime_type": "text/plain",  # نوع MIME للاستجابة
}

# إعدادات الأمان
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},  # عتبة للمضايقة
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},  # عتبة للكلام الكراهية
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},  # عتبة للمحتوى الجنسي الصريح
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},  # عتبة للمحتوى الخطر
]

# اسم النموذج
MODEL_NAME = "gemini-1.5-pro-latest"

# إنشاء النموذج
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    safety_settings=safety_settings,
    generation_config=generation_config,
)

# بدء جلسة الدردشة
chat_session = model.start_chat(history=[])

# دالة لإرسال رسالة إلى النموذج
def send_message_to_model(message):
    response = chat_session.send_message([message])
    return response.text

# تعريف استثناء مخصص لإيقاف الترجمة
class StopTranslation(Exception):
    pass

# دالة للتحقق من طلب إيقاف الترجمة
def check_for_stop():
    if st.button("stop translation", key="stop_button"):
        raise StopTranslation("تم إيقاف الترجمة بناءً على طلبك.")

# Streamlit app
def main():
    st.title("Gemini 1.5 Pro, UI to Code 👨‍💻 ")
    st.subheader('Made with ❤️ by [Skirano](https://x.com/skirano)')

    text_file = st.text_area("set your text here")
    target_lang = st.text_input("set the target language here")

    if st.button("start translation", key="start_button"):
        try:
            # Generate UI description
            check_for_stop()  # التحقق من طلب الإيقاف
            st.write("🧑‍💻 Looking at your UI...")
            prompt = f"Write a dictionary in the format " source language name, target language name, gender " target language is :{target_lang}, {text_file}"
            description = send_message_to_model(prompt)
            st.write(dictionary)

            # Refine the description
            st.write("🔍 Refining description with visual comparison...")
            translation_1 = f"translate to :{target_lang}, {dictionary}, {text_file}"
            trans_1 = send_message_to_model(translation_1)
            st.write(trans_1)

            # Generate HTML
            st.write("🛠️ Generating website...")
            translation_2 = f"continue translate to :{target_lang}, {text_file}"
            trans_2 = send_message_to_model(translation_2)
            st.write(trans_2)

            # Refine HTML
            st.write("🔧 Refining website...")
            translation_3 = f"continue translate to :{target_lang}, {text_file}"
            trans_3 = send_message_to_model(translation_3)
            st.write(trans_3)

            # تحويل HTML إلى PDF باستخدام WeasyPrint
            with open("temp.html", "w", encoding="utf-8") as f:
                f.write(trans_1, trans_2, trans_3)
            HTML("temp.html").write_pdf("translate.pdf")

            # توفير خيارات التحميل
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="Download HTML",
                    data=refined_html.encode(),
                    file_name="translate.html",
                    mime="text/html",
                    key="download_html_button"
                )
            with col2:
                with open("translate.pdf", "rb") as pdf_file:
                    PDFbyte = pdf_file.read()
                st.download_button(
                    label="Download PDF",
                    data=PDFbyte,
                    file_name="translate.pdf",
                    mime="application/pdf",
                    key="download_pdf_button" 
                )

        except StopTranslation as e:
            st.warning(str(e))
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

import streamlit as st
from pathlib import Path
import google.generativeai as genai
import pdfkit  # استيراد مكتبة pdfkit
import os

# تكوين مفتاح الـ API من متغير بيئي
API_KEY = os.getenv('GOOGLE_API_KEY')
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
    if st.button("stop translation"):
        raise StopTranslation("تم إيقاف الترجمة بناءً على طلبك.")

# Streamlit app
def main():
    st.title("Gemini 1.5 Pro, UI to Code 👨‍💻 ")
    st.subheader('Made with ❤️ by [Skirano](https://x.com/skirano)')

    text_file = st.text_area("set your text here")
    target_lang = st.text_input("set the target language here")

    if st.button("start translation"):
        try:
            # Generate UI description
            check_for_stop()  # التحقق من طلب الإيقاف
            st.write("🧑‍💻 Looking at your UI...")
            prompt = f"translate to :{target_lang}, {text_file}"
            description = send_message_to_model(prompt)
            st.write(description)

            # Refine the description
            check_for_stop()  # التحقق من طلب الإيقاف
            st.write("🔍 Refining description with visual comparison...")
            refine_prompt = f"Compare the described UI elements with the provided text and identify any missing elements or inaccuracies. Also Describe the color of the elements. Provide a refined and accurate description of the UI elements based on this comparison. Here is the initial description: {description}"
            refined_description = send_message_to_model(refine_prompt)
            st.write(refined_description)

            # Generate HTML
            check_for_stop()  # التحقق من طلب الإيقاف
            st.write("🛠️ Generating website...")
            html_prompt = f"Create an HTML file based on the following UI description, using the UI elements described in the previous response. Include CSS within the HTML file to style the elements. Make sure the colors used are the same as the original UI. The UI needs to be responsive and mobile-first, matching the original UI as closely as possible. Do not include any explanations or comments. Avoid using ```html. and ``` at the end. ONLY return the HTML code with inline CSS. Here is the refined description: {refined_description}"
            initial_html = send_message_to_model(html_prompt)
            st.write(initial_html, language='html')

            # Refine HTML
            check_for_stop()  # التحقق من طلب الإيقاف
            st.write("🔧 Refining website...")
            refine_html_prompt = f"Validate the following HTML code based on the UI description and text and provide a refined version of the HTML code with CSS that improves accuracy, responsiveness, and adherence to the original design. ONLY return the refined HTML code with inline CSS. Avoid using ```html. and ``` at the end. Here is the initial HTML: {initial_html}"
            refined_html = send_message_to_model(refine_html_prompt)
            st.write(refined_html, language='html')

            # تحويل HTML إلى PDF
            with open("temp.html", "w", encoding="utf-8") as f:
                f.write(refined_html)
            pdfkit.from_file("temp.html", "translate.pdf", options={"enable-local-file-access": ""})

            # توفير خيارات التحميل
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="Download HTML",
                    data=refined_html.encode(),
                    file_name="translate.html",
                    mime="text/html",
                )
            with col2:
                with open("translate.pdf", "rb") as pdf_file:
                    PDFbyte = pdf_file.read()
                st.download_button(
                    label="Download PDF",
                    data=PDFbyte,
                    file_name="translate.pdf",
                    mime="application/pdf",
                )

        except StopTranslation as e:
            st.warning(str(e))
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

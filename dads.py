import streamlit as st
import pathlib
import PyPDF2
import google.generativeai as genai

# تكوين مفتاح الـ API مباشرة في البرنامج
API_KEY = 'YOUR KEY'
genai.configure(api_key=API_KEY)

# تكوين الإنتاج
generation_config = {
    "temperature": 1,  # درجة الحرارة، تحكم تباين الإخراج
    "top_p": 0.95,  # أعلى احتمال تراكمي
    "top_k": 64,  # أعلى قيمة k
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

# تطبيق Streamlit
def main():
    st.title("PDF Translator with Gemini 1.5 Pro")
    st.subheader('Made with ❤️ by [Your Name](https://your-profile.com)')

    uploaded_file = st.file_uploader("Choose a PDF file...", type=["pdf"])

    if uploaded_file is not None:
        try:
            # حفظ الملف المرفوع بشكل مؤقت
            temp_pdf_path = pathlib.Path("temp_pdf.pdf")
            temp_pdf_path.write_bytes(uploaded_file.read())

            # قراءة المحتوى من ملف PDF
            pdf_reader = PyPDF2.PdfFileReader(str(temp_pdf_path))
            text = ""
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text += page.extract_text()

            # توليد وصف للمحتوى
            if st.button("Translate PDF"):
                st.write("🧑‍💻 Analyzing PDF content...")
                prompt = f"Translate the following text from English to Spanish: {text}"
                translation = send_message_to_model(prompt)
                st.write(translation)

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

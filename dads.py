import streamlit as st
import pathlib
from PIL import Image  # لا نحتاجها في هذا السيناريو
import google.generativeai as genai

# تكوين مفتاح الـ API مباشرة في البرنامج (يجب تجنب هذا في الإنتاج)
API_KEY = 'AIzaSyDMlyV1-x32KlZa3Q-bUg2qIA3HkYrMMRY'
genai.configure(api_key=API_KEY)

# تكوين الإنتاج
generation_config = {
    "temperature": 1,  # درجة الحرارة، تحكم تباين الإخراج
    "top_p": 0.95,  # أعلى احتمال تراكمي
    "top_k": 14,  # أعلى قيمة k
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

# تطبيق Streamlit
def main():
    st.title("Gemini 1.5 Pro, UI to Code 👨‍💻 ")
    st.subheader('Made with ❤️ by [Skirano](https://x.com/skirano)')

    user_input = st.text_area("Enter your text here...")

    if user_input:
        try:
            # إنشاء وصف لواجهة المستخدم
            if st.button("Code UI"):
                st.write("🧑‍💻 Looking at your UI...")
                prompt = "قم بوصف النص."
                description = send_message_to_model(prompt)
                st.write(description)

                # تنقيح الوصف
                st.write("🔍 Refining description with visual comparison...")
                refine_prompt = f"قم بصناعة قاموس للنص: {description}"
                refined_description = send_message_to_model(refine_prompt)
                st.write(refined_description)

                # إنشاء HTML
                st.write("🛠️ Generating website...")
                html_prompt = f"قم بالترجمة إلى العربية: {refined_description}"
                initial_html = send_message_to_model(html_prompt)
                st.code(initial_html, language='html')

                # تنقيح HTML
                st.write("🔧 Refining website...")
                refine_html_prompt = f"قم بالتأكد أن الترجمة قد تمت إذا كانت ناقصة فأكملها وإن كانت كاملة فقل هي كاملة: {initial_html}"
                refined_html = send_message_to_model(refine_html_prompt)
                st.code(refined_html, language='html')

                # حفظ HTML المنقح في ملف
                with open("index.html", "w") as file:
                    file.write(refined_html)
                st.success("HTML file 'index.html' has been created.")

                # توفير رابط تنزيل لملف HTML
                st.download_button(label="Download HTML", data=refined_html, file_name="index.html", mime="text/html")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

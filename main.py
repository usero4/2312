import streamlit as st
import pathlib
import google.generativeai as genai

# Configure the API key directly in the script
API_KEY = 'AIzaSyDMlyV1-x32KlZa3Q-bUg2qIA3HkYrMMRY'
genai.configure(api_key=API_KEY)

# Generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Safety settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Model name
MODEL_NAME = "gemini-1.5-pro-latest"

# Create the model
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    safety_settings=safety_settings,
    generation_config=generation_config,
)

# Start a chat session
chat_session = model.start_chat(history=[])

# Function to send a message to the model
def send_message_to_model(message, text_path):
    text_input = {
        'mime_type': 'text/plain',
        'data': pathlib.Path(text_path).read_text()
    }
    response = chat_session.send_message([message, text_input])
    return response.text

# Streamlit app
def main():
    st.title("Gemini 1.5 Pro, Text to Code 👨‍💻 ")
    st.subheader('Made with ❤️ by [Skirano](https://x.com/skirano)')

    uploaded_file = st.file_uploader("Choose a text file...", type=["txt"])

    if uploaded_file is not None:
        try:
            # Save the uploaded text file temporarily
            temp_text_path = pathlib.Path("temp_text.txt")
            temp_text_path.write_text(uploaded_file.read().decode("utf-8"))

            # Generate code from text
            if st.button("ترجمة النصوص"):
                st.write("🧑‍💻 جاري الترجمة...")
                prompt = " f"قم بالترجمة إلى العربية: {temp_text_path}"
                translate_output = send_message_to_model(prompt, temp_text_path)
                st.write(translate_output)

                # Refine the code
                st.write("🔍 Refining code...")
                refine_prompt = f"Refine the generated code based on the text description. Here is the initial code: {translate_output}"
                refined_code = send_message_to_model(refine_prompt, temp_text_path)
                st.write(refined_code)

                # Generate HTML
                st.write("🛠️ Generating HTML...")
                html_prompt = f"Create an HTML file based on the refined code. Include {framework} CSS within the HTML file to style the elements. Make sure the HTML is responsive and mobile-first. Do not include any explanations or comments. Avoid using ```html. and ``` at the end. ONLY return the HTML code with inline CSS. Here is the refined code: {refined_code}"
                initial_html = send_message_to_model(html_prompt, temp_text_path)
                st.write(initial_html, language='html')

                # Refine HTML
                st.write("🔧 Refining HTML...")
                refine_html_prompt = f"Validate the following HTML code based on the text description and provide a refined version of the HTML code with {framework} CSS that improves accuracy, responsiveness, and adherence to the original design. ONLY return the refined HTML code with inline CSS. Avoid using ```html. and ``` at the end. Here is the initial HTML: {initial_html}"
                refined_html = send_message_to_model(refine_html_prompt, temp_text_path)
                st.write(refined_html, language='html')

                # Save the refined HTML to a file
                with open("index.html", "w") as file:
                    file.write(refined_html)
                st.success("HTML file 'index.html' has been created.")

                # Provide download link for HTML
                st.download_button(label="Download HTML", data=refined_html, file_name="index.html", mime="text/html")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

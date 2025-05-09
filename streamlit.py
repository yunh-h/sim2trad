import streamlit as st
import openai
from datetime import datetime
import pandas as pd

# Set OpenAI API key
openai.api_key = ""
model_id = "ft:gpt-4o-mini-2024-07-18:emily-ho:kde2:BSwUQZS8"

st.markdown("# Simplified to Traditional Chinese Translation\n## 簡中轉台灣繁中翻譯器")
st.markdown("### How to use 使用說明 \n1. Choose a translation style\n\n選擇一個想要的翻譯風格\n\n2. Enter a Simplified Chinese sentence or upload a TXT file below\n\n在下方輸入框中輸入簡體中文句子或上傳一個文字檔\n\n3. Press 'Send' to get the translation result\n\n點擊「Send」按鍵以獲取翻譯結果\n\n4. Modify the output if needed\n\n如有需要可修改翻譯結果\n\n5. Save the translation to history\n\n點擊「Save」按鍵以儲存翻譯結果至歷史紀錄\n\n6. Download the translation history as a CSV file\n\n點擊「Download」按鍵以下載翻譯歷史紀錄為CSV檔案")

if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("#### Translation Style  翻譯風格")
style = st.radio(
    "Choose a translation style:",
    ("Formal", "Casual", "Neutral"),
    index=2,
    key="global_style"
)

style_prompt = {
    "Formal": "把以下簡體中文**翻譯**成台灣繁體中文，使用正式的用語和語法：",
    "Casual": "把以下簡體中文**翻譯**成台灣繁體中文，使用口語化的用語和語法：",
    "Neutral": "把以下簡體中文**翻譯**成台灣繁體中文："
}[style]

# In Development: Add support for multiple translation types
# st.markdown("#### Translation Type")
# translation_type = st.radio(
#     "Choose a translation style:",
#     ("Literal Translation", "Idiomatic Translation"),
#     index=0,
#     key="global_type"
# )

# type_prompt = {
#   "Literal Translation": "把以下簡體中文**轉換**成繁體中文，只做字面轉換，如：软件 -> 軟件。",
#   "Idiomatic Translation": "把以下簡體中文**翻譯**成繁體中文，包含用語習慣和文化細節，如：软件 -> 軟體。"
#   "Literal Translation": "ONLY focus on literal word-to-word conversion. ",
#   "Idiomatic Translation": "Include idiomatic expressions and cultural nuances. "
# }[translation_type]

prompt = f"""你是一名了解台灣本土文化及語言習慣的專家，專門將簡體中文翻譯成台灣正體中文。請提供準確且符合台灣文化的本地化翻譯，**保留並使用適當的全形標點符號**。依據以下步驟進行翻譯：
1. 將簡體中文轉換為繁體中文
2. 確保翻譯符合台灣的語言使用和文化背景
3. 使用適當的全形標點符號

範例：
簡體輸入：这加工厂生产的产品质量很好，深受消费者喜爱。
繁體輸出：這家加工廠生產的產品品質很好，深受消費者喜愛。

簡體輸入：这个平台提供丰富的数字内容，比如电子书和在线课程。
繁體輸出：這個平台提供豐富的數位內容，比如電子書和線上課程。

簡體輸入：这只流浪猫很瘦，它可能饿了很久。
繁體輸出：這隻流浪貓很瘦，牠可能餓了很久。

請仿照以上的例子，簡潔地回答。{style_prompt}\n\n"""

tab1, tab2 = st.tabs(["Text Input", "File Upload"])    

# Single Sentence Translation Section
with tab1:
    st.markdown("### Text Translation (Single Input)")
    user_input = st.text_area("Enter your sentence:", placeholder="Type something...", height=100)

    if "output" not in st.session_state:
        st.session_state.output = ""

    if st.button("Send"):
        if user_input.strip():
            try:
                final_prompt = f"{prompt}\n\n{user_input}"

                response = openai.ChatCompletion.create(
                    model=model_id,
                    messages=[{"role": "user", "content": final_prompt}],
                    temperature=0.4,
                    top_p=0.5
                )
                result = response['choices'][0]['message']['content']
                st.session_state.output = result

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a sentence to translate!")
    
    output = st.text_area("Response:", st.session_state.output, height=100)
    if st.button("Save"):
        st.session_state.output = output 
        st.session_state.history.append({
            "input": user_input,
            "output": st.session_state.output,
            "time": datetime.now().strftime("%Y-%m-%d")
        })
        st.success("Translation saved to history!")                

# Batch Translation Section
with tab2:
    st.markdown("### Batch Translation (Upload a File)")
    uploaded_file = st.file_uploader("Upload a text file for batch translation", type=["txt"])

    if uploaded_file:
        st.success("File uploaded successfully! Press 'Translate' to start translation.")
        if st.button("Translate"):
            try:
                content = uploaded_file.read().decode("utf-8").splitlines()
                translations = []

                for line in content:
                    if line.strip():
                        final_prompt = f"{prompt}\n\n{line}"

                        response = openai.ChatCompletion.create(
                            model=model_id,
                            messages=[{"role": "user", "content": final_prompt}],
                            temperature=0.4,
                            top_p=0.6
                        )
                        result = response['choices'][0]['message']['content']
                        translations.append({"input": line, "output": result})

                st.markdown("### Batch Translation Results")
                for i, record in enumerate(translations, 1):
                    st.markdown(f"**{i}. Input:** {record['input']}")
                    st.markdown(f"**Output:** {record['output']}")
                    st.markdown("---")

                df = pd.DataFrame(translations)
                csv = df.to_csv(index=False, encoding="utf-8-sig")
                st.download_button(
                    label="Download Batch Translation Results as CSV",
                    data=csv,
                    file_name="batch_translation_results.csv",
                    mime="text/csv",
                )

                st.session_state.history.append({
                    "input": record['input'],
                    "output": record['output'],
                    "time": datetime.now().strftime("%Y-%m-%d")
                })
                
            except Exception as e:
                st.error(f"Error processing the uploaded file: {e}")

# Sidebar: Translation History Section
with st.sidebar:
    st.markdown("### Translation History")
    if st.session_state.history:
        for i, record in enumerate(st.session_state.history[::-1], 1):
            preview = record['input'][:20] + "..." if len(record['input']) > 20 else record['input']
            timestamp = record['time']

            with st.expander(f"{i}. {preview} ({timestamp})"):
                st.markdown(f"**Input:**\n{record['input']}")
                st.markdown(f"**Output:**\n{record['output']}")
        
        df = pd.DataFrame(st.session_state.history)
        csv = df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="Download Translation History as CSV",
            data=csv,
            file_name="translation_history.csv",
            mime="text/csv",
        )
    else:
        st.info("No history yet.")

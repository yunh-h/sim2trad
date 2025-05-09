import openai
import json
import argparse

openai.api_key = ""

sys_prompt_zh = """你是一名了解台灣本土文化及語言習慣的專家，專門將簡體中文翻譯成台灣正體中文。請提供準確且符合台灣文化的本地化翻譯，**保留並使用適當的全形標點符號**。依據以下步驟進行翻譯：
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

請仿照以上的例子，簡潔地回答。"""

sys_prompt_en = """You are a translator specialized in converting Simplified Chinese to Traditional Chinese used in Taiwan. You are an expert of language use and culture in Taiwan. Please provide accurate and culturally appropriate conversion or translations that align language and punctuation use in Taiwan. Please use the same punctuation as the input, and answer concisely. Follow the steps below:
1. Convert Simplified Chinese to Traditional Chinese.
2. Ensure the translation aligns with the language usage and cultural context of Taiwan.
3. Use appropriate full-width punctuation.

Examples:
simplified input: 这加工厂生产的产品质量很好，深受消费者喜爱。
traditional output: 這家加工廠生產的產品品質很好，深受消費者喜愛。

simplified input:这个平台提供丰富的数字内容，比如电子书和在线课程。
traditional output: 這個平台提供豐富的數位內容，比如電子書和線上課程。

simplified input: 这只流浪猫很瘦，它可能饿了很久。
traditional output: 這隻流浪貓很瘦，牠可能餓了很久。
"""

MODEL_ID = "ft:gpt-4o-mini-2024-07-18:emily-ho:kde2:BSwUQZS8"

def prepare_messages_from_jsonl(file_path):
    messages_list = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            simplified = data["simplified"]
            traditional = data["traditional"]
            messages = [
                {"role": "system", "content": sys_prompt_zh},
                {"role": "user", "content": f"將以下簡體中文轉換成台灣使用的繁體中文，並使用適當的標點符號: {simplified}"}
            ]
            messages_list.append((messages, traditional))
    return messages_list


def evaluate_model(file_path):
    """
    Evaluate the model using the provided JSONL file and model ID.

    :param file_path: Path to the JSONL file containing evaluation data.
    :param model_id: The OpenAI model ID to use for evaluation.
    """
    messages_list = prepare_messages_from_jsonl(file_path)

    for messages, expected_traditional in messages_list:
        response = openai.ChatCompletion.create(
            model=MODEL_ID,
            messages=messages,
            max_tokens=50,
            temperature=0.4,
            top_p=0.7
        )
        generated_traditional = response["choices"][0]["message"]["content"].strip()
        print(f"Input: {messages[1]['content']}")
        print(f"Expected: {expected_traditional}")
        print(f"Generated: {generated_traditional}")
        print("-" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate a GPT model for Simplified to Traditional Chinese translation.")
    parser.add_argument("file_path", type=str, help="Path to the JSONL file containing evaluation data.")
    args = parser.parse_args()

    evaluate_model(args.file_path)
import json


def convert_txt_to_jsonl(data_file, source_file, target_file, output_file):
    """
    Convert parallel text files in Simplified and Traditional Chinese into JSONL format.

    :param data_file: Path to the data folder
    :param source_file: Path to the Simplified Chinese file
    :param target_file: Path to the Traditional Chinese file
    :param output_file: Path to the output JSONL file
    """
    source_file = data_file + source_file
    target_file = data_file + target_file

    with open(source_file, 'r', encoding='utf-8') as src, open(target_file, 'r', encoding='utf-8') as tgt:
        source_lines = src.readlines()
        target_lines = tgt.readlines()

    if len(source_lines) != len(target_lines):
        raise ValueError("The number of lines in the two files is inconsistent. Please check the alignment of the parallel text.")

    messages = []

    with open(output_file, 'w', encoding='utf-8') as out_file:
        for source, target in zip(source_lines, target_lines):
            source = source.strip()
            target = target.strip()
            
            conversation = [
                    {"role": "system", "content": "You are a translator specialized in converting Simplified Chinese to Traditional Chinese used in Taiwan."},
                    {"role": "user", "content": source},
                    {"role": "assistant", "content": target}
                ]
            
            out_file.write(json.dumps({'messages': conversation}, ensure_ascii=False) + '\n')

    print(f"Conversion complete! Output file: {output_file}")


def format_for_gpt(input_file, output_file):
    """
    Format data for GPT model input by converting JSONL entries into a structured format.

    :param input_file: Path to the original JSONL file
    :param output_file: Path to the formatted JSONL file
    """
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            data = json.loads(line)
            prompt = data["prompt"]
            completion = data["completion"]
            
            formatted_text = {
                "messages": [
                    {"role": "system", "content": "You are an AI assistant specialized in Simplified Chinese to Traditional Chinese localization translation. Your goal is to provide accurate translation that align with the language uasge and cultural context of Taiwan."},
                    {"role": "user", "content": f"請將以下簡體中文翻譯成繁體中文：{prompt}"},
                    {"role": "assistant", "content": completion}
                ]
            }
            
            outfile.write(json.dumps(formatted_text, ensure_ascii=False) + "\n")

    print(f"Formatting complete. Output file: {output_file}")


def filter_top_n_long_sentences(input_file, output_file, n=5000, min_length=10):
    """
    Filter the top `n` entries where both the prompt and completion exceed the minimum length.

    :param input_file: Path to the original JSONL file
    :param output_file: Path to the filtered JSONL file
    :param n: Number of entries to filter
    :param min_length: Minimum character length requirement for both prompt and completion
    """
    filtered_data = []
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            data = json.loads(line)
            prompt_length = len(data['prompt'])
            completion_length = len(data['completion'])
            
            if prompt_length > min_length and completion_length > min_length:
                filtered_data.append(data)
            
            if len(filtered_data) >= n:
                break
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for item in filtered_data:
            outfile.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        print(f"The top {n} entries with lengths exceeding {min_length} have been saved to: {output_file}")


if __name__ == "__main__":
    datasets = [
        {'file': './original/KDE4/', 'source': 'KDE4.zh_CN-zh_TW.zh_CN', 'target': 'KDE4.zh_CN-zh_TW.zh_TW', 'output': './finetune/KDE4_role.jsonl'}
    ]

    for dataset in datasets:
        convert_txt_to_jsonl(dataset['file'], dataset['source'], dataset['target'], dataset['output'])

    input_file = './finetune/KDE4_cleaned.jsonl'
    output_file = './finetune/KDE4_5k.jsonl'
    filter_top_n_long_sentences(input_file, output_file, n=5000, min_length=10)

    # Format for GPT
    input_file = "./finetune/KDE4_5-10k_10.jsonl"
    output_file = "./finetune/formatted_KDE4_5-10k.jsonl"
    format_for_gpt(input_file, output_file)
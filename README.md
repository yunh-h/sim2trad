# Simplified to Traditional Chinese Translator

This is a Simplified Chinese to Traditional Chinese translation tool, specifically designed for localization to the Taiwanese context. This project leverages OpenAI's GPT models, fine-tuned on domain-specific datasets, to provide accurate and culturally appropriate translations. It supports both single-sentence translation and batch translation via file uploads, with additional features like translation history and CSV export.

---

## Features

- **Fine-Tuned GPT Model**: The translation tool uses a fine-tuned GPT model, specifically trained on Simplified-to-Traditional Chinese datasets for accurate localization to the Taiwanese context.
- **Single Sentence Translation**: Translate individual Simplified Chinese sentences into Traditional Chinese with customizable translation styles (Formal, Casual, Neutral).
- **Batch Translation**: Upload a `.txt` file for batch translation, with results downloadable as a CSV file.
- **Translation History**: Save and view past translations, with the option to download the history as a CSV file.
- **Customizable Translation Styles**: Choose from Formal, Casual, or Neutral styles to suit your needs.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yunh-h/sim2trad.git
   cd sim2trad
   ```
2. Install the required dependencies
    ```sh
    pip install -r requirements.txt
    ```
3. Set up your Open API key in `streamlit.py`

---

## Usage

Start the Streamlit application locally:
```sh
streamlit run streamlit.py
```
How to Use

1. Open the app in your browser (usually at http://localhost:8501).

2. Choose a translation style (Formal, Casual, or Neutral).

3. Enter a Simplified Chinese sentence or upload a `.txt` file for batch translation.

4. View the translation results, edit and save them to history if needed.

5. Download the translation history or batch results as a CSV file.

---

## File Structure

- `streamlit.py`: The main Streamlit application that serves as the user interface for the translation tool.
- `data/eval.py`: Script for evaluating the performance of the translation model using test datasets. It compares the model's output with expected results to measure accuracy and quality.
- `data/preprocessing.py`: Scripts for preprocessing and formatting data to prepare it for GPT model training and inference.
- `data/finetune/`: Directory containing fine-tuned datasets and translation results.
- `data/eval/`: Directory for storing evaluation datasets used for testing and validation.
- `Sim2Trad.pdf`: Presentation slides detailing the project overview and methodology.
- `demo.mp4`: A video demonstration showcasing how to use the application.

---

## Known Issues

- **Missing Punctuation in Generated Content**: The generated Traditional Chinese translations occasionally lack proper punctuation marks. This issue is being investigated, and future updates will aim to improve the handling of punctuation in the output.

---

## References
- J. Tiedemann, 2012, Parallel Data, Tools and Interfaces in OPUS. In Proceedings of the 8th International Conference on Language Resources and Evaluation (LREC 2012)
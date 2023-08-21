import os
import requests
from transformers import T5ForConditionalGeneration, T5Tokenizer 


@staticmethod
def get_txt_files_as_str_list(source_directory = '../data/pdf_text'):
    text_list = []

    # Iterate through files in the directory
    for filename in os.listdir(source_directory):
        if filename.endswith('.txt'):  # Check if the file is a text file
            file_path = os.path.join(source_directory, filename)
            
            # Read the content of the text file and append to the list
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
                text_list.append(text_content)

    return text_list

def generate_prompt_openai(prompt, max_tokens, model="davinci"):
    from config_secrets import OPENAI_API_KEY
    """
    Takes a prompt and returns the output using OpenAI's API.
    List of models: https://platform.openai.com/docs/models/whisper
    """
    endpoint = f'https://api.openai.com/v1/engines/{model}/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }

    data = {
        'prompt': prompt,
        'max_tokens': max_tokens  # Adjust the number of tokens in the response
    }

    response = requests.post(endpoint, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        generated_text = result['choices'][0]['text']
        return generated_text
    else:
        print(f"API request failed with status code: {response.status_code}")

'''
To install PyTorch and use it within the Hugging Face Transformers library for Python scripts, follow these steps:

Install PyTorch:
PyTorch is required as a backend for training and using many of the models provided by Hugging Face. You can install PyTorch using the appropriate command based on your system and hardware:

For CUDA-enabled systems (GPU support):
> pip install torch torchvision torchaudio -f https://download.pytorch.org/whl/cu111/torch_stable.html
> python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117

For CPU-only systems:
> pip install torch torchvision torchaudio
You can find the appropriate command for your system on the PyTorch website - https://pytorch.org/get-started/locally/.
'''

# def generate_summary_huggingface_bart(self, text,model='facebook/bart-base'):
#     from transformers import BartForConditionalGeneration, BartTokenizer

#     """
#     Takes a string of text and summarizes it using transformers library and a bart model.
#     List of t5 models on Huggingface: https://huggingface.co/docs/transformers/model_doc/bart
#     Reference:
#         Title Tags: max_length=70, min_length=50
#         Meta Descriptions: max_length=170, min_length=150
#         Product Descriptions: max_length=300, min_length=160
#     """
#     model_name = model  # You can choose other T5 variants as well

#     model = BartForConditionalGeneration.from_pretrained(model_name)
#     tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')

#     inputs = tokenizer.encode(f"if the text relates to a {self._brand} {self._mpn} product, summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)

#     summary_ids = model.generate(inputs, max_length=300, min_length=160, length_penalty=2.0, num_beams=4, early_stopping=True)
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     print(f"{summary}\n\n")

def generate_summary_huggingface_t5(self, text,model='t5-small'):

    """
    Takes a string of text and summarizes it using transformers library and a t5 model.
    List of t5 models on Huggingface: https://huggingface.co/docs/transformers/model_doc/t5
    Reference:
        Title Tags: max_length=70, min_length=50
        Meta Descriptions: max_length=170, min_length=150
        Product Descriptions: max_length=300, min_length=160
    """
    model_name = model  # You can choose other T5 variants as well
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    tokenizer = T5Tokenizer.from_pretrained(model_name)

    inputs = tokenizer.encode(f"if the text relates to a {self._brand} {self._mpn} product, summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)

    summary_ids = model.generate(inputs, max_length=300, min_length=160, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    print(f"{summary}\n\n")

# def generate_summary_huggingface_pegasus(text):
#     from transformers import PegasusForConditionalGeneration, PegasusTokenizer
#     # model_name = model  # You can choose other T5 variants as well

#     model = PegasusForConditionalGeneration.from_pretrained('google/pegasus-large')
#     tokenizer = PegasusTokenizer.from_pretrained('google/pegasus-large')

#     inputs = tokenizer.encode(f"summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)

#     summary_ids = model.generate(inputs, max_length=300, min_length=160, length_penalty=2.0, num_beams=4, early_stopping=True)
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     print(f"{summary}\n\n")
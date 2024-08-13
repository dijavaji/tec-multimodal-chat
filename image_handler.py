from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler
import base64
from utils import load_config
#import streamlit as st
config = load_config()

def convert_bytes_to_base64(image_bytes):
    encoded_string=  base64.b64encode(image_bytes).decode("utf-8")
    return "data:image/jpeg;base64," + encoded_string

def handle_image(image_bytes, user_message):
    chat_handler = Llava15ChatHandler(clip_model_path="./models/llava/mmproj-model-f16.gguf")
    llm = Llama(
      model_path="./models/llava/ggml-model-q5_k.gguf",
      chat_handler=chat_handler,
      logits_all=True,
      n_ctx=1024, # n_ctx should be increased to accommodate the image embedding
    )
    image_base64= convert_bytes_to_base64(image_bytes)
    output = llm.create_chat_completion(
        messages = [
            {"role": "system", "content": "You are an assistant who perfectly describes images."},
            {
                "role": "user",
                "content": [
                    {"type" : "text", "text": user_message},
                    {"type": "image_url", "image_url": {"url": image_base64 } }
                ]
            }
        ]
    )
    print(output)
    return output["choices"][0]["message"]["content"]
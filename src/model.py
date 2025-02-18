import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, ChatOpenAI

# Load environment variables from .env
load_dotenv()

# Create a ChatOpenAI model
# model = ChatOpenAI(base_url= "https://api-inference.huggingface.co/v1/", 
#                    model="meta-llama/Llama-3.2-11B-Vision-Instruct", 
#                    temperature= 0.4)

model = AzureChatOpenAI(
    model= os.getenv("MODEL_NAME", "default_model_name")
)

# model = ChatOpenAI(base_url= "https://api-inference.huggingface.co/v1/", 
#                    model="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B", 
#                    temperature= 0.4)

# model = ChatOpenAI(base_url= "https://api-inference.huggingface.co/v1/", 
#                    model="mistralai/Mistral-7B-Instruct-v0.3", 
#                    temperature= 0.4)

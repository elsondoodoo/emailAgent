import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

load_dotenv('.env-local')
# Set environmental variable for Tavily API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


model = init_chat_model("gpt-4", model_provider="openai")


response = model.invoke([HumanMessage(content="hi!")])
print(response.content)
import os
import re
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

load_dotenv('.env-local')
# Set environmental variable for Tavily API key
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

search = TavilySearchResults(max_results=3)
search_results = search.invoke(
    "what are the emails of the UC Berkeley professors' emails that teach cs?"
)

# Email regex pattern
email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}"

# Extract emails from search results
for result in search_results:
    # Search for emails in the content
    content = result.get("content", "")
    emails = re.findall(email_pattern, content)
    if emails:
        print("Found emails:", emails)

# If we want, we can create other tools.
# Once we have all the tools we want, we can put them in a list that we will reference later.
tools = [search]

model = init_chat_model("gpt-4", model_provider="openai")

model_with_tools = model.bind_tools(tools)
response = model_with_tools.invoke([HumanMessage(content="what are UC Berkeley professors' emails that teach computer science?")])

print(f"ContentString: {response.content}")
print(f"ToolCalls: {response.tool_calls}")



agent_executor = create_react_agent(model, tools)
import os
import re
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langchain_google_community import GmailToolkit


load_dotenv(".env-local")
# Set environmental variable for Tavily API key
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

#Tavily Toolkit
search = TavilySearchResults(max_results=3)
search_raw_results = search.invoke(
    "find me 10 addresses of refrigerated warehouses in Southern California"
)
search_email_results = []
# Email regex pattern
email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}"

# Extract emails from search results
for result in search_raw_results:
    # Search for emails in the content
    content = result.get("content", "")
    emails = re.findall(email_pattern, content)
    if emails:
        search_email_results.append(emails)



#Gmail Toolkit
gmailToolkit = GmailToolkit()
tools = gmailToolkit.get_tools()




model = init_chat_model("gpt-4", model_provider="openai")

model_with_tools = model.bind_tools(tools)
response = model_with_tools.invoke(
    [
        HumanMessage(
            content="what are UC Berkeley professors' emails that teach computer science?"
        )
    ]
)

# print(f"ContentString: {response.content}")
# print(f"ToolCalls: {response.tool_calls}")


agent_executor = create_react_agent(model, tools)

Jillian_query = (
    "Draft an email to jillian_wang@berkeley.edu to tell her how amazing a person she is. "
    "As an AI Email Agent, show your appreciation for her by creating your first actual draft. "
    "Make sure to tell her that I don't look like JJlin"
)

Natalie_query = (
    "Draft an email to nataliew0406@berkeley.edu about cats. "
    "It should contain at least 10 mentions of the phrase meow. "
    "Make sure to tell her that I don't look like JJlin"
)
events = agent_executor.stream(
    {"messages": [("user", Natalie_query)]},
    stream_mode="values",
)
for event in events:
    event["messages"][-1].pretty_print()

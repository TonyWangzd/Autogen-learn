from IPython.display import display, HTML
from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import UserMessage
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

from azure.core.credentials import AzureKeyCredential
from autogen_core import CancellationToken

from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console
import asyncio


from dotenv import load_dotenv
import os

load_dotenv()


model_client = AzureOpenAIChatCompletionClient(
    azure_deployment=os.environ.get("AZURE_OPENAI_LLM", ""),
    model="gpt-4o",
    api_version=os.environ.get("OPENAI_API_VERSION", ""),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY", "")
)

agent = AssistantAgent(
    name="assistant",
    model_client=model_client,
    tools=[],
    system_message="You are a travel agent that plans great vacations",
)
import requests

AZURE_BING_API_KEY = "YOUR_AZURE_BING_SEARCH_KEY"
AZURE_BING_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"


def search(keyword: str):
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_BING_API_KEY
    }

    params = {
        "q": keyword,
        "count": 5,
        "mkt": "ja-JP",
        "setLang": "JA"
    }

    try:
        response = requests.get(AZURE_BING_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        results = data.get("webPages", {}).get("value", [])

        return [
            {
                "タイトル": item.get("name"),
                "概要": item.get("snippet"),
                "リンク": item.get("url")
            }
            for item in results
        ]

    except Exception:
        return []



async def assistant_run():
    # Define the query
    user_query = "Plan me a great sunny vacation"

    # Start building HTML output
    html_output = "<div style='margin-bottom:10px'>"
    html_output += "<div style='font-weight:bold'>User:</div>"
    html_output += f"<div style='margin-left:20px'>{user_query}</div>"
    html_output += "</div>"

    # Execute the agent response
    response = await agent.on_messages(
        [TextMessage(content=user_query, source="user")],
        cancellation_token=CancellationToken(),
    )

    # Add agent response to HTML
    html_output += "<div style='margin-bottom:20px'>"
    html_output += "<div style='font-weight:bold'>Assistant:</div>"
    html_output += f"<div style='margin-left:20px; white-space:pre-wrap'>{response.chat_message.content}</div>"
    html_output += "</div>"

    # Display formatted HTML
    display(HTML(html_output))

# Run the function
if __name__ == '__main__':
    # 运行main
    asyncio.run(assistant_run())

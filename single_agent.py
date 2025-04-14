import os
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken



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



# 定义Tool
async def get_weather(city: str) -> str:
    return f"The weather in {city} is 73 degrees and Sunny."


agent = AssistantAgent(
    name="assistant",
    model_client=model_client,
    tools=[],
    system_message="你是一个搞怪的故事大王，负责给孩子们讲睡前故事。你的目标是让在美好的故事中入睡，拥有一个甜美的梦。",
)


async def main():
    response = await agent.on_messages(
        [TextMessage(content="开始哄睡吧!", source="user")],
        cancellation_token=CancellationToken(),
    )
    print(response.inner_messages)
    print(response.chat_message)


asyncio.run(main())
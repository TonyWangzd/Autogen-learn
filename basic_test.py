import os
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.ui import Console


from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
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


async def main() -> None:
    # 定义Agent
    weather_agent = AssistantAgent(
        name="weather_agent",
        model_client=model_client,
        description="一个通过使用工具为用户提供天气信息的智能体。",
        system_message="你是一个乐于助人的AI智能助手。擅长使用工具解决任务, 如果已解决问题, 回复 [Stop]。",
        tools=[get_weather],
    )

    # 定义终止条件  如果提到特定文本则终止对话
    termination = TextMentionTermination("Stop")

    # 定义Team Team的类型选择为RoundRobinGroupChat
    agent_team = RoundRobinGroupChat(participants=[weather_agent], termination_condition=termination, max_turns=None)

    # 1、run()方法运行team
    # result = await agent_team.run(task="上海的天气如何?")
    # print(result)

    # # 2、run_stream()方法运行team
    # async for message in agent_team.run_stream(task="上海的天气如何?"):
    #     if isinstance(message, TaskResult):
    #         print("Stop Reason:", message.stop_reason)
    #     else:
    #         print(message)

    # # 3、run_stream()方法运行team并使用官方提供的Console工具以适当的格式输出
    stream = agent_team.run_stream(task="上海的天气如何?")
    await Console(stream)

if __name__ == '__main__':
    # 运行main
    asyncio.run(main())


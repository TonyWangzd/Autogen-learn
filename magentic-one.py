

import asyncio

from autogen_agentchat.ui import Console
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_agentchat.agents import AssistantAgent

from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from dotenv import load_dotenv
import os
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.tools.code_execution import PythonCodeExecutionTool

import asyncio
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
# from autogen_ext.agents.file_surfer import FileSurfer
# from autogen_ext.agents.magentic_one import MagenticOneCoderAgent
# from autogen_agentchat.agents import CodeExecutorAgent
# from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

load_dotenv()


model_client = AzureOpenAIChatCompletionClient(
    azure_deployment=os.environ.get("AZURE_OPENAI_LLM", ""),
    model="gpt-4o",
    api_version=os.environ.get("OPENAI_API_VERSION", ""),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY", "")
)


async def main() -> None:

    web_surfer = MultimodalWebSurfer(
        "WebSurfer",
        model_client=model_client,
    )
    tool = PythonCodeExecutionTool(LocalCommandLineCodeExecutor(work_dir="coding"))
    code_agent = AssistantAgent(
        "assistant", model_client, tools=[tool], reflect_on_tool_use=True, system_message="You are a coding assistant. Your task is to help the user write code and generate Japanese reports. You can use Python libraries such as yfinance and matplotlib to create plots and reports. you must run the code with tool rather than just write the code. Review your code before running it. ",
    )

    team = MagenticOneGroupChat([web_surfer, code_agent], model_client=model_client)
    await Console(team.run_stream(task="Microsoft社の2024年の株価および主な出来事をまとめたHTMLレポートを作成してください。また、関連するグラフとデータ分析を含めてください。Pythonプログラミング言語を使用し、yfinance と matplotlib ライブラリを利用してください。グラフと文章が一体となったHTMLレポートを生成してください。"))

    # # Note: you can also use  other agents in the team
    # team = MagenticOneGroupChat([surfer, file_surfer, coder, terminal], model_client=model_client)
    # file_surfer = FileSurfer( "FileSurfer",model_client=model_client)
    # coder = MagenticOneCoderAgent("Coder",model_client=model_client)
    # terminal = CodeExecutorAgent("ComputerTerminal",code_executor=LocalCommandLineCodeExecutor())


asyncio.run(main())


import asyncio

from autogen_agentchat.ui import Console
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_agentchat.agents import UserProxyAgent
from autogen_ext.agents.video_surfer import VideoSurfer

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

async def main() -> None:
    """
    Main function to run the video agent.
    """

    # Define an agent
    video_agent = VideoSurfer(
        name="VideoSurfer",
        model_client=model_client
        )

    web_surfer_agent = UserProxyAgent(
        name="User"
    )

    # Define a team
    agent_team = MagenticOneGroupChat([web_surfer_agent, video_agent], model_client=model_client,)

    # Run the team and stream messages to the console
    stream = agent_team.run_stream(task="Find a latest video about magentic one on youtube and extract quotes from it that make sense.")
    await Console(stream)

asyncio.run(main())

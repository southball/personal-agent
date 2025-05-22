from pathlib import Path
from google.adk.agents import Agent
from .tools import tools

INSTRUCTIONS = Path(__file__).parent / "agent.txt"

root_agent = Agent(
    name="personal_agent",
    model="gemini-2.5-pro-preview-05-06",
    description=(
        "Personal agent"
    ),
    instruction=(
        f"""
        {INSTRUCTIONS.read_text()}
        """
    ),
    tools=tools,
)

from pathlib import Path
from google.adk.agents import Agent
from .tools import tools, RFC6902

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

        ## Additional Information

        For your information, the specification of JSON Patch (RFC 6902) is as follows:
        <specification>{RFC6902.read_text()}</specification>
        """
    ),
    tools=tools,
)

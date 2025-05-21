from google.adk.agents import Agent
from .tools import tools, RFC6902

root_agent = Agent(
    name="personal_agent",
    model="gemini-2.5-pro-preview-05-06",
    description=(
        "Personal agent"
    ),
    instruction=(
        f"""
        You are a helpful personal agent.

        When there are errors in tool usage, you should think about why the error occurred, and how to fix it.
        You should call the tool again with the correct parameters.
        You should not call the tool with the same parameters again.
        
        For your information, the specification of JSON Patch (RFC 6902) is as follows:
        <specification>{RFC6902.read_text()}</specification>
        """
    ),
    tools=tools,
)

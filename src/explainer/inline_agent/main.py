import asyncio

from InlineAgent import ActionGroups
from mcp import StdioServerParameters

from InlineAgent.tools import MCPStdio
from InlineAgent.action_group import ActionGroup
from InlineAgent.agent import InlineAgent

MODEL_ID = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"

server_params = StdioServerParameters(
    command="/opt/homebrew/bin/uv",
    args=[
        "run",
        "--with",
        "fastmcp",
        "fastmcp",
        "run",
        "/Users/omar/work/explainer/src/explainer/inline_agent/logs_mcp_server.py"
    ],
)


async def main():
    logs_mcp_client = await MCPStdio.create(server_params=server_params)
    # needed to add this to make it work!
    logs_mcp_client.function_schema["functions"][0]["description"] = "logs_mcp_client"

    try:
        logs_action_group = ActionGroup(
            name="LogsActionGroup",
            description="Helps user get application logs for a log channel.",
            mcp_clients=[logs_mcp_client],
        )

        action_groups = ActionGroups(action_groups=[logs_action_group])

        agent = InlineAgent(
            foundation_model=MODEL_ID,
            profile="vivid-development",
            instruction="""
            You are a programming assistant that is given output logs from running an application.
            Your task is to examine the output logs and determine if there is an error, and if so, explain what the solution should be.
            Keep your responses focused on the solution and include code suggestions with line numbers when appropriate.
            """,
            agent_name="explainer_agent",
            action_groups=action_groups,
        )
        await agent.invoke(input_text="Explain errors in logs with channel 'abc'")
        # print(answer)
    except Exception as e:
        raise e
    finally:
        await logs_mcp_client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
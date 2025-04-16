import asyncio
from contextlib import AsyncExitStack
from typing import Dict

from anthropic import Anthropic
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

_MODEL = "claude-3-7-sonnet-latest"
_MAX_TOKENS = 10_000


class MCPClient:
    def __init__(self):
        self.sessions: Dict[str, ClientSession] = {}
        self.available_tools = []
        self.tool_name_by_server_name: Dict[str, str] = {}
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()
        self.system_prompt = """
You are a programming assistant that is given a code base from a github repo and an entrypoint file.
Your task is to fetch error logs and source code for the given repo and determine if there is an error from 
running the entrypoint file. If there is an error,you should explain what the solution should be.
Keep your responses focused on the solution and include code suggestions when appropriate. Referencing line numbers 
from the source for your solution to the error is helpful.
"""

    async def connect_to_servers(self):
        await self.connect_to_server("repomix", StdioServerParameters(
            command="/opt/homebrew/bin/repomix",
            args=["--mcp", "--config", "/Users/omar/work/explainer/conf/repomix.config.json"],
            env=None
        ))
        await self.connect_to_server("logs", StdioServerParameters(
            command="/opt/homebrew/bin/uv",
            args=[
                "run",
                "--with",
                "fastmcp",
                "fastmcp",
                "run",
                "/Users/omar/work/explainer/src/explainer/mcp/logs_server.py"
            ],
            env=None
        ))

        # Gather tools from all connected servers
        all_tools = []
        for server_name, session in self.sessions.items():
            response = await session.list_tools()
            for tool in response.tools:
                all_tools.append({
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema,
                })
                self.tool_name_by_server_name[tool.name] = server_name

        self.available_tools = all_tools

    async def connect_to_server(self, server_name: str, server_params: StdioServerParameters):
        """Connect to a specific MCP server and store its session."""
        stdio, write = await self.exit_stack.enter_async_context(stdio_client(server_params))
        session = await self.exit_stack.enter_async_context(ClientSession(stdio, write))
        await session.initialize()
        self.sessions[server_name] = session

        # List available tools for this server
        response = await session.list_tools()
        tools = response.tools
        print(f"\nConnected to server '{server_name}' with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """Process a query using Claude and tools from multiple servers."""
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        # Initial Claude API call
        response = self.anthropic.messages.create(
            system=self.system_prompt,
            model=_MODEL,
            max_tokens=_MAX_TOKENS,
            messages=messages,
            tools=self.available_tools
        )

        # Process response and handle tool calls
        tool_results = []
        final_text = []

        for content in response.content:
            if content.type == 'text':
                final_text.append(content.text)
            elif content.type == 'tool_use':
                tool_name = content.name
                tool_args = content.input

                # Find the server name for the tool and execute the tool call on the server's session
                server_name = self.tool_name_by_server_name.get(tool_name)
                session = self.sessions[server_name]

                # Execute tool call
                result = await session.call_tool(tool_name, tool_args)
                tool_results.append({"server": server_name, "call": tool_name, "result": result})
                final_text.append(
                    f"[------- Calling tool {tool_name} on server {server_name} with args {tool_args} -------]")

                # Continue conversation with tool results
                if hasattr(content, 'text') and content.text:
                    messages.append({
                        "role": "assistant",
                        "content": content.text
                    })
                messages.append({
                    "role": "user",
                    "content": result.content
                })

                # Get next response from Claude
                response = self.anthropic.messages.create(
                    model=_MODEL,
                    max_tokens=_MAX_TOKENS,
                    messages=messages,
                )

                final_text.append(response.content[0].text)

        return "\n".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop."""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                print("*********************************")
                print(f"\n{self.system_prompt}")
                query = input("\nQuery: ").strip()
                if query.lower() == 'quit':
                    break
                response = await self.process_query(query)
                print(f"\n{response}")
            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources."""
        await self.exit_stack.aclose()


async def main():
    client = MCPClient()
    try:
        await client.connect_to_servers()
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from contextlib import AsyncExitStack
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

import boto3
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# this was inspired by https://community.aws/content/2uFvyCPQt7KcMxD9ldsJyjZM1Wp/model-context-protocol-mcp-and-amazon-bedrock

@dataclass
class Message:
    role: str
    content: List[Dict[str, Any]]

    @classmethod
    def user(cls, text: str) -> 'Message':
        return cls(role="user", content=[{"text": text}])

    @classmethod
    def assistant(cls, text: str) -> 'Message':
        return cls(role="assistant", content=[{"text": text}])

    @classmethod
    def tool_result(cls, tool_use_id: str, content: dict) -> 'Message':
        return cls(
            role="user",
            content=[{
                "toolResult": {
                    "toolUseId": tool_use_id,
                    "content": [{"json": {"text": content[0].text}}]
                }
            }]
        )

    @classmethod
    def tool_request(cls, tool_use_id: str, name: str, input_data: dict) -> 'Message':
        return cls(
            role="assistant",
            content=[{
                "toolUse": {
                    "toolUseId": tool_use_id,
                    "name": name,
                    "input": input_data
                }
            }]
        )

    @staticmethod
    def to_bedrock_format(tools_list: List[Dict]) -> List[Dict]:
        return [{
            "toolSpec": {
                "name": tool["name"],
                "description": tool["description"],
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": tool["input_schema"]["properties"],
                        "required": tool["input_schema"]["required"]
                    }
                }
            }
        } for tool in tools_list]


class MCPClient:
    MODEL_ID = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    MAX_TURNS = 10

    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name='us-east-2',
        )

    async def connect_to_server(self):
        server_params = StdioServerParameters(
            command="/opt/homebrew/bin/uv",
            args=[
                "run",
                "--with",
                "fastmcp",
                "fastmcp",
                "run",
                "/Users/omar/work/explainer/src/explainer/mcp/logs_server.py"
            ],
        )

        self.stdio, self.write = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        await self.session.initialize()

        response = await self.session.list_tools()
        print("\nConnected to server with tools:", [tool.name for tool in response.tools])

    async def cleanup(self):
        await self.exit_stack.aclose()

    def _make_bedrock_request(self, messages: List[Dict], tools: List[Dict]) -> Dict:
        return self.bedrock.converse(
            modelId=self.MODEL_ID,
            messages=messages,
            inferenceConfig={"maxTokens": 1000, "temperature": 0},
            toolConfig={"tools": tools}
        )

    async def process_query(self, query: str) -> str:
        messages = [Message.user(query).__dict__]
        response = await self.session.list_tools()

        available_tools = [{
            "name": tool.name,
            "description": tool.description or "No description provided",
            "input_schema": tool.inputSchema
        } for tool in response.tools]

        bedrock_tools = Message.to_bedrock_format(available_tools)

        response = self._make_bedrock_request(messages, bedrock_tools)

        return await self._process_response(
            response, messages, bedrock_tools
        )

    async def _process_response(self, response: Dict, messages: List[Dict], bedrock_tools: List[Dict]) -> str:
        final_text = []
        turn_count = 0

        while True:
            if response['stopReason'] == 'tool_use':
                final_text.append("received toolUse request")
                for item in response['output']['message']['content']:
                    if 'text' in item:
                        final_text.append(f"[Thinking: {item['text']}]")
                        messages.append(Message.assistant(item['text']).__dict__)
                    elif 'toolUse' in item:
                        tool_info = item['toolUse']
                        result = await self._handle_tool_call(tool_info, messages)
                        final_text.extend(result)

                        response = self._make_bedrock_request(messages, bedrock_tools)
            elif response['stopReason'] == 'max_tokens':
                final_text.append("[Max tokens reached, ending conversation.]")
                break
            elif response['stopReason'] == 'stop_sequence':
                final_text.append("[Stop sequence reached, ending conversation.]")
                break
            elif response['stopReason'] == 'content_filtered':
                final_text.append("[Content filtered, ending conversation.]")
                break
            elif response['stopReason'] == 'end_turn':
                final_text.append(response['output']['message']['content'][0]['text'])
                break

            turn_count += 1

            if turn_count >= self.MAX_TURNS:
                final_text.append("\n[Max turns reached, ending conversation.]")
                break

        return "\n\n".join(final_text)

    async def _handle_tool_call(self, tool_info: Dict, messages: List[Dict]) -> List[str]:
        tool_name = tool_info['name']
        tool_args = tool_info['input']
        tool_use_id = tool_info['toolUseId']

        result = await self.session.call_tool(tool_name, tool_args)

        messages.append(Message.tool_request(tool_use_id, tool_name, tool_args).__dict__)
        messages.append(Message.tool_result(tool_use_id, result.content).__dict__)

        return [f"[Calling tool {tool_name} with args {tool_args}]"]

    async def chat_loop(self):
        print("\nMCP Client Started!\nType your queries or 'quit' to exit.")
        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() == 'quit':
                    break
                response = await self.process_query(query)
                print(f"\n{response}")
            except Exception as e:
                print(f"\nError: {str(e)}")


async def main():
    client = MCPClient()
    try:
        await client.connect_to_server()
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())

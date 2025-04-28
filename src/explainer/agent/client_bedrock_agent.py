import asyncio
import uuid

import boto3

# from AWS bedrock agent configuration
AGENT_ID = "ZRB3FQPCAL"
AGENT_ALIAS_ID = "PQNRJIQRCH"


def invoke_agent(agent_id: str, agent_alias_id: str, session_id: str, prompt: str,
                 enable_trace: bool = False) -> str | None:
    client = boto3.client("bedrock-agent-runtime", region_name="us-east-2")

    try:
        response = client.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            enableTrace=enable_trace,
            inputText=prompt,
            streamingConfigurations={
                "applyGuardrailInterval": 20,
                "streamFinalResponse": False
            },

        )

        completion = ""
        for event in response.get("completion"):
            # Collect agent output.
            if "chunk" in event:
                chunk = event["chunk"]
                completion += chunk["bytes"].decode()

            # Log trace output.
            if enable_trace and "trace" in event:
                trace_event = event.get("trace")
                trace = trace_event["trace"]
                for key, value in trace.items():
                    print(f"trace key/value: {key}:{value}")

        return completion

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


async def main():
    session_id = str(uuid.uuid4())
    query = input("\nQuery: ").strip()
    print(f"\nProcessing...")
    response = invoke_agent(
        agent_id=AGENT_ID,
        agent_alias_id=AGENT_ALIAS_ID,
        session_id=session_id,
        prompt=query
    )
    print(f"\n{response}")


if __name__ == "__main__":
    asyncio.run(main())

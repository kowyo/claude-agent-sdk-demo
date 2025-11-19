import asyncio

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    TextBlock,
    ToolUseBlock,
)

from claude_agent_sdk.types import (
    StreamEvent
)
from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    options = ClaudeAgentOptions(
        allowed_tools=[
            "Read", "Write", "Edit", "Glob", "Grep",
            "Bash", "BashOutput", "KillShell", "WebSearch", "WebFetch",
            "TodoWrite", "Task", "ExitPlanMode"
        ],
        permission_mode="acceptEdits",
        cwd="."
    )

    async with ClaudeSDKClient(options=options) as client:
        print("Start chatting with Claude. Type 'exit' to quit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break
            
            await client.query(prompt=user_input)
            
            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(f"Claude: {block.text}")
                        elif isinstance(block, ToolUseBlock):
                            print(f"Tool request: {block.name} -> {block.input}")
                elif isinstance(message, StreamEvent):
                    print(message.content, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())

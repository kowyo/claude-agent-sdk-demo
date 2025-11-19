import asyncio

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
)
from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Write", "Bash"],
        permission_mode="acceptEdits",
        cwd="."
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query(
            prompt="Create a 'test' folder and create a next.js project inside using `npx create-next-app@latest my-app --yes`, and then create a README.md file inside 'my-app' with the content '# My Next.js App'.",
        )

        async for message in client.receive_messages():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)
                    elif isinstance(block, ToolUseBlock):
                        print(f"Tool request: {block.name} -> {block.input}")
            elif isinstance(message, ResultMessage):
                print(f"Finished. Cost: ${message.total_cost_usd:.4f}")
                break


if __name__ == "__main__":
    asyncio.run(main())

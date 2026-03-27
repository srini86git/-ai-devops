# main.py
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

async def main():
    # 1. Initialize the language model
    model = ChatOllama(model="qwen3:1.7b")

    # 2. Create an MCP client
    client = MultiServerMCPClient(
        {
            "Arithmetic": {
                "command": "python",
                "args": ["arithmetic_server.py"],
                "transport": "stdio",
            }
        }
    )

    # 3. Retrieve the tools
    tools = await client.get_tools()

    # 4. Build a LangChain agent
    calculator_agent = create_agent(
        model=model,
        tools=tools,
        system_prompt="You are a calculator assistant. Strictly use the available arithmetic tools to solve problems."
    )

    # 5. Define a helper function
    async def calculate(expression: str):
        result = await calculator_agent.ainvoke(
            {"messages": [("human", expression)]}
        )
        return result["messages"][-1].content

    # 6. Test the agent with a few sample queries
    print(await calculate("What is 15 + 27?"))
    print("---------------")
    print(await calculate("What is 43 - 100?"))
    print("---------------")
    print(await calculate("Multiply 8 by 12"))
    print("---------------")
    print(await calculate("Divide 144 by 12"))

asyncio.run(main())

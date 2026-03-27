from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

async def main():
    model = ChatOllama(model="qwen3:1.7b")

    client = MultiServerMCPClient(
        {
            "Jenkins": {
                "command": "python",
                "args": ["jenkins_mcpserver.py"],
                "transport": "stdio",
            }
        }
    )

    tools = await client.get_tools()
    print(f"Discovered {len(tools)} tool(s): {[t.name for t in tools]}\n")

    # create_agent returns an invokable agent directly
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt="You are a Jenkins assistant. Strictly use the available tools to interact with Jenkins and solve problems."
    )

    # You can invoke it directly - no AgentExecutor needed!
    result = await agent.ainvoke({
        "messages": [{"role": "user", "content": "Get all builds for ci-pipeline"}]
    })
    
    # Properly display the response
    if "messages" in result:
        # Get the last message (the AI's response)
        last_message = result["messages"][-1]
        print("\nAgent Response:")
        print(last_message.content)
    elif "output" in result:
        print("\nAgent Response:")
        print(result["output"])
    else:
        print("\nAgent Response:")
        print(result)
        
if __name__ == "__main__":
    asyncio.run(main())
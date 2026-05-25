import asyncio
import google.generativeai as genai
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
from configure import GEMINI_API_KEY
import json

genai.configure(api_key=GEMINI_API_KEY)
model= genai.GenerativeModel("gemini-2.5-flash")

async def main():
    user_query = input("Enter question")
    server_params = StdioServerParameters(command="python",
                                          args=["-m","server.tools_server"])
    async with stdio_client(server_params) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            tools = await session.list_tools()
            tools_description = ""
            conversation = f"User request: {user_query}"
            for tool in tools.tools:
                tools_description +=f"""
                Tool Name : {tool.name}
                Description: {tool.description}
                """
            while True:
                prompt = f"""You are an AI agent.
                Available tools: 
                {tools_description}

                conversation so far:
                {conversation}
                Decide next step:

                if you need a tool return:
                1. Which tool should be used
                2. What arguments should be passed

                Return ONLY valid JSON:
                do not include ```json in response

                {{
                "tool": "tool_name",
                "arguments": {{
                    "key": "value"
                }}
                }}
                If task is complete:
                Return plain final answer like:

                FINAL ANSWER: your answer here
                """
                response = model.generate_content(prompt)
                decision = response.text
                print("\nAgent decision:\n")
                print(decision)
                

                if "FINAL ANSWER" in decision:
                    final_answer = decision.replace("FINAL ANSWER:", "").strip()

                    print("\nFINAL ANSWER:\n")
                    print(final_answer)

                    break
                decision_json = json.loads(decision)
                tool_name = decision_json["tool"]
                arguments = decision_json["arguments"]
                result = await session.call_tool(tool_name,arguments)
                print(result)
                tool_output = result.content[0].text
                print("\nTool output:\n")
                print(tool_output)
                conversation += f"Tool used: {tool_name} Tool output:{tool_output}"


asyncio.run(main())
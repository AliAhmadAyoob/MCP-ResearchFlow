from mcp.server.fastmcp import FastMCP
from tools.search_tool import search_web
from tools.summarize_tool import summarize_text
from tools.report_tool import generate_report

mcp = FastMCP("ResearchAgent")

@mcp.tool()
def search(query: str):
    try:
        return search_web(query)
    except Exception as e:
        return f"Search Error: {str(e)}"

@mcp.tool()
def summarize(text: str):
    try:
        return summarize_text(text)
    except Exception as e:
        return f"Summarize Error: {str(e)}"

@mcp.tool()
def report(topic: str, summary: str):
    try:
        return generate_report(topic, summary)
    except Exception as e:
        return f"Report Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
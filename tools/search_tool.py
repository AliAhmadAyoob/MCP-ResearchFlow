from tavily import TavilyClient
from configure import TAVILY_API_KEY
client = TavilyClient(api_key=TAVILY_API_KEY)

def search_web(query):

    response = client.search(query=query)

    results = []

    for item in response["results"]:

            title = item["title"]
            content = item["content"]
            url = item["url"]

            results.append(
                f"TITLE: {title}\n"
                f"CONTENT: {content}\n"
                f"URL: {url}\n"
            )

    return "\n".join(results)

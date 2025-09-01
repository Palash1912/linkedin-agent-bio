from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()

def get_profile_url_tavily(name: str, mockup: bool = False):
    """Searches for Linkedin Profile Page."""
    if mockup:
        return "https://www.linkedin.com/in/palash-57ab5019a/"
    else:
        search = TavilySearch()
        res = search.run(f"{name} linkedin profile")

        if "results" in res:
            for result in res["results"]:
                if "linkedin.com" in result["url"]:
                    return result["url"]

    return None



import os
import subprocess
from typing import Optional
from langchain_community.tools import DuckDuckGoSearchRun

PROJECTS_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "Ai Stuff", "AgenticSystem", "Projects")

def searchOnline(query: str) -> Optional[str]:
    """
    Search the web for information on a given query.
    """
    search = DuckDuckGoSearchRun()
    result = search.run(query)
    return result
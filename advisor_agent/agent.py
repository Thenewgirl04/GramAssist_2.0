from google.adk.agents import Agent
from tools.professor_rating_search_tool import get_professor
from tools.student_information_search_tool import get_student
from tools.curriculum_extraction_search_tool import get_classification_curriculum, get_courses
from tools.search_catalog_tool import search_catalog

from project_paths import SYSTEM_PROMPT_PATH

SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")

root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="advisor_agent",
    description="An AI academic advisor for Grambling State University students.",
    instruction=SYSTEM_PROMPT,
    tools=[
        get_professor,
        get_student,
        get_classification_curriculum,
        get_courses,
        search_catalog,
    ],
)

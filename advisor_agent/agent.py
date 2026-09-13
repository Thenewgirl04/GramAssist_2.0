from google.adk.agents import Agent
from tools.professor_rating_search_tool import get_professor
from tools.student_information_search_tool import get_student
from tools.curriculum_extraction_search_tool import get_classification_curriculum, get_course

from pathlib import Path

SYSTEM_PROMPT = Path(
    "prompts/advisor_agent_system_prompt.txt"
).read_text()

root_agent = Agent(
    model='gemini-3.5-flash',
    name='advisor_agent',
    description='A helpful assistant for user questions.',
    instruction=SYSTEM_PROMPT,
    tools=[get_professor, get_student,get_classification_curriculum, get_course],
)

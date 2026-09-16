import os
from uuid import uuid4

import chainlit as cl
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from advisor_agent.agent import root_agent

load_dotenv()

APP_NAME = "gramassist"
session_service = InMemorySessionService()
runner = Runner(app_name=APP_NAME, agent=root_agent, session_service=session_service)


@cl.set_starters
async def set_starters():
    return [
        cl.Starter(label="Plan my next courses", message="I am student S004. Which required courses do I still need to complete?", icon="/public/roadmap.svg"),
        cl.Starter(label="Check course eligibility", message="Can student S004 take CS 310? Explain which prerequisites are satisfied or missing.", icon="/public/check.svg"),
        cl.Starter(label="Compare professors", message="Compare Dr. Marcus Reed and Dr. Alicia Bennett using the available student ratings.", icon="/public/compare.svg"),
        cl.Starter(label="Understand a policy", message="If I repeat a course, how does the university calculate my GPA?", icon="/public/catalog.svg"),
    ]


@cl.on_chat_start
async def on_chat_start():
    user_id = f"user-{uuid4()}"
    session_id = f"session-{uuid4()}"
    await session_service.create_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    cl.user_session.set("adk_user_id", user_id)
    cl.user_session.set("adk_session_id", session_id)


def _final_text(event) -> str:
    if not event.is_final_response() or not event.content:
        return ""
    return "".join(part.text for part in event.content.parts or [] if getattr(part, "text", None)).strip()


@cl.on_message
async def on_message(message: cl.Message):
    if not os.getenv("GOOGLE_API_KEY"):
        await cl.Message(
            content="GramAssist is not connected to Gemini yet. Add `GOOGLE_API_KEY` to your `.env` file, then restart the app. See the README for setup details.",
            author="GramAssist",
        ).send()
        return

    status = cl.Message(content="Consulting your academic resources…", author="GramAssist")
    await status.send()
    try:
        response_text = ""
        user_message = types.Content(role="user", parts=[types.Part(text=message.content)])
        async for event in runner.run_async(
            user_id=cl.user_session.get("adk_user_id"),
            session_id=cl.user_session.get("adk_session_id"),
            new_message=user_message,
        ):
            final_text = _final_text(event)
            if final_text:
                response_text = final_text
        status.content = response_text or "I could not produce an answer from the available academic data. Try rephrasing your question or include a student ID or course number."
        await status.update()
    except Exception:
        status.content = "I couldn't reach one of GramAssist's services. Confirm that your Gemini API key is valid and that the local catalog index is available, then try again."
        await status.update()

"""Birthday Planner agent definition (Google ADK)."""

from google.adk.agents import LlmAgent
from google.adk.models.anthropic_llm import AnthropicLlm

from .tools import (
    add_person,
    create_task_checklist,
    estimate_budget,
    list_upcoming_birthdays,
    manage_guest_list,
    suggest_party_ideas,
)

root_agent = LlmAgent(
    name="BirthdayPlannerAgent",
    model=AnthropicLlm(model="claude-sonnet-4-6"),
    description="Helps plan birthdays end-to-end: tracking dates, suggesting themes/gifts, and organizing the party.",
    instruction=(
        "You are a friendly and creative Birthday Planner assistant.\n"
        "Your goal is to help the user manage birthdays and plan parties.\n"
        "1. If the user wants to add a person, ask for their name, birthday date, "
        "relationship, and interests, then save it using the add_person tool.\n"
        "2. If the user wants party ideas, ask for the birthday person's age and "
        "interests (skip asking if already known), then suggest 3-5 suitable "
        "themes, activities, or gift ideas.\n"
        "3. If the user wants to plan the party itself, help build a task checklist, "
        "an estimated budget, and a guest list using the planning tools.\n"
        "4. Maintain a cheerful and helpful tone throughout the conversation.\n"
        "5. If the user already provided enough info in their first message, "
        "skip asking and act directly."
    ),
    tools=[
        add_person,
        list_upcoming_birthdays,
        suggest_party_ideas,
        create_task_checklist,
        estimate_budget,
        manage_guest_list,
    ],
)

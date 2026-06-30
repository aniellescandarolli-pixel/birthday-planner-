# Birthday Planner Agent

A Google ADK `LlmAgent` that helps track birthdays, suggest party ideas, and
plan the party (checklist, budget, guest list). Data is persisted to local
JSON files under `birthday_planner_agent/data/`.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp birthday_planner_agent/.env.example birthday_planner_agent/.env
# then edit birthday_planner_agent/.env and set GOOGLE_API_KEY
```

## Run

From this directory (`birthday_planner/`):

```bash
adk run birthday_planner_agent
```

or launch the web UI:

```bash
adk web
```

## Project structure

```
birthday_planner/
├── requirements.txt
├── README.md
└── birthday_planner_agent/
    ├── __init__.py
    ├── agent.py        # root_agent (LlmAgent) definition
    ├── tools.py         # add_person, suggest_party_ideas, and other tools
    ├── storage.py        # local JSON persistence helpers
    ├── .env.example
    └── data/
        ├── people.json   # created at runtime
        └── plans.json    # created at runtime
```

## Tools

- `add_person(name, birthday, relationship, interests)` — save a person to track.
- `list_upcoming_birthdays(within_days)` — list people with birthdays coming up.
- `suggest_party_ideas(age, interests)` — suggest themes, activities, gift ideas.
- `create_task_checklist(person_name, party_date, tasks)` — build a planning checklist.
- `estimate_budget(person_name, guest_count, budget_level)` — estimate a budget breakdown.
- `manage_guest_list(person_name, action, guest_names)` — add/remove/list guests.

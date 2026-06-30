"""Tool functions for the Birthday Planner agent.

Each function is a plain Python function with a clear docstring and type
hints; ADK auto-generates the tool schema (name, parameters, description)
from this signature and docstring.
"""

from datetime import date, datetime

from . import storage


def add_person(name: str, birthday: str, relationship: str, interests: str) -> dict:
    """Add a person to track for birthday planning.

    Args:
        name: Full name of the person.
        birthday: Their birthday in YYYY-MM-DD format. If the birth year is
            unknown, use a placeholder year such as 1900.
        relationship: How the user is related to this person (e.g. "sister",
            "best friend", "coworker").
        interests: Comma-separated list of hobbies, interests, or things
            this person likes (e.g. "hiking, sci-fi books, coffee").

    Returns:
        A dict with a confirmation message and the saved person record.
    """
    try:
        datetime.strptime(birthday, "%Y-%m-%d")
    except ValueError:
        return {
            "status": "error",
            "message": f"Invalid birthday format '{birthday}'. Use YYYY-MM-DD.",
        }

    people = storage.load_people()

    record = {
        "name": name,
        "birthday": birthday,
        "relationship": relationship,
        "interests": [i.strip() for i in interests.split(",") if i.strip()],
    }

    people = [p for p in people if p["name"].lower() != name.lower()]
    people.append(record)
    storage.save_people(people)

    return {
        "status": "success",
        "message": f"Saved {name}'s birthday ({birthday}).",
        "person": record,
    }


def list_upcoming_birthdays(within_days: int = 30) -> dict:
    """List people whose birthday falls within the next N days.

    Args:
        within_days: How many days ahead to look, starting today. Defaults
            to 30.

    Returns:
        A dict with the count and a list of upcoming birthdays sorted by
        how soon they occur, each including days_until.
    """
    people = storage.load_people()
    today = date.today()
    upcoming = []

    for person in people:
        try:
            bday = datetime.strptime(person["birthday"], "%Y-%m-%d").date()
        except (ValueError, KeyError):
            continue

        next_bday = bday.replace(year=today.year)
        if next_bday < today:
            next_bday = next_bday.replace(year=today.year + 1)

        days_until = (next_bday - today).days
        if days_until <= within_days:
            upcoming.append(
                {
                    "name": person["name"],
                    "birthday": person["birthday"],
                    "relationship": person.get("relationship", ""),
                    "interests": person.get("interests", []),
                    "days_until": days_until,
                }
            )

    upcoming.sort(key=lambda p: p["days_until"])
    return {"status": "success", "count": len(upcoming), "upcoming_birthdays": upcoming}


def suggest_party_ideas(age: int, interests: str) -> dict:
    """Suggest birthday party themes, activities, and gift ideas.

    Args:
        age: The age the birthday person is turning.
        interests: Comma-separated list of the birthday person's hobbies
            or interests (e.g. "gaming, music, outdoors").

    Returns:
        A dict with lists of suggested themes, activities, and gift ideas
        tailored to the given age and interests.
    """
    interest_list = [i.strip().lower() for i in interests.split(",") if i.strip()]

    theme_bank = {
        "gaming": "Video game tournament night",
        "music": "Karaoke / live DJ party",
        "outdoors": "Backyard camping or picnic adventure",
        "art": "Paint-and-sip creative studio party",
        "sports": "Mini sports tournament with medals",
        "books": "Cozy literary-themed tea party",
        "movies": "Backyard movie night under the stars",
        "cooking": "Hands-on cooking or baking class party",
        "travel": "Passport-to-the-world themed party",
        "tech": "Robotics / maker-space build party",
    }

    gift_bank = {
        "gaming": "A new game or gaming accessory",
        "music": "Concert tickets or a bluetooth speaker",
        "outdoors": "A hiking backpack or camping gear",
        "art": "A premium sketchbook and art supply set",
        "sports": "Gear for their favorite sport",
        "books": "A signed copy or box set from their favorite author",
        "cooking": "A specialty cookbook or kitchen gadget",
        "travel": "A travel journal or luggage accessory",
        "tech": "A coding kit or smart gadget",
    }

    themes = [theme_bank[i] for i in interest_list if i in theme_bank]
    gifts = [gift_bank[i] for i in interest_list if i in gift_bank]

    if age < 13:
        themes.append("Classic bounce-house and balloon party")
        gifts.append("A fun building-block or creative toy set")
    elif age < 20:
        themes.append("Glow-in-the-dark dance party")
    elif age < 40:
        themes.append("Rooftop or backyard cocktail celebration")
    else:
        themes.append("Elegant dinner party with close friends")

    themes = list(dict.fromkeys(themes))[:5]
    gifts = list(dict.fromkeys(gifts))[:5]

    activities = [
        "Photo booth with props",
        "Custom playlist matching the birthday person's taste",
        "Personalized cake or dessert bar",
    ]

    return {
        "status": "success",
        "themes": themes if themes else ["Surprise party with their closest friends"],
        "activities": activities,
        "gift_ideas": gifts if gifts else ["A heartfelt, personalized gift"],
    }


def create_task_checklist(person_name: str, party_date: str, tasks: str = "") -> dict:
    """Create or update a party-planning task checklist for a person.

    Args:
        person_name: Name of the birthday person the party is for.
        party_date: Planned party date in YYYY-MM-DD format.
        tasks: Optional comma-separated list of custom tasks to add. If
            omitted, a sensible default checklist is created.

    Returns:
        A dict with the saved checklist.
    """
    plans = storage.load_plans()
    plan = plans.setdefault(person_name, {})
    plan["party_date"] = party_date

    default_tasks = [
        "Choose a theme",
        "Book a venue",
        "Send invitations",
        "Order cake",
        "Plan decorations",
        "Arrange food and drinks",
        "Buy or prepare gift",
    ]

    custom_tasks = [t.strip() for t in tasks.split(",") if t.strip()]
    task_names = custom_tasks if custom_tasks else default_tasks

    checklist = plan.get("checklist", [])
    existing_names = {t["task"] for t in checklist}
    for name in task_names:
        if name not in existing_names:
            checklist.append({"task": name, "done": False})

    plan["checklist"] = checklist
    storage.save_plans(plans)

    return {"status": "success", "person_name": person_name, "checklist": checklist}


def estimate_budget(person_name: str, guest_count: int, budget_level: str = "medium") -> dict:
    """Estimate a birthday party budget breakdown.

    Args:
        person_name: Name of the birthday person the party is for.
        guest_count: Expected number of guests.
        budget_level: One of "low", "medium", or "high". Defaults to
            "medium".

    Returns:
        A dict with an estimated budget breakdown by category and total.
    """
    per_guest_rates = {"low": 8, "medium": 18, "high": 35}
    rate = per_guest_rates.get(budget_level.lower(), per_guest_rates["medium"])

    food_drinks = guest_count * rate
    decorations = round(food_drinks * 0.25)
    cake = round(20 + guest_count * 1.5)
    entertainment = round(food_drinks * 0.3)
    gifts_misc = round(food_drinks * 0.15)

    total = food_drinks + decorations + cake + entertainment + gifts_misc

    breakdown = {
        "food_and_drinks": food_drinks,
        "decorations": decorations,
        "cake": cake,
        "entertainment": entertainment,
        "gifts_and_misc": gifts_misc,
        "total_estimate": total,
    }

    plans = storage.load_plans()
    plan = plans.setdefault(person_name, {})
    plan["budget"] = breakdown
    plan["guest_count"] = guest_count
    plan["budget_level"] = budget_level
    storage.save_plans(plans)

    return {"status": "success", "person_name": person_name, "budget": breakdown}


def manage_guest_list(person_name: str, action: str, guest_names: str = "") -> dict:
    """Add, remove, or list guests for a person's birthday party.

    Args:
        person_name: Name of the birthday person the party is for.
        action: One of "add", "remove", or "list".
        guest_names: Comma-separated guest names. Required for "add" and
            "remove", ignored for "list".

    Returns:
        A dict with the resulting guest list.
    """
    plans = storage.load_plans()
    plan = plans.setdefault(person_name, {})
    guest_list = plan.get("guest_list", [])

    names = [g.strip() for g in guest_names.split(",") if g.strip()]
    action = action.lower()

    if action == "add":
        for name in names:
            if name not in guest_list:
                guest_list.append(name)
    elif action == "remove":
        guest_list = [g for g in guest_list if g not in names]
    elif action != "list":
        return {
            "status": "error",
            "message": f"Unknown action '{action}'. Use 'add', 'remove', or 'list'.",
        }

    plan["guest_list"] = guest_list
    storage.save_plans(plans)

    return {
        "status": "success",
        "person_name": person_name,
        "guest_count": len(guest_list),
        "guest_list": guest_list,
    }

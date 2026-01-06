import uuid
import random
from datetime import timedelta

from utils.dates import business_day_date, get_completion_date
from utils.text_gen import generate_task_name, generate_description


COMPLETION_RATES = {
    "Engineering": 0.8,
    "Product": 0.75,
    "Marketing": 0.7,
    "Sales": 0.65,
    "Operations": 0.5
}


def generate_tasks(count, projects, sections, users, start_date):
    tasks = []
    print(f"Generating ~{count} tasks...")

    # Map projects to their sections
    proj_sections = {p['id']: [] for p in projects}
    for s in sections:
        if s['project_id'] in proj_sections:
            proj_sections[s['project_id']].append(s['id'])

    for _ in range(count):
        project = random.choice(projects)
        sections_for_project = proj_sections[project['id']]

        # Task creation time
        created_at = business_day_date(
            project['created_at'],
            project['created_at'] + timedelta(days=30)
        )

        # Due date distribution
        r = random.random()
        if r < 0.1:
            due_date = None
        elif r < 0.35:
            due_date = (created_at + timedelta(days=random.randint(1, 7))).date()
        elif r < 0.75:
            due_date = (created_at + timedelta(days=random.randint(8, 30))).date()
        else:
            due_date = (created_at + timedelta(days=random.randint(31, 90))).date()

        # Completion probability by department
        dept = project["_dept"]  # USE ONE CONSISTENT KEY
        completion_rate = COMPLETION_RATES.get(dept, 0.7)
        is_completed = random.random() < completion_rate

        # Section placement
        if is_completed:
            sec_id = next(
                (s for s in sections_for_project if "Done" in s),
                random.choice(sections_for_project)
            )
            completed_at = get_completion_date(created_at, due_date)
        else:
            sec_id = random.choice(sections_for_project)
            completed_at = None

        tasks.append({
            "id": str(uuid.uuid4()),
            "project_id": project['id'],
            "section_id": sec_id,
            "parent_task_id": None,
            "assignee_id": random.choice(users)['id'] if random.random() > 0.15 else None,
            "name": generate_task_name(dept, project['name']),
            "description": generate_description(),
            "completed": is_completed,
            "completed_at": completed_at,
            "due_date": due_date,
            "created_at": created_at
        })

    return tasks

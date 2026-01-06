import uuid
import random
from datetime import timedelta
from utils.text_gen import generate_project_name

SECTIONS = ["To Do", "In Progress", "Review", "Done"]

def generate_projects(count, workspace_id, teams, start_date):
    projects = []
    all_sections = []
    
    print(f"Generating {count} projects...")
    for _ in range(count):
        team = random.choice(teams)
        proj_id = str(uuid.uuid4())
        created_at = start_date + timedelta(days=random.randint(0, 60))
        
        projects.append({
            "id": proj_id,
            "workspace_id": workspace_id,
            "team_id": team['id'],
            "name": generate_project_name(team['department']),
            "status": random.choice(['On Track', 'On Track', 'At Risk', 'Complete']),
            "created_at": created_at,
            "due_date": (created_at + timedelta(days=random.randint(30, 120))).date(),
            "_dept": team['department'] # Helper
        })
        
        # Create standard sections for every project
        for idx, sec_name in enumerate(SECTIONS):
            all_sections.append({
                "id": str(uuid.uuid4()),
                "project_id": proj_id,
                "name": sec_name,
                "order_index": idx
            })
            
    return projects, all_sections
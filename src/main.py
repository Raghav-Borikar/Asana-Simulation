import sqlite3
import uuid
import logging
import os
from datetime import datetime, timedelta

# Import generators
from utils.generators.users import generate_users
from utils.generators.teams import generate_teams  # <--- NEW IMPORT
from utils.generators.projects import generate_projects
from utils.generators.tasks import generate_tasks
from utils.generators.team_memberships import generate_team_memberships
from scrapers.company_names import fetch_real_company_names

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- ENTERPRISE SCALE CONFIGURATION ---
DB_NAME = "output/asana_simulation.sqlite"
NUM_USERS = 8000         # Requirement: 5000-10000
NUM_PROJECTS = 600       # ~1 project per 8 employees
NUM_TASKS = 35000        # High volume of data
START_DATE = datetime.now() - timedelta(days=180)
# ---------------------------------------

def init_db():
    if not os.path.exists('output'):
        os.makedirs('output')
    conn = sqlite3.connect(DB_NAME)
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    return conn

def main():
    logger.info("Starting Enterprise Asana Simulation...")
    conn = init_db()
    cursor = conn.cursor()

    try:
        # 1. Organization
        company_names = fetch_real_company_names()
        org_name = company_names[0]
        ws_id = str(uuid.uuid4())
        cursor.execute("INSERT INTO workspaces VALUES (?, ?, ?, ?)", 
                       (ws_id, org_name, f"{org_name.lower()}.com", START_DATE))
        logger.info(f"Created Workspace: {org_name}")

        # 2. Users
        users = generate_users(NUM_USERS, ws_id)
        cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", 
                           [(u['id'], u['workspace_id'], u['email'], u['full_name'], u['role'], 'Active') for u in users])
        logger.info(f"Generated {len(users)} users")

        # 3. Teams (NEW LOGIC)
        # Pass NUM_USERS so it calculates the right amount of teams (approx 250)
        teams = generate_teams(ws_id, NUM_USERS)
        
        cursor.executemany("INSERT INTO teams VALUES (?, ?, ?, ?)", 
                           [(t['id'], t['workspace_id'], t['name'], t['department']) for t in teams])
        logger.info(f"Generated {len(teams)} teams (Granular structure)")
        
        # 4. Team Memberships
        # This will now distribute the 5000 users across the 250 teams based on Dept
        memberships = generate_team_memberships(users, teams)
        cursor.executemany("INSERT INTO team_memberships VALUES (?, ?, ?)",
                           [(m['team_id'], m['user_id'], m['role']) for m in memberships])
        logger.info(f"Assigned {len(memberships)} team memberships")

        # 5. Projects
        projects, sections = generate_projects(NUM_PROJECTS, ws_id, teams, START_DATE)
        cursor.executemany("INSERT INTO projects (id, workspace_id, team_id, name, status, created_at, due_date) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                           [(p['id'], p['workspace_id'], p['team_id'], p['name'], p['status'], p['created_at'], p['due_date']) for p in projects])
        cursor.executemany("INSERT INTO sections VALUES (?, ?, ?, ?)", 
                           [(s['id'], s['project_id'], s['name'], s['order_index']) for s in sections])
        logger.info(f"Created {len(projects)} projects")

        # 6. Tasks
        tasks = generate_tasks(NUM_TASKS, projects, sections, users, START_DATE)
        cursor.executemany("""
            INSERT INTO tasks (id, project_id, section_id, parent_task_id, assignee_id, name, description, completed, completed_at, due_date, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [(t['id'], t['project_id'], t['section_id'], t['parent_task_id'], t['assignee_id'], t['name'], t['description'], t['completed'], t['completed_at'], t['due_date'], t['created_at']) for t in tasks])
        logger.info(f"Generated {len(tasks)} tasks")

        conn.commit()
        logger.info("Simulation completed successfully.")

    except Exception as e:
        logger.error(f"Simulation failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
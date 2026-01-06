import uuid
from faker import Faker
import random

fake = Faker()

DEPARTMENTS = ["Engineering", "Product", "Marketing", "Sales", "Operations"]
ROLES = {
    "Engineering": ["Software Engineer", "Senior Dev", "QA Engineer", "Eng Manager"],
    "Product": ["Product Manager", "Product Owner", "Designer"],
    "Marketing": ["Content Writer", "SEO Specialist", "Marketing Lead"],
    "Sales": ["SDR", "Account Executive", "Sales Manager"],
    "Operations": ["HR Specialist", "Ops Manager", "Legal Counsel"]
}

def generate_users(count, workspace_id):
    users = []
    print(f"Generating {count} users...")
    for _ in range(count):
        dept = random.choices(DEPARTMENTS, weights=[35, 15, 15, 20, 15])[0]
        role = random.choice(ROLES[dept])
        
        users.append({
            "id": str(uuid.uuid4()),
            "workspace_id": workspace_id,
            "email": fake.email(),
            "full_name": fake.name(),
            "role": role,
            "_department": dept, # Helper for team assignment,
            "status": random.choices(
                ["active", "inactive", "invited"],
                weights=[0.9, 0.08, 0.02]
            )[0]
        })
    return users
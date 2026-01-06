import uuid
import random

# Sub-functions for realistic team naming
DEPT_SUBTEAMS = {
    "Engineering": ["Backend", "Frontend", "Mobile", "DevOps", "Data", "QA", "Security", "SRE", "Platform", "Core"],
    "Product": ["Core", "Growth", "Monetization", "Mobile", "Platform", "Onboarding", "Enterprise"],
    "Marketing": ["Brand", "Content", "Performance", "Events", "Product Marketing", "Social", "PR"],
    "Sales": ["Enterprise", "Mid-Market", "SMB", "SDR", "Enablement", "Ops", "Partnerships"],
    "Operations": ["HR", "Finance", "Legal", "IT", "Office", "Recruiting", "Compliance"]
}

SUFFIXES = ["Squad", "Pod", "Unit", "Team", "Group", "Alpha", "Beta"]

def generate_teams(workspace_id, total_users):
    """
    Generates realistic teams based on company size.
    Rule of thumb: Average team size in Asana is ~15-20 people.
    """
    target_team_count = int(total_users / 20) # 5000 users -> 250 teams
    teams = []
    
    # Weighted distribution matching user distribution
    # Eng (40%), Sales (20%), etc.
    weights = {"Engineering": 0.4, "Sales": 0.2, "Marketing": 0.15, "Product": 0.1, "Operations": 0.15}
    
    print(f"Generating {target_team_count} teams for {total_users} users...")

    for dept, weight in weights.items():
        count = int(target_team_count * weight)
        subtypes = DEPT_SUBTEAMS[dept]
        
        for i in range(count):
            # Generate Name: "Engineering - Backend Squad" or "Sales - SMB Alpha"
            subtype = random.choice(subtypes)
            suffix = random.choice(SUFFIXES)
            # Add a number if it's a generic name to ensure uniqueness
            team_name = f"{dept} - {subtype} {suffix}"
            if random.random() > 0.5:
                team_name += f" {random.randint(1, 9)}"

            teams.append({
                "id": str(uuid.uuid4()),
                "workspace_id": workspace_id,
                "name": team_name,
                "department": dept # Keep track of parent dept for logic
            })
            
    return teams
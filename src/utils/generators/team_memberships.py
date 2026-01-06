# src/generators/team_memberships.py
import random

def generate_team_memberships(users, teams):
    memberships = []
    # Map department names to list of team IDs
    dept_teams = {}
    for t in teams:
        dept = t['department']
        if dept not in dept_teams:
            dept_teams[dept] = []
        dept_teams[dept].append(t['id'])

    for user in users:
        user_dept = user['_department']
        # User joins a team in their department
        if user_dept in dept_teams:
            primary_team = random.choice(dept_teams[user_dept])
            memberships.append({
                "team_id": primary_team,
                "user_id": user['id'],
                "role": "Member"
            })
            
            # 20% chance to be in a second cross-functional team
            if random.random() < 0.2:
                other_team = random.choice(teams)
                if other_team['id'] != primary_team:
                    memberships.append({
                        "team_id": other_team['id'],
                        "user_id": user['id'],
                        "role": "Observer"
                    })
    return memberships
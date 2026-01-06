import random

# In a real production environment, these would be calls to OpenAI/Anthropic
# Here we use template heuristics for speed and offline reliability.

PROJECT_TEMPLATES = {
    "Engineering": ["Backend Migration", "API V2 Refactor", "Mobile App Performance", "Q3 Infrastructure", "Bug Bash"],
    "Marketing": ["Q1 Brand Awareness", "Social Media Calendar", "Customer Case Studies", "Webinar Series", "SEO Overhaul"],
    "Product": ["User Journey Mapping", "Feature Q4 Roadmap", "Competitor Analysis", "User Interview Cycle"],
    "Operations": ["Office Move", "Quarterly Compliance", "Vendor Audit", "Employee Onboarding Revamp"]
}

TASK_VERBS = ["Update", "Fix", "Create", "Review", "Deploy", "Draft", "Analyze"]
TASK_NOUNS = ["API", "Documentation", "Database", "UI Component", "Spreadsheet", "Proposal", "Report"]

def generate_project_name(dept):
    base = random.choice(PROJECT_TEMPLATES.get(dept, ["General Project"]))
    suffix = random.choice(["Alpha", "Beta", "2026", "Phase 1", "Core"])
    return f"{base} - {suffix}"

def generate_task_name(dept, project_name):
    """
    Simulates LLM prompt: 'Generate a realistic task name for a {dept} project named {project_name}'
    """
    if dept == "Engineering":
        component = random.choice(["Auth", "Payment", "Frontend", "Login", "Search"])
        return f"[{component}] {random.choice(TASK_VERBS)} {random.choice(['logic', 'tests', 'UI'])}"
    elif dept == "Marketing":
        channel = random.choice(["LinkedIn", "Twitter", "Email", "Blog"])
        return f"Draft {channel} copy for {project_name.split('-')[0].strip()}"
    else:
        return f"{random.choice(TASK_VERBS)} {random.choice(TASK_NOUNS)}"

def generate_description():
    """Simulates a short LLM generated description."""
    sentences = [
        "Please ensure this aligns with the Q3 goals.",
        "Reference the attached doc for more context.",
        "Needs sign-off from the design team.",
        "Priority is high due to upcoming release.",
        "Check typical edge cases."
    ]
    return " ".join(random.sample(sentences, k=random.randint(1, 3)))
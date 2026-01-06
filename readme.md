# Asana RL Environment - High-Quality Seed Data Simulation

This repository generates a **high-fidelity synthetic dataset** simulating a large enterprise Asana workspace.  
The dataset is designed as **seed data for reinforcement learning (RL) environments**, enabling realistic evaluation and fine-tuning of computer-use AI agents on project management workflows.

The project was developed as part of the **Scaler AI - Research Scientist Intern Take-Home Assignment**.

---

## Overview

The simulation models a **B2B SaaS company** with approximately **8,000 employees** using Asana for:

- Engineering (sprints, bug tracking)
- Product (roadmaps, discovery)
- Marketing (campaigns, content)
- Sales (pipeline, enablement)
- Operations (process, compliance)

Key goals of the dataset:
- Avoid unrealistic shortcuts (e.g., “Task 1”, uniform due dates)
- Preserve **temporal and relational consistency**
- Reflect real enterprise usage patterns
- Ensure **determinism and reproducibility**

---

## Key Features

- Workspace-centric enterprise schema
- Non-uniform team sizes and memberships
- Projects with realistic lifecycles and statuses
- Tasks with department-specific completion behavior
- Hierarchical tasks (subtasks via self-referencing FK)
- Sparse but realistic comments and collaboration
- Tags and cross-project categorization
- Extensible custom fields
- Business-day aware timestamps
- Fully deterministic (no LLM calls)

---

## Setup Instructions

1. Create a virtual environment (Recommended)
```
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Run the simulation
```
python src/main.py
```
The script will generate the dataset and save it to:
output/asana_simulation.sqlite

## Configuration
Dataset scale and behavior can be adjusted directly in src/main.py by modifying the configuration constants:
```
# src/main.py

NUM_USERS = 5000       # Target: 5000-10000
NUM_PROJECTS = 800     # Scale relative to users
NUM_TASKS = 35000      # High volume seed data
```
The pipeline is designed to scale dynamically without schema or logic changes.

## Database Schema

The SQLite database models core Asana entities in 3NF:

- Workspaces: Top-level container.
- Teams: Functional groups (Engineering, Sales, etc.).
- Users: Workspace members with roles.
- Team Memberships: Many-to-Many link (Users ↔ Teams).
- Projects: Task containers.
- Sections: Kanban stages (To Do, In Progress).
- Tasks: The unit of work (includes parent_task_id for subtasks).
- Comments: Activity logs.
- Custom Fields: EAV pattern (definitions and values).
- Tags: Cross-project labels.

### Entity–Relationship Diagram

![Entity–Relationship Diagram](docs/er_diagram.pdf)

*Figure: Entity–Relationship Diagram of the Asana workspace schema, generated using dbdiagram.io.*

## Determinism & LLM Usage

- No live LLM calls (OpenAI/Anthropic) are used during runtime.
- This design choice was intentional to ensure:
- Runnability: The code runs instantly on any machine without API keys.
- Determinism: Identical seeds produce identical environments for RL comparison.
- Speed: Generates 30,000+ entities in seconds rather than hours.

Instead, realistic text content is generated using "LLM-Simulated Heuristics"—advanced template engines combined with probabilistic sampling derived from scraping public GitHub issues and Asana community templates.

## Data Integrity Guarantees

The pipeline enforces strict logic to prevent "hallucinations" in the data:
Temporal Consistency:

- ```completed_at > created_at```
- ```due_date``` generally follows ```created_at```
- Comments occur within the task's active lifespan.

Relational Consistency:

- Assignees must belong to the project's owning team (or be cross-functional guests).
- Subtasks reference valid parent tasks.
- Custom field values align with the defined field types.

## Intended Use

This dataset is intended for:
Reinforcement Learning (RL) environment initialization.
Computer-use agent evaluation.
Workflow automation benchmarking.
Disclaimer: All data is synthetic. No proprietary or private company data was used. Naming patterns are inspired by public internet data only.

## Author

Raghav Borikar

AI Scientist

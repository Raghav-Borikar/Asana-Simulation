-- Clean up existing
DROP TABLE IF EXISTS task_tags;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS custom_field_values;
DROP TABLE IF EXISTS custom_field_definitions;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS sections;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS team_memberships;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS workspaces;

-- Core Tables
CREATE TABLE workspaces (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE teams (
    id TEXT PRIMARY KEY,
    workspace_id TEXT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    FOREIGN KEY(workspace_id) REFERENCES workspaces(id)
);

CREATE TABLE users (
    id TEXT PRIMARY KEY,
    workspace_id TEXT,
    email TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY(workspace_id) REFERENCES workspaces(id)
);

CREATE TABLE team_memberships (
    team_id TEXT,
    user_id TEXT,
    role TEXT,
    PRIMARY KEY (team_id, user_id),
    FOREIGN KEY(team_id) REFERENCES teams(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE projects (
    id TEXT PRIMARY KEY,
    workspace_id TEXT,
    team_id TEXT,
    name TEXT NOT NULL,
    status TEXT CHECK(status IN ('On Track', 'At Risk', 'Off Track', 'On Hold', 'Complete')),
    created_at TIMESTAMP NOT NULL,
    due_date DATE,
    FOREIGN KEY(workspace_id) REFERENCES workspaces(id),
    FOREIGN KEY(team_id) REFERENCES teams(id)
);

CREATE TABLE sections (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    name TEXT NOT NULL,
    order_index INTEGER NOT NULL,
    FOREIGN KEY(project_id) REFERENCES projects(id)
);

CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    section_id TEXT,
    parent_task_id TEXT,
    assignee_id TEXT,
    name TEXT NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT 0,
    completed_at TIMESTAMP,
    due_date DATE,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY(project_id) REFERENCES projects(id),
    FOREIGN KEY(section_id) REFERENCES sections(id),
    FOREIGN KEY(parent_task_id) REFERENCES tasks(id),
    FOREIGN KEY(assignee_id) REFERENCES users(id)
);

CREATE TABLE comments (
    id TEXT PRIMARY KEY,
    task_id TEXT,
    user_id TEXT,
    text TEXT,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY(task_id) REFERENCES tasks(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Metadata Tables
CREATE TABLE custom_field_definitions (
    id TEXT PRIMARY KEY,
    workspace_id TEXT,
    name TEXT NOT NULL,
    type TEXT NOT NULL, -- 'text', 'number', 'enum'
    FOREIGN KEY(workspace_id) REFERENCES workspaces(id)
);

CREATE TABLE custom_field_values (
    task_id TEXT,
    field_id TEXT,
    value_text TEXT,
    value_number REAL,
    FOREIGN KEY(task_id) REFERENCES tasks(id),
    FOREIGN KEY(field_id) REFERENCES custom_field_definitions(id)
);
CREATE TABLE teams (
	id VARCHAR(50) PRIMARY KEY,
	created_at TIMESTAMPTZ,
	deleted_at TIMESTAMPTZ
);

CREATE TABLE users (
	id VARCHAR(50) PRIMARY KEY,
	created_at TIMESTAMPTZ,
	deleted_at TIMESTAMPTZ,
	team_id VARCHAR(50),

	FOREIGN KEY(team_id)
	REFERENCES teams(id)
);

CREATE TABLE projects (
	id VARCHAR(50) PRIMARY KEY,
	created_at TIMESTAMPTZ,
	team_id VARCHAR(50),

	FOREIGN KEY(team_id)
	REFERENCES teams(id) 
);

CREATE TABLE projects_computed (
	id VARCHAR(50),
	created_at TIMESTAMPTZ,
	team_id VARCHAR(50),
	planned_duration VARCHAR(20),
	elapsed_duration VARCHAR(20),

	FOREIGN KEY(team_id)
	REFERENCES teams(id)
);

CREATE TABLE tasks (
	id VARCHAR(50) PRIMARY KEY,
	created_at TIMESTAMPTZ,
	is_container VARCHAR(10),
	parent_id VARCHAR(50),
	project_id VARCHAR(50),

	FOREIGN KEY(project_id)
	REFERENCES projects(id)
);

CREATE TABLE tasks_computed (
	id VARCHAR(50),
	created_at TIMESTAMPTZ,
	is_container VARCHAR(10),
	parent_id VARCHAR(50),
	project_id VARCHAR(50),
	planned_duration VARCHAR(20),
	elapsed_duration VARCHAR(20),

	FOREIGN KEY(project_id)
	REFERENCES projects(id)
);

CREATE TABLE declarations (
	id VARCHAR(50),
	created_at TIMESTAMPTZ,
	date DATE,
	durations BIGINT,
	source VARCHAR(20),
	user_id VARCHAR(50),
	task_id VARCHAR(50),

	FOREIGN KEY(user_id)
	REFERENCES users(id),

	FOREIGN KEY(task_id)
	REFERENCES tasks(id)
);

CREATE TABLE subscriptions (
	team_id VARCHAR(50),
	subscribe_at TIMESTAMPTZ,
	disabled_at TIMESTAMPTZ,
	status VARCHAR(20),
	offer VARCHAR(20),
	trial_start_at TIMESTAMPTZ,
	trial_end_at TIMESTAMPTZ,

	FOREIGN KEY(team_id)
	REFERENCES teams(id)
);
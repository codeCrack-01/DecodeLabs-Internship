## How to Use It (Step-by-Step Guide)

Once your server is running, the application automates background scanning and session logging. Here is how to use the system flow:

### 1. Register a Project / Workspace Path

Before scanning, you need to tell the system which directory contains your workspace.

- Open the Swagger UI (`http://127.0.0.1:8000/docs`).
- Expand the `POST /projects/` endpoint.
- Click **Try it out** and send a JSON payload specifying your project name and its absolute path on your system:

```json
{
  "name": "My Frontend App",
  "path": "/path/to/your/workspace/My_Frontend"
}
```

---

### 2. Trigger the Background Workspace Scan

The core automation feature scans your directories to look for framework signatures (such as `package.json` for Node.js projects or `requirements.txt` for Python projects).

- Navigate to the `POST /scan/` endpoint.
- Execute the request.
- This initiates an asynchronous task using FastAPI's `BackgroundTasks`.
- The scanner parses all registered workspace paths.
- It searches for files, matches them against the `SUPPORTED_INDICATORS` defined in `bg_scan.py`, and automatically attaches corresponding tech-stack tags to projects in the database.

---

### 3. Check the Scan Results

To verify which technologies were detected:

- Use the `GET /projects/` endpoint.
- The response returns all registered projects along with their automatically populated tags.

Example response:

```json
[
  {
    "id": 1,
    "name": "My Frontend App",
    "tags": ["React", "Node.js"]
  }
]
```

---

### 4. Log a Development Work Session

When you actively work on a project, log the elapsed duration to keep track of your time allocation.

- Navigate to the `POST /sessions/` endpoint.
- Provide the project ID and the number of minutes spent working.

Example payload:

```json
{
  "project_id": 1,
  "minutes": 45,
  "description": "Refactored database initialization and fixed relative imports"
}
```

This creates a session record associated with the selected project. Over time, session data can be used to analyze development effort, monitor productivity, and understand how time is distributed across different projects and technology stacks.

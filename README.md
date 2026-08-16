# CS Roster - Team Shift Scheduler

Interactive shift scheduling tool replacing Excel-based roster management.

## Quick Start

```
docker-compose up --build
```

Open http://localhost:8000 - login: admin@example.com / demo123456

### Standalone Demo

Open `demo.html` in any browser - fully offline, data in localStorage.

## Features

- Monthly grid with drag-select and keyboard shortcuts
- 13+ shift types with auto-calculated hours
- Real-time validation
- Overtime and comp-off tracking
- Auto-scheduling algorithm
- 50-step undo (Ctrl+Z)
- Permission control
- Export: TSV, Markdown, JSON

## Tech Stack

Vue 3 + TypeScript + Element Plus | Flask 2.x + SQLAlchemy + JWT | SQLite/MySQL | Docker

## Docs

- [Lark Integration](docs/guides/lark-integration.md)
- [Deployment](docs/guides/deployment.md)

## License

MIT

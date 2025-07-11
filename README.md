# manager_bot

A Telegram bot for managing office reports, schedules, and user roles in a distributed team environment.

## Features

- Office and region management
- Daily report collection and Excel export
- User and admin roles with region-based permissions
- Work schedule tracking and calendar integration
- Admin web panel for CRUD operations

## Technology Stack

- **Python 3.10+**
- **aiogram** (Telegram bot framework)
- **FastAPI** (webhook and admin panel)
- **SQLAlchemy** (ORM)
- **PostgreSQL** (database)
- **openpyxl** (Excel file generation)
- **asyncio** (asynchronous programming)
- **Redis** (caching, optional)
- **Uvicorn** (ASGI server)
- **Docker** (recommended for deployment)

## Project Structure

```
app/
  bot/           # Bot logic, handlers, filters, utils
  dao/           # Data access objects (database queries)
  users/         # User models and DAO
  offices/       # Office models and DAO
  reports/       # Report models and DAO
  admin/         # Admin panel views
  core/          # Constants, config, and base classes
  main.py        # FastAPI app entry point
README.md
requirements.txt
.env.example
docker-compose.yml
```
## app/bot/ directory structure

The `app/bot/` folder contains all the logic related to the Telegram bot, including handlers, filters, keyboards, states, and utility functions. Here is a detailed breakdown of its subfolders and files:

```
app/bot/
├── filters/         # Custom aiogram filters for message and callback processing
│   └── ...          # (e.g., user role checks, office/region validation)
├── handlers/        # All message and callback query handlers
│   └── subfunctions/   # additional handler logic, functions for processing information
├── keyboards/       # Inline and reply keyboard builders for user interaction
│   └── ...          # (e.g., calendar, menu, confirmation keyboards)
├── states/          # FSM state definitions for multi-step user interactions
│   └── ...          # (e.g., report submission, admin flows)
├── utils.py         # Utility functions for file handling, Excel generation, etc.
├── init_bot.py      # Bot and dispatcher initialization
├── routers.py       # Routers for grouping handlers by logic or access level
└── scheduler.py     #Scheduled/background tasks (e.g., notifications, periodic jobs)
```

### Main components:

- **filters/**  
  Contains custom aiogram filters for advanced message/callback validation (e.g., checking user roles, office existence, region admin rights).

- **handlers/**  
  Contains all bot handlers, split by logic (e.g., admin, user, reports). The `subfunctions/` subfolder contains additional handler logic, functions for processing information, preparing a response, functional mixins to support DRY principlesю

- **keyboards/**  
  Contains functions to build inline and reply keyboards, such as calendars, menus, and confirmation prompts.

- **states/**  
  Contains FSM state classes for managing multi-step user interactions (e.g., report submission, office selection).

- **utils.py**  
  Utility functions for file operations, Excel report generation, file downloads, and other helper logic.

- **captions.py**  
  Centralized storage for all bot message templates and captions, making it easy to manage and localize bot texts.

- **init_bot.py**  
  Initializes the aiogram Bot and Dispatcher objects, and sets up middleware if needed.

This modular structure keeps the bot logic organized, scalable, and easy to maintain.

## Deployment

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/manager_bot.git
cd manager_bot
```

### 2. Configure environment variables

Create a `main.env` file in the project root and set the following variables:

```
BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=postgresql+asyncpg://user:password@host:port/dbname
REDIS_URL=redis://localhost:6379/0
ADMIN_IDS=comma,separated,telegram,ids
WEBHOOK_URL=https://your.domain.com/webhook
```

### 3. Install dependencies

It is recommended to use a virtual environment. This project uses [Python UV](https://github.com/astral-sh/uv) for fast dependency management.

If you don't have UV installed, you can install it with:

```bash
pip install uv
```

Then install and activate dependencies with:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```


### 4. Run database migrations

If you use Alembic:

```bash
alembic upgrade head
```

### 5. Set up the webhook

Set the webhook for your bot using the provided management script or manually via Telegram Bot API.

---

### 6. Start the bot and web server

**Development:**

```bash
uvicorn app.main:app --reload
```

**Production (recommended with Docker):**

```bash
docker-compose up --build -
```


## License

MIT License

---

**Author:** Ilya Shirokov  
**Contact:** [ilshi2904@gmail.com]
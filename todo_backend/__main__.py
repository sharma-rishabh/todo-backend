import uvicorn
from dotenv import load_dotenv

load_dotenv("./.env")


def start_server():
    uvicorn.run(
        "todo_backend.api:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )

import uvicorn


def start_server():
    # print('Starting Server...')       

    uvicorn.run(
        "todo_backend.api:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
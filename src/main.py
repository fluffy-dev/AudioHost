import uvicorn
from src.app import get_app
# from src.config.project import settings as main_settings #TODO


app = get_app()


if __name__ == "__main__":
    # uvicorn.run("main:app", host=main_settings.host, port=main_settings.port, reload=main_settings.debug)#TODO
    uvicorn.run(app, host="0.0.0.0", port=8000)

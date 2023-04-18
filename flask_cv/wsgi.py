from evaluation import load_evaluation_stuff
from app import app


def start_server():
    load_evaluation_stuff()

    return app


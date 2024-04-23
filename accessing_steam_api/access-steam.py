from os import environ as ENV
import requests as req

from dotenv import load_dotenv


if __name__ == "__main__":

    load_dotenv()

    res = req.get(ENV["BASE_URL"])

    print(res.json())

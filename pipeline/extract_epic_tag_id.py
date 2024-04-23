from os import environ as ENV

from dotenv import load_dotenv
import requests as req


if __name__ == "__main__":

    load_dotenv()

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0"
    }

    res = req.get(ENV["EPIC_URL"], headers=headers).json()

    print(res['data']['t'])

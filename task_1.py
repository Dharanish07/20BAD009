import requests
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)


async def fetch_numbers(url):
    try:
        response = await requests.get(url, timeout=0.5)
        if response.ok:
            data = await response.json()
            return data.get("numbers", [])
    except (requests.exceptions.Timeout, requests.exceptions.RequestException):
        pass
    return []


@app.route('/numbers', methods=['GET'])
async def get_numbers():
    urls = request.args.getlist('url')
    numbers = set()

    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        futures = [loop.run_in_executor(executor, fetch_numbers, url) for url in urls]
        for future in futures:
            numbers.update(await future)

    return jsonify({"numbers": sorted(numbers)})


if __name__ == '__main__':
    import asyncio
    app.run(port=8008)

import ssl
import asyncio
import aiohttp
from flask import Flask, request, jsonify

app = Flask(__name__)
ssl_context = ssl._create_unverified_context()

async def fetch_instagram_profile(username, method="GET", **kwargs):
    url = "https://i.instagram.com/api/v1/users/web_profile_info/"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 243.1.0.14.111 (iPhone13,3; iOS 15_5; en_US; en-US; scale=3.00; 1170x2532; 382468104) NW/3",
    }

    async with aiohttp.ClientSession() as session:
        async with session.request(
            method,
            url,
            params={"username": username},
            headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 243.1.0.14.111 (iPhone13,3; iOS 15_5; en_US; en-US; scale=3.00; 1170x2532; 382468104) NW/3"},
            ssl=ssl_context,
            **kwargs
        ) as response:
            return await response.text()

@app.route("/api/instagram", methods=["GET"])
def instagram_api():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "Missing ?username= parameter"}), 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    data = loop.run_until_complete(fetch_instagram_profile(username))
    return jsonify(data)

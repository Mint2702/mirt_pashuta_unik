import os
import requests

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        promt = request.form["promt"]
        response = create_image(promt)
        image_url = response['data'][0]['url']
        return redirect(url_for("index", result=image_url))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def create_image(promt: str) -> dict:
    result = requests.post("https://api.openai.com/v1/images/generations", json={"prompt": promt, "n": 1, "size": "256x256"}, headers={"Authorization": f"Bearer {openai.api_key}"})
    return result.json()

def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )

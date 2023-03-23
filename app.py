import openai
from flask import Flask, redirect, render_template, url_for, request

from settings import settings
from logic import create_image, add_user, get_all_users, create_profile_description
from flask_cors import CORS

app = Flask(__name__)
openai.api_key = settings.openai_api_key
CORS(app, supports_credentials=True)



@app.route("/", methods=("GET", "POST", "PUT"))
def index():
    if request.method == "POST":
        fio = request.form["fio"]
        user_facts = request.form["user_facts"]
        sex = request.form["sex"]
        user_description = request.form["user_description"]
        image_type = request.form["image_type"]

        image_url = create_image(user_description, sex, image_type)

        profile_description = create_profile_description(
            user_facts=user_facts, user_description=user_description, sex=sex, fio=fio
        )

        user = add_user(
            user_facts=user_facts,
            fio=fio,
            photo_url=image_url,
            user_description=user_description,
            profile_description=profile_description,
        )
        return redirect(url_for("index", user=user))

    result = request.args.get("result")
    return render_template("index.html", result=result)


@app.route("/showcase", methods=("GET",))
def showcase():
    users = get_all_users()

    return render_template("showcase.html", users=users)


@app.route("/news", methods=("GET",))
def news():
    

    return render_template("news.html")





@app.route("/gpt_info", methods=("GET",))
def gpt_info():
    

    return render_template("gpt_info.html")




@app.route("/dalle_info", methods=("GET",))
def dalle_info():
    

    return render_template("dalle_info.html")

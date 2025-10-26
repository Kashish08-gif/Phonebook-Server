from flask import Flask, render_template, request, redirect, url_for
import json
import os


app = Flask(__name__)
FILE_NAME = "phonebook.json"


def load_phonebook():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    else:
        return {}


def save_phonebook(phonebook):
    with open(FILE_NAME, "w") as file:
        json.dump(phonebook, file, indent=4)


@app.route("/")
def home():
    phonebook = load_phonebook()
    return render_template("index.html", phonebook=phonebook)


@app.route("/add_contact", methods=["GET", "POST"])
def add_contact():
    message = ""
    if request.method == "POST":
        name = request.form.get("name", "").strip().title()
        phone = request.form.get("phone", "").strip()
        if name and phone:
            phonebook = load_phonebook()
            phonebook[name] = phone
            save_phonebook(phonebook)
            message = f"Contact {name} added successfully!"
        else:
            message = "Please enter both name and phone."
    return render_template("add.html", message=message)


@app.route("/search_contact", methods=["GET", "POST"])
def search_contact():
    result = None
    if request.method == "POST":
        name = request.form["name"].strip().title()
        phonebook = load_phonebook()
        if name in phonebook:
            result = f"{name}: {phonebook[name]}"
        else:
            result = f"{name} not found."
    return render_template("search.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)

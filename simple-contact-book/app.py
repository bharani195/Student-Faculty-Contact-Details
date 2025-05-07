from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Filepath for storing contacts
FILE_PATH = "contact_book.json"

# Load contacts from file
def load_contacts():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as file:
        return json.load(file)

# Save contacts to file
def save_contacts(contacts):
    with open(FILE_PATH, "w") as file:
        json.dump(contacts, file, indent=4)

# Home route
@app.route("/")
def index():
    return render_template("index.html")

# Add contact route
@app.route("/add", methods=["GET", "POST"])
def add_contact():
    if request.method == "POST":
        role = request.form["role"]
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]

        contacts = load_contacts()
        contacts.append({"role": role, "name": name, "phone": phone, "email": email})
        save_contacts(contacts)
        return redirect(url_for("view_contacts"))
    return render_template("add_contact.html")

@app.route("/view")
def view_contacts():
    contacts = load_contacts()  # Load all contacts from the JSON file
    students = [c for c in contacts if c["role"] == "student"]  # Filter students
    faculty = [c for c in contacts if c["role"] == "faculty"]  # Filter faculty
    return render_template("view_contacts.html", students=students, faculty=faculty)

# Search contact route
@app.route("/search", methods=["GET", "POST"])
def search_contact():
    if request.method == "POST":
        query = request.form["query"].lower()
        contacts = load_contacts()
        results = [c for c in contacts if query in c["name"].lower() or query in c["role"].lower()]
        return render_template("search_contact.html", contacts=results, query=query)
    return render_template("search_contact.html", contacts=None)

# Update contact route
@app.route("/update/<name>", methods=["GET", "POST"])
def update_contact(name):
    contacts = load_contacts()
    contact = next((c for c in contacts if c["name"] == name), None)
    if not contact:
        return "Contact not found", 404

    if request.method == "POST":
        contact["role"] = request.form["role"] or contact["role"]
        contact["phone"] = request.form["phone"] or contact["phone"]
        contact["email"] = request.form["email"] or contact["email"]
        save_contacts(contacts)
        return redirect(url_for("view_contacts"))

    return render_template("update_contact.html", contact=contact)

# Delete contact route
@app.route("/delete/<name>")
def delete_contact(name):
    contacts = load_contacts()
    contacts = [c for c in contacts if c["name"] != name]
    save_contacts(contacts)
    return redirect(url_for("view_contacts"))

if __name__ == "__main__":
    app.run(port=5000, debug=True)
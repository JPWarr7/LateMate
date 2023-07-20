# Project Setup Guide

Follow these steps to properly set up the project:

## 1. Clone the Repository

Clone the repository to your local machine.

## 2. Configure .flaskenv File

Open the `.flaskenv` file and replace the placeholder values with your own database and VM credentials.

## 3. Update the populate_db.py File

Navigate to the `populate_db.py` file and update the path after `/home/` to your VM username.

For example:
folder_path = "/home/CHANGE_THIS_PART/ctrl-alt-elite-dev/FALL-2023-CSC-schedule.csv"

## 4. Launch the Application

Finally, type `flask run` in the terminal to launch the application.

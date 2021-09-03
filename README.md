# CGH AI Chatbot
The main goal of this project is to save time on the entire hiring process.

This will be done through three main features:
- An application management tool to streamline recruitment workflow for HR.
- A 24/7 smart chatbot to facilitate the job application of job seekers.
- AI analysis of potential candidates to help select the best talent profiles without bias.

For the first stage of the project, I will be focusing on developing the structure and interface of the entire web app.


## Installation
After cloning, use command-line to cd to the project folder and install the necessary packages.

Step 1: Install requirements
```bash
pip install -r requirements.txt
```
Step 2: Set environment variables
```
export SECRET_KEY=(type any secret key)
export SQLALCHEMY_DATABASE_URI=sqlite:///(type database name).sqlite3
export EMAIL_USER=(Type server email username)
export EMAIL_PASS=(Type server email password)
```
Note: Email functionality does not work yet

Step 3: Set up the database (requires sqlite)
```python
python cghChatbot/models.py
```
Step 4: Run the website
```python
python app.py
```

## Content

The app contains the following activities:
```
.
├─ admin
│  ├─ home
│  ├─ create job
│  └─ edit job
├─ auth
│  ├─ login
│  ├─ signup
│  └─ reset password
├─ user
│  ├─ home
│  ├─ attempt quiz
│  └─ view account
└─ chatbot
```
To see a more detailed view and explanation of the structure click [here](https://pastebin.com/a8PXfVzp)

## To Do


## Tech

- HTML/CSS/Javascript
- JQuery/Ajax
- Flask
- SQLite3
- Tensorflow/Keras

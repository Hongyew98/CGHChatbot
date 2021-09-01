# CGH AI Chatbot
The main goal of this project is to save time on the entire hiring process.

This will be done through three main features:
- An application management tool to streamline recruitment workflow for HR.
- A 24/7 smart chatbot to facilitate the job application of job seekers.
- AI analysis of potential candidates to help select the best talent profiles without bias.

For the first stage of the project, I will be focusing on developing the structure and interface of the entire web app.


## Installation
After cloning, use command-line to cd to the project folder and install the necessary packages.

```bash
pip install -r requirements.txt
```
Next, install the database (requires sqlite)
```python
python cghChatbot/models.py
```
Finally, to run the website:
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
To see a more detailed view and explanation of the structure click [here](https://pastebin.com/r2yph7i7)

I did not create a navigation bar. Urls have to be accessed manually.

## Notes
The idea of this version was to separate the cv uploading and the quiz from the chatbot, but it seems that the stakeholders want to incorporate all 3 elements together.

This version has been phased out and is no longer in development due to changes with the project direction.

## Tech
- HTML/CSS/Javascript
- JQuery/Ajax
- Flask
- SQLite3
- Tensorflow/Keras
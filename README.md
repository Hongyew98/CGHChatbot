
# CGH AI Chatbot

The main goal of this project is to save time on the entire hiring process.

This will be done through three main features:
- An application management tool to streamline recruitment workflow for HR.
- A 24/7 smart chatbot to facilitate the job application of job seekers.
- AI analysis of potential candidates to help select the best talent profiles without bias.

For the first stage of the project, I will be focusing on developing the application management tool for HR.


## Installation

After cloning, use command-line to cd to the project folder and install the necessary packages.

```bash
pip install -r requirements.txt
```
To run the website: (doesn't work)
```python
python app.py
```
To submit a job application for testing: (works)
```python
python submit.py
```

## Content

There will be 6 main activities:
1. Login
2. Home
3. New Job Listing
4. Pending Applications
5. Completed Applications
6. Questions

As of now, none of these are functional.

### TODO:
The pages are being constructed. I have just settled the database and am now working on a basic functional layout for each of the pages, starting from 4 - Pending Applications. After that, the following functions can be implemented to improve user experience.
- Searching, Sorting, Filtering
- Side menu/navbar pop up
- Star/Pin/Flag
- Export data
- Email data
- Account creation



The following 2 files are to simulate a candidate submitting an application with a completed test, as well as any questions they might have.
> apply.py  
apply.html  

## Tech Stack

- HTML/CSS/Javascript
- AJAX
- Flask
- SQLite3



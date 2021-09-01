import os
import secrets
from flask import current_app
from PIL import Image

def save_picture(image):
    randomHex = secrets.token_hex(8)
    _, fileExt = os.path.splitext(image.filename) # underscore is throwaway
    newName = randomHex + fileExt
    imagePath = os.path.join(current_app.root_path, "user/static/profile_pics", newName)
    resize = (125, 125)
    newImage = Image.open(image)
    newImage = newImage.resize(resize)
    newImage.save(imagePath)
    return newName

def save_cv(cv):
    randomHex = secrets.token_hex(8)
    _, fileExt = os.path.splitext(cv.filename) # underscore is throwaway
    newName = randomHex + fileExt
    cvPath = os.path.join(current_app.root_path, "user/static/cvs", newName)
    cv.save(cvPath)
    return newName


def delete(file):
    try:
        os.remove(file)
    except:
        pass
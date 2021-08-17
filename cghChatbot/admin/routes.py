from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from ..models import *

admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.route("/", methods=["GET", "POST"])
def overview():
    return "admin"

@admin.route("/create", methods=["GET", "POST"])
def create():
    return "admin"

@admin.route("/edit", methods=["GET", "POST"])
def edit():
    return "admin"
    #functions: select jobs, route all cvs and tests to page, can email to self or download (choose automatic from bot or manual)
    #create job listing: upload test questions and details, get chatbot link
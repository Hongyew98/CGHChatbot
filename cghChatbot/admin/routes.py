from flask import Blueprint, render_template, redirect, url_for, flash
from ..models import *
from .utils import *

admin = Blueprint("admin", __name__, url_prefix="/admin", static_folder="static", static_url_path="/CGHChatbot/cghChatbot/admin", template_folder="templates")

@admin.route("/", methods=["GET", "POST"])
@admin_required
def index():
    return render_template("index_admin.html")

@admin.route("/create", methods=["GET", "POST"])
@admin_required
def create():
    return render_template("create.html")

@admin.route("/edit", methods=["GET", "POST"])
@admin_required
def edit():
    return render_template("edit.html")

#functions: select jobs, route all cvs and tests to page, can email to self or download (choose automatic from bot or manual)
#create job listing: upload test questions and details, get chatbot link
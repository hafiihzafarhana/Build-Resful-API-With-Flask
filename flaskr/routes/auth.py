from flask import Blueprint

# auth menajadi nama
# __name__ digunakan untuk mengatur dimana blueprint akan berjalan
auth = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth.post("/register")
def register():
    return "Register"


@auth.get("/me")
def me():
    return "me"


@auth.post("/login")
def login():
    return "login"

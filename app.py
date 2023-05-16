import json
from os import environ, path
from urllib.parse import quote_plus, urlencode, urljoin, urlparse, urlunparse

import requests
from authlib.integrations.flask_client import OAuth
from dotenv import dotenv_values, find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for

load_dotenv(".env.defaults")
load_dotenv(".env")


app = Flask(__name__)
app.config.update(
    {
        "STATIC_DIR": environ.get(
            "STATIC_DIR", path.join(path.dirname(path.realpath(__file__)), "public")
        ),
        "SECRET_KEY": environ.get("SESSION_SECRET", "yoursecret"),
        "BASE_URL": environ.get("BASE_URL", "http://localhost:8090"),
        "VV_ISSUER_URL": environ.get("VV_ISSUER_URL"),
        "VV_CLIENT_ID": environ.get("VV_CLIENT_ID"),
        "VV_CLIENT_SECRET": environ.get("VV_CLIENT_SECRET"),
    }
)


oauth = OAuth(app)
oauth.register(
    "vaultvision",
    client_id=app.config.get("VV_CLIENT_ID"),
    client_secret=app.config.get("VV_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=urljoin(
        app.config.get("VV_ISSUER_URL"), "/.well-known/openid-configuration"
    ),
)


@app.route("/")
def index():
    a = json.dumps(session.get("userinfo"), sort_keys=True, indent=2)
    tpl_ctx = {
        "user": session.get("userinfo"),
        "user_json": a,
        "oidc": {
            "issuer_url": app.config.get("VV_ISSUER_URL"),
        },
    }

    try:
        u = urljoin(
            app.config.get("VV_ISSUER_URL"),
            "/.well-known/openid-configuration"
        )
        res = requests.get(u)
        res.raise_for_status()
    except Exception as err:
        tpl_ctx["oidc"]["error"] = err
    return render_template("index.html", **tpl_ctx)


@app.route("/login")
def login():
    return redirect(url_for("auth_login"))


# /auth/login kicks off the OIDC flow by redirecting to Vault Vision. Once
# authentication is complete the user will be returned to /auth/callback.
@app.route("/auth/login")
def auth_login():
    return oauth.vaultvision.authorize_redirect(
        redirect_uri=url_for("auth_callback", _external=True)
    )


# Once Vault Vision authenticates a user they will be sent here to complete
# the OIDC flow.
@app.route("/auth/callback", methods=["GET", "POST"])
def auth_callback():
    oauth.vaultvision.authorize_access_token()
    userinfo = oauth.vaultvision.userinfo()

    session.update(
        {
            "userinfo": userinfo,
        }
    )
    return redirect("/")


# Logout clears the cookies and then sends the users to Vault Vision to clear
# the session, then Vault Vision will redirect the user to /auth/logout.
@app.route("/logout")
def logout():
    session.clear()
    q = urlencode(
        {
            "return_to": urljoin(app.config.get("BASE_URL"), "/auth/logout"),
            "client_id": app.config.get("VV_CLIENT_ID"),
        },
        quote_via=quote_plus,
    )
    redir = urljoin(app.config.get("VV_ISSUER_URL"), "/logout?%s" % q)
    return redirect(redir)


@app.route("/auth/logout")
def auth_logout():
    return redirect(url_for("index"))


# /settings just redirects to /auth/settings. But it could contain any app 
# specific logic or a confirmation page that shows a settings button.
@app.route("/settings")
def settings():
    return redirect("/auth/settings")


# /auth/settings redirects to the Vault Vision settings page so users can
# manage their email, password, social logins, webauthn credentials and more.
# 
# This works by using an oidc prompt named "settings". When the user returns
# your session will be updated to reflect any changes they made.
@app.route("/auth/settings")
def auth_settings():
    redir = url_for("auth_callback", _external=True)
    return oauth.vaultvision.authorize_redirect(
        redirect_uri=redir,
        prompt="settings",
    )


if __name__ == "__main__":
    listen_url = urlparse(app.config.get("BASE_URL"))
    app.run(host=listen_url.hostname, port=listen_url.port)

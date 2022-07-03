from flask import Flask, render_template, redirect

import os

from flask import Flask, redirect, url_for
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

# Create a flask app
app = Flask(
  __name__,
  template_folder='dashboard',
  static_folder='static'
)

app.secret_key = b"by-xvladx-programming-studio"
# OAuth2 must make use of HTTPS in production environment.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"      # !! Only in development environment.

app.config["DISCORD_CLIENT_ID"] = 1234567890    # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"                # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "https://your-website-url/callback/"                 # URL to your callback endpoint.
app.config["DISCORD_BOT_TOKEN"] = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"                    # Required to access BOT resources.


discord = DiscordOAuth2Session(app)

def welcome_user(user):
    dm_channel = discord.bot_request("/users/@me/channels", "POST", json={"recipient_id": user.id})
    return discord.bot_request(
        f"/channels/{dm_channel['id']}/messages", "POST", json={"content": "Thanks for authorizing the app!"}
    )

@app.route("/login/")
def login():
    return discord.create_session(scope=['identify', 'email'])


@app.route("/callback/")
def callback():
    discord.callback()
    user = discord.fetch_user()
    welcome_user(user)
    return redirect(url_for(".me"))


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))


@app.route("/me/")
@requires_authorization
def me():
    user = discord.fetch_user()
    return f"""
    <html>
        <head>
            <title>{user.name}#{user.discriminator}</title>
        </head>
        <body>
            <img src='{user.avatar_url}' />
            <h1>Hey, {user.name}#{user.discriminator}!</h1>
        </body>
    </html>"""

# Index page (now using the index.html file)
@app.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  # Run the Flask app
  app.run(
	host='0.0.0.0',
	debug=True,
	port=8080
  )

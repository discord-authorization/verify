from flask import Flask, redirect, request, jsonify
import requests

app = Flask(__name__)

# Replace these with your actual Client ID, Client Secret, and Redirect URI
CLIENT_ID = "1242183096804053003"
CLIENT_SECRET = "xOifdVdR2AdyEbKNgIwhBJqxrYKa07ny"
REDIRECT_URI = "https://discord-authorization.github.io/verify/"

@app.route("/")
def index():
    return redirect(f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify")

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Error: Authorization code not provided."

    # Exchange the authorization code for an access token
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": "identify"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    token_response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    if token_response.status_code != 200:
        return f"Error getting access token: {token_response.text}"

    access_token = token_response.json()["access_token"]

    # Use the access token to get user information
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    user_response = requests.get("https://discord.com/api/users/@me", headers=headers)
    if user_response.status_code != 200:
        return f"Error getting user information: {user_response.text}"

    user_data = user_response.json()
    username = user_data["username"]

    return jsonify({"access_token": access_token, "username": username})

if __name__ == "__main__":
    app.run(debug=True)

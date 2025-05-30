from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

UNIVERSE_ID = 7436755782

@app.route('/')
def index():
    # Initial page render, you can send name once to display
    try:
        url = f"https://games.roblox.com/v1/games?universeIds={UNIVERSE_ID}"
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()

        if 'data' not in json_data or len(json_data['data']) == 0:
            game_name = "Unknown Game"
        else:
            game_name = json_data['data'][0].get('name', 'Unknown Game')
    except:
        game_name = "Unknown Game"

    return render_template('index.html', game_name=game_name)

@app.route('/stats')
def stats():
    try:
        url = f"https://games.roblox.com/v1/games?universeIds={UNIVERSE_ID}"
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        if 'data' not in json_data or len(json_data['data']) == 0:
            return jsonify({"error": "No game data found."}), 404

        data = json_data['data'][0]
        return jsonify({
            "playing": data.get('playing', 0),
            "visits": data.get('visits', 0),
            "favorites": data.get('favoritedCount', 0)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)

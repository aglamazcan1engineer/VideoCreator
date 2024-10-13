import os
import asyncio
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file, jsonify
from api_clients.api_factory import APIFactory
import requests

load_dotenv()

app = Flask(__name__)

# API istemcilerini oluştur
api_clients = {}
for api_name in ["unsplash", "pexels", "fma"]:
    api_key = os.getenv(f"{api_name.upper()}_API_KEY")
    if api_key:
        api_clients[api_name] = APIFactory.get_client(api_name, api_key)
    else:
        print(f"Uyarı: {api_name.upper()}_API_KEY bulunamadı veya boş.")

async def search_all_apis(query, per_page=5):
    tasks = []
    for client in api_clients.values():
        if isinstance(client, api_clients['fma'].__class__):
            tasks.append(client.search_music(query, limit=per_page))
        else:
            tasks.append(client.search_images(query, per_page))
    results = await asyncio.gather(*tasks)
    return results

@app.route('/', methods=['GET', 'POST'])
async def home():
    if request.method == 'POST':
        user_input = request.form['user_input']
        results = await search_all_apis(user_input)
        images = [item for sublist in results[:-1] for item in sublist]  # Flatten image results
        music = results[-1]  # FMA results
        return render_template('results.html', images=images, music=music)
    return render_template('home.html')

@app.route('/download_music/<path:url>')
def download_music(url):
    response = requests.get(url)
    return send_file(
        io.BytesIO(response.content),
        mimetype="audio/mpeg",
        as_attachment=True,
        attachment_filename="music.mp3"
    )

if __name__ == '__main__':
    app.run(debug=True)
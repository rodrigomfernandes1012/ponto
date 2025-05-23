from flask import Flask, jsonify, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/dados')
def get_dados():
    import requests
    supabase_url = "https://luvluchyqpfnckfutwja.supabase.co"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx1dmx1Y2h5cXBmbmNrZnV0d2phIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDczMTA0OTEsImV4cCI6MjA2Mjg4NjQ5MX0.tfI7QZiBDSkTwXlZlJgUprMzW3u27zbPJfjUWNIldXc"
    url = f"{supabase_url}/rest/v1/TbCubagem"
    headers = {
        "apikey": token,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": f"Erro {response.status_code}"}), response.status_code


def main():
   # port = int(os.environ.get("PORT", 8080))
   # app.run(host="127.0.0.1", port=port)
    port = int(os.environ.get("PORT", 80))
    app.run(host="192.168.0.200", port=port)


if __name__ == "__main__":
    main()

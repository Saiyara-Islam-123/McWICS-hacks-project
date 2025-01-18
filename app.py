from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap

app = Flask(__name__)

bootstrap = Bootstrap(app)
item_links = []

@app.route('/')
def index():
    return render_template('app.html', links=item_links)

@app.route('/add-item', methods=['POST'])
def add_item():
    global item_links

    item_link = request.json.get('link')
    if item_link:
        item_links.append({"link": item_link, "price": len(item_links) * 10}) 
        print(f"Received link: {item_link}")

        return jsonify({"status": "success", "itemLink": item_link})
    else:
        return jsonify({"status": "error", "message": "No link provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
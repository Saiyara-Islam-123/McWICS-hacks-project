from flask import Flask, render_template, redirect, request, jsonify
from flask_bootstrap import Bootstrap
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

app = Flask(__name__)

bootstrap=Bootstrap(app)
item_links = []
user_budget = 0.0
bought_items = []
 
# Landing page
@app.route('/')
def index():
    return render_template('app.html', links=item_links)

# Wishlist page
@app.route('/mycart')
def my_shopping_cart():
    return render_template('app.html', links=item_links)  
    
# creating a database to store login credentials for users
login_databasee = {'admin' : 'password'}

# Creating a function to allow users to login from the login page
@app.route('/login', methods=['POST', 'GET'])
def login():
    usr_name = request.form['username']
    usr_pwd = request.form['password']
    # existing user trying to login
    if 'login' in request.form:
        if usr_name in login_databasee and usr_pwd == login_databasee[usr_name]:
            return render_template('app.html')
        else:
            return render_template('login.html')
    # new user creating account and logging in
    elif 'create_user' in request.form:
        if usr_name not in login_databasee:
            login_databasee[usr_name] = usr_pwd
            return render_template('app.html')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/set-budget', methods=['POST'])
def set_budget():
    global user_budget
    user_budget = float(request.json.get('budget'))
    return jsonify({"status": "success", "budget": user_budget})

@app.route('/update-budget', methods=['POST'])
def update_budget():
    global user_budget
    item_price = float(request.json.get('price'))
    bought_items.append(item_price)
    user_budget -= item_price
    return jsonify({"status": "success", "remaining_budget": user_budget})
 
@app.route('/get-items', methods=['GET'])
def get_items():
    return jsonify(item_links)
    
@app.route('/add-item', methods=['POST'])
def add_item():
    global item_links

    item_link = request.json.get('link')
    if item_link:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Referer': 'https://www.google.com',
                'Connection': 'keep-alive'
            }
            response = requests.get(item_link, headers=headers)

            source_code = response.text

            name_start = source_code.find('"name":"')
            product_name = "Unknown Product"
            if name_start != -1:
                name_start += len('"name":"')
                name_end = source_code.find('"', name_start)
                product_name = source_code[name_start:name_end]

            image_start = source_code.find('"image"')
            product_image = 'https://via.placeholder.com/200'
            if image_start != -1:
                link_start = source_code.find('https://', image_start)  
                if link_start != -1:
                    link_end = source_code.find('"', link_start)
                    product_image = source_code[link_start:link_end]

            price_start = source_code.find('"price"')
            product_price = '$0.00'
            if price_start != -1:
                price_start += len('"price"')
                while price_start < len(source_code) and not source_code[price_start].isdigit():
                    price_start += 1
                if price_start < len(source_code):
                    price_end = price_start
                    while price_end < len(source_code) and (source_code[price_end].isdigit() or source_code[price_end] == '.'):
                        price_end += 1
                    product_price = source_code[price_start:price_end]

            domain = urlparse(item_link).netloc
            product_shop = domain.split('.')[1]
            if product_shop == "shop": product_shop = domain.split('.')[2]
            if product_shop == "hm": product_shop = "H&M"

            item_links.append({
                "link": item_link,
                "name": product_name,
                "image": product_image,
                "price": product_price,
                "shop": product_shop.capitalize()
            })

            return jsonify({
                "status": "success",
                "itemLink": item_link,
                "name": product_name,
                "image": product_image,
                "price": product_price,
                "shop": product_shop.capitalize()
            })
        except Exception as e:
            print(f"Error processing link: {e}")
            return jsonify({"status": "error", "message": "Failed to fetch product details"}), 400
    else:
        return jsonify({"status": "error", "message": "No link provided"}), 400

@app.route('/delete-item', methods=['DELETE'])
def delete_item():
    global item_links
    item_link = request.json.get('link')   

    for item in item_links:
        if item['link'] == item_link:
            item_links.remove(item)
            return jsonify({'status': 'success', 'message': 'Product removed'}), 200

    return jsonify({'status': 'error', 'message': 'Failed to remove product'}), 404

if __name__ == '__main__':
    app.run(debug=True)
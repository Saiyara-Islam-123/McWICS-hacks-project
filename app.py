from flask import Flask, render_template, redirect, request, jsonify
from flask_bootstrap import Bootstrap
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

bootstrap=Bootstrap(app)
item_links = []
 
# Landing page
@app.route('/')
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
    
@app.route('/add-item', methods=['POST'])
def add_item():
    global item_links

    item_link = request.json.get('link')
    if item_link:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(item_link, headers=headers)
            source_code = response.text

            name_start = source_code.find('"name":"') 
            product_name = "Unknown Product"
            if name_start != -1:
                name_start += len('"name":"')
                name_end = source_code.find('"', name_start)
                product_name = source_code[name_start:name_end]

            image_start = source_code.find('"image":"')
            product_image = 'https://via.placeholder.com/200'
            if image_start != -1:
                image_start += len('"image":"')
                image_end = source_code.find('"', image_start)
                product_image = source_code[image_start:image_end]

            price_start = source_code.find('"price":"')
            product_price = '$0.00'
            if price_start != -1:
                price_start += len('"price":"')
                price_end = source_code.find('"', price_start)
                product_price = source_code[price_start:price_end]

            item_links.append({
                "link": item_link,
                "name": product_name,
                "image": product_image,
                "price": product_price
            })

            print(f"Product Name: {product_name}, Image: {product_image}, Price: {product_price}")

            return jsonify({
                "status": "success",
                "itemLink": item_link,
                "name": product_name,
                "image": product_image,
                "price": product_price
            })
        except Exception as e:
            print(f"Error processing link: {e}")
            return jsonify({"status": "error", "message": "Failed to fetch product details"}), 400
    else:
        return jsonify({"status": "error", "message": "No link provided"}), 400



if __name__ == '__main__':
    app.run(debug=True)
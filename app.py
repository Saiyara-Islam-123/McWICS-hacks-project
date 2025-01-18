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
            soup = BeautifulSoup(response.text, 'html.parser')

            product_name = soup.find('meta', property='og:title')['content'] if soup.find('meta', property='og:title') else soup.find('title').text.strip()
            print(product_name)

            product_image = soup.find('meta', property='og:image')['content'] if soup.find('meta', property='og:image') else 'https://via.placeholder.com/200'

            price_tag = soup.select_one('.price, .product-price, [itemprop=price]')
            product_price = price_tag.text.strip() if price_tag else '$0.00'

            item_links.append({
                "link": item_link,
                "name": product_name,
                "image": product_image,
                "price": product_price
            })

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
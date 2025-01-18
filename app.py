from flask import Flask, render_template, redirect, request, jsonify
from flask_bootstrap import Bootstrap

app = Flask(__name__)

bootstrap=Bootstrap(app)
item_links = []
 
# Landing page
@app.route('/')
# Wishlist page
@app.route('/mycart')
def my_shopping_cart():
    return render_template('app.html', links=item_links)  

# Adding links to wishlist page
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

if __name__ == '__main__':
    app.run(debug=True)
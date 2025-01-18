from flask import Flask,render_template,redirect
from flask_bootstrap import Bootstrap
 
app = Flask(__name__)

bootstrap=Bootstrap(app)
 
@app.route('/')
def hello():
    return render_template('app.html')  
 
if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'This is index page'

@app.route('/help')
def help():
    return 'This is help page'

@app.route('/user/<username>')
def userpage(username):
    return 'This is %s\'s page ' % username

if __name__ == '__main__':
    #app.run()
    app.run(debug=True)

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/help')
def help():
    return 'This is help page'

@app.route('/user/<username>')
def userpage(username):
    return 'This is %s\'s page ' % username

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # If you enable debug support the server will reload itself on code changes 
    app.debug = True
    app.run()

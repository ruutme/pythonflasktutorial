from flask import Flask

app = Flask(__name__)

@app.route('/')
def deploy():
    return 'Hello world!'

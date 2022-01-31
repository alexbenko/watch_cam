from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello from Watch Cam !</h2>'


if __name__ == "__main__":
    app.run(host='0.0.0.0')

#docker build -t watch_cam:latest .
#docker tag watch_cam alexbenko/watch_cam && docker push alexbenko/watch_cam
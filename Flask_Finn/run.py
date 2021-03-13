
from flaskblog import app
from flaskblog.routes import ui
from threading import Timer

if __name__ == '__main__':
    Timer(1,lambda: ui("http://127.0.0.1:5000/")).start()
    app.run(debug = False)
    


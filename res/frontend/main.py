import os
from flask import Flask, render_template
app = Flask(__name__, static_folder='static')

@app.route('/', methods=['GET'])
def index_page_landing():
    video_name = os.listdir('./res/frontend/static/emotion')
    print (video_name)
    return render_template('index.html', video_name=video_name)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2000)
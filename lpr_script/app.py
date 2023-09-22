from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    # Handle license plate detection here
    # You can put your detection logic or function here
    return render_template('detection_result.html')

if __name__ == '__main__':
    app.run(debug=True)
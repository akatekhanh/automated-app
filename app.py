from flask import Flask, render_template, request

from negotiation import process_data
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    return render_template('home.html', result=result)


@app.route('/process', methods=['POST'])
def process():
    data = request.json
    return process_data(int(data['agent_1']), int(data['agent_2']))


if __name__ == "__main__":
    app.run(debug=True, port=8080)

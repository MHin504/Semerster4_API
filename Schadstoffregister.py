from flask import Flask, jsonify

app = Flask(__name__)

# Liste von Schadstoffen
schadstoffe = [
    {'id': 1, 'name': 'Schadstoff 1'},
    {'id': 2, 'name': 'Schadstoff 2'},
    {'id': 3, 'name': 'Schadstoff 3'},
    {'id': 4, 'name': 'Schadstoff 4'},
    {'id': 5, 'name': 'Schadstoff 5'}
]

@app.route('/schadstoffe', methods=['GET'])
def get_schadstoffe():
    return jsonify(list(map(lambda x: x['name'], schadstoffe)))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
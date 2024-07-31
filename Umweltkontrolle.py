from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///incidents.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    vorfall_art = db.Column(db.String(100), nullable=False)
    vorfall_ort = db.Column(db.String(100), nullable=False)
    schadstoff = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False, default='in_bearbeitung')

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        pollutants_response = requests.get('http://127.0.0.1:5001/schadstoffe')
        pollutants_response.raise_for_status()  # Überprüfen Sie, ob die Anfrage erfolgreich war
        pollutants = pollutants_response.json()
        return render_template('index.html', schadstoffe=pollutants)
    except requests.exceptions.RequestException as e:
        # Behandeln Sie den Fehler, wenn die Anfrage nicht erfolgreich war
        return render_template('index.html', schadstoffe=[], error=str(e))

@app.route('/send_incident', methods=['GET', 'POST'])
def send_incident():
    if request.method == 'POST':
        incident_data = request.form
        incident_data_dict = {}
        for key, value in incident_data.items():
            new_key = key.replace('-', '_')
            incident_data_dict[new_key] = value
        incident = Incident(
            date=datetime.datetime.now(),
            vorfall_art=incident_data_dict['vorfall_art'],
            vorfall_ort=incident_data_dict['vorfall_ort'],
            schadstoff=incident_data_dict['schadstoff'],
            status='in_bearbeitung'
        )
        db.session.add(incident)
        db.session.commit()
        return redirect(url_for('index', success=True))
    else:
        return 'Diese Seite kann nur per POST-Anfrage aufgerufen werden.'

@app.route('/incidents', methods=['GET'])
def get_incidents():
    incidents = Incident.query.all()
    return render_template('incidents.html', incidents=incidents)

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()  # Löschen Sie die alte Tabelle
        db.create_all()  # Erstellen Sie die neue Tabelle
    app.run(debug=True, port=5000)
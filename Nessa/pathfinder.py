from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)

# Configure the PostgreSQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/yourdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Job model
class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    date_applied = db.Column(db.Date, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Route to load jobs from a JSON file
@app.route('/api/load_jobs', methods=['POST'])
def load_jobs():
    with open('jobs.json', 'r') as file:
        jobs = json.load(file)
    
    for job in jobs:
        new_job = Job(
            company=job['company'],
            position=job['position'],
            status=job['status'],
            date_applied=datetime.strptime(job['dateApplied'], '%Y-%m-%d')
        )
        db.session.add(new_job)
    db.session.commit()

    return jsonify({"message": "Jobs loaded successfully!"}), 201

# API Route to handle CRUD operations for jobs
@app.route('/api/jobs', methods=['GET', 'POST'])
def handle_jobs():
    if request.method == 'POST':
        data = request.json
        new_job = Job(
            company=data['company'],
            position=data['position'],
            status=data['status'],
            date_applied=datetime.strptime(data['dateApplied'], '%Y-%m-%d')
        )
        db.session.add(new_job)
        db.session.commit()
        return jsonify({"message": "Job added successfully!"}), 201
    
    elif request.method == 'GET':
        jobs = Job.query.all()
        job_list = []
        for job in jobs:
            job_list.append({
                "id": job.id,
                "company": job.company,
                "position": job.position,
                "status": job.status,
                "dateApplied": job.date_applied.strftime('%Y-%m-%d')
            })
        return jsonify(job_list)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

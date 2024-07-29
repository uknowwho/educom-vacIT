import os
from datetime import date
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Configuration for PostgreSQL connection
db_password = os.environ["POSTGRES_PSWD"]
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:' + db_password + '@localhost/vacit'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object with the Flask app
db = SQLAlchemy(app)

# Define the ORM for the database
class Technique(db.Model):
    __tablename__ = 'techniques'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    logo_img = db.Column(db.String(255), unique=True, nullable=False)

    jobs = db.relationship('Job', back_populates='technique')

    def __repr__(self) -> str:
        return f"Technique {self.name}"

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    pswd = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    postal_code = db.Column(db.String(10), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    profile_img = db.Column(db.Text, nullable=False)
    resume_pdf = db.Column(db.Text, nullable=True)
    date_of_bearth = db.Column(db.Date, nullable=True)
    mobile = db.Column(db.String(20), nullable=True)

    jobs = db.relationship('Job', back_populates='company', foreign_keys='Job.company_id')
    candidate_jobs = db.relationship('CandidateJob', back_populates='candidate', foreign_keys='CandidateJob.candidate_id')

    def __repr__(self):
        return f"User {self.name} as {self.role}"

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    post_date = db.Column(db.Date, nullable=False, default=date.today)
    company_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    level = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technique_id = db.Column(db.Integer, db.ForeignKey('techniques.id'), nullable=True)

    company = db.relationship('User', back_populates='jobs', foreign_keys=[company_id])
    technique = db.relationship('Technique', back_populates='jobs', foreign_keys=[technique_id])
    candidate_jobs = db.relationship('CandidateJob', back_populates='job', foreign_keys='CandidateJob.job_id')

    def __repr__(self) -> str:
        return f"Job {self.id}"

class CandidateJob(db.Model):
    __tablename__ = 'candidate_jobs'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    motivation = db.Column(db.Text, nullable=False)

    job = db.relationship('Job', back_populates='candidate_jobs', foreign_keys=[job_id])
    candidate = db.relationship('User', back_populates='candidate_jobs', foreign_keys=[candidate_id])

    def __repr__(self) -> str:
        return f"Candidate {self.candidate_id} for Job {self.job_id}"


@app.route("/", methods=["GET"])
def index():
    # Query to get all jobs along with their associated companies and techniques
    jobs = db.session.query(Job, User, Technique).join(User, Job.company_id == User.id).join(Technique, Job.technique_id == Technique.id).order_by(Job.post_date).all()

    # Create a structured list for the template
    jobs_data = []
    for job, user, technique in jobs:
        jobs_data.append({
            "job_id": job.id,
            "post_date": job.post_date,
            "company_name": user.name,
            "technique_name": technique.name,
            "technique_icon": technique.logo_img,
            "level": job.level,
            "title": job.title,
            "location": job.location,
            "description": job.description
        })

    return render_template("index.html", jobs=jobs_data)

# @app.route("/profile", methods=["POST", "GET"])
# def profile():
#     return "Hello Profile!"
#     return render_template("")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

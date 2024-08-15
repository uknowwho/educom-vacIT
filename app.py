import os
import sys
from datetime import date
from flask import Flask, render_template, session, redirect, request, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash

from forms import ProfileForm, LoginForm, ApplicationForm, RegisterForm

app = Flask(__name__)

# Configuration for PostgreSQL connection
db_password = os.environ["POSTGRES_PSWD"]
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://postgres:{db_password}@localhost/vacit"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Set up a secret key for form CSRF protection
SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY

# Configure the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize the SQLAlchemy object with the Flask app
db = SQLAlchemy(app)

# Setup Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Define the ORM for the database
class Technique(db.Model):
    __tablename__ = 'techniques'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    logo_img = db.Column(db.String(255), unique=True, nullable=False)

    jobs = db.relationship('Job', back_populates='technique')

    def __repr__(self) -> str:
        return f"Technique {self.name}"

class User(db.Model, UserMixin):
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
    profile_img = db.Column(db.Text, nullable=False, default='uploads\profiles\default.jpg')
    resume_pdf = db.Column(db.Text, nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
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
    motivation = db.Column(db.Text, nullable=True)

    job = db.relationship('Job', back_populates='candidate_jobs', foreign_keys=[job_id])
    candidate = db.relationship('User', back_populates='candidate_jobs', foreign_keys=[candidate_id])

    def __repr__(self) -> str:
        return f"Candidate {self.candidate_id} for Job {self.job_id}"

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter(User.id == int(user_id)).first()

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

@app.route("/profile", methods=["POST", "GET"])
def profile():
    if current_user.is_anonymous:
        return redirect('/')

    form = ProfileForm(request.form, obj=current_user)
    if request.method == "POST" and form.validate_on_submit():
        form.populate_obj(current_user)

        # Manually handle resume upload
        resume_file = request.files.get('resume_pdf')
        if resume_file:
            filename = secure_filename(resume_file.filename)
            upload_resumes = app.config['UPLOAD_FOLDER'] + '/resumes'
            file_path = os.path.join(upload_resumes, filename)
            resume_file.save(file_path)
            current_user.resume_pdf = file_path

        # Manually handle profile image upload
        profile_img_file = request.files.get('profile_img')
        if profile_img_file:
            filename = secure_filename(profile_img_file.filename)
            upload_profiles = os.path.join(app.config['UPLOAD_FOLDER'], 'profiles')
            os.makedirs(upload_profiles, exist_ok=True)
            file_path = os.path.join(upload_profiles, filename)
            profile_img_file.save(file_path)
            current_user.profile_img = file_path

        # Commit the changes to the database
        db.session.commit()

        return redirect('/profile')
   
    return render_template("profile.html", form=form)

@app.route("/jobs/<job_id>", methods=["GET", "POST"])
def job_detail(job_id):
    # TODO: add 404 page
    job = db.session.query(Job).filter(Job.id == job_id).first()
    company = db.session.query(User).filter(User.id == job.company_id).first()
    technique = db.session.query(Technique).filter(Technique.id == job.technique_id).first()

    form = ApplicationForm()
    if request.method == "POST" and form.validate_on_submit():
        # Add the application to the candidate_jobs table only if none existant
        if not db.session.query(CandidateJob).filter(CandidateJob.job_id == job.id).filter(CandidateJob.candidate_id == current_user.id).first():
            new_application = CandidateJob(job_id=job.id, candidate_id=current_user.id)
            db.session.add(new_application)
            db.session.commit()

    return render_template("job.html", job=job, company=company, technique=technique, form=form)

@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect("/")

    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user and user.pswd == form.password.data:
            login_user(user)
            return redirect('/')
        else:
            flash('Invalid email or password')

    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect("/")

    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        existing_user = db.session.query(User).filter(User.email == form.email.data).first()

        if existing_user:
            flash('Email address already registered')
        else:
            # Create a new user instance
            new_user = User(
                role='ROLE_CANDIDATE',
                email=form.email.data,
                pswd=form.pswd.data,
                name=form.name.data,
                last_name=form.last_name.data
            )

            # Add the new user to the session and commit
            db.session.add(new_user)
            db.session.commit()

            # Log the user in after successful registration
            login_user(new_user)

            return redirect('/')

    return render_template("register.html", form=form)

@app.route('/uploads/resumes/<name>')
def download_file(name):
    return send_from_directory('uploads/resumes/', name)

@app.route('/uploads/profiles/<name>')
def show_img(name):
    return send_from_directory('uploads/profiles/', name)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

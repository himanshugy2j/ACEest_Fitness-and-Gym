from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-secret-to-something-random'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    workout = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # minutes
    date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('workouts', lazy=True))

# Add new models below this line

class StrengthWorkout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise = db.Column(db.String(200), nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)  # kg
    date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('strength_workouts', lazy=True))


class CardioWorkout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer)   # minutes
    distance = db.Column(db.Float)     # km
    calories = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('cardio_workouts', lazy=True))
# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            flash('Please provide username and password', 'warning')
            return redirect(url_for('signup'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists. Choose another.', 'danger')
            return redirect(url_for('signup'))

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Account created. You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user)
        flash('Logged in successfully', 'success')
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # Handle adding workouts
    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == "strength":
            exercise = request.form.get('exercise')
            reps = request.form.get('reps')
            weight = request.form.get('weight')
            if exercise and reps and weight:
                try:
                    reps = int(reps)
                    weight = float(weight)
                except ValueError:
                    flash("Invalid reps or weight", "warning")
                    return redirect(url_for('dashboard'))
                sw = StrengthWorkout(user_id=current_user.id, exercise=exercise, reps=reps, weight=weight)
                db.session.add(sw)
                db.session.commit()
                flash("Strength workout added", "success")

        elif form_type == "cardio":
            activity = request.form.get('activity')
            duration = request.form.get('duration')
            distance = request.form.get('distance')
            calories = request.form.get('calories')
            if activity and duration and distance:
                try:
                    duration = int(duration)
                    distance = float(distance)
                    calories = float(calories) if calories else None
                except ValueError:
                    flash("Invalid cardio values", "warning")
                    return redirect(url_for('dashboard'))
                cw = CardioWorkout(user_id=current_user.id, activity=activity, duration=duration, distance=distance, calories=calories)
                db.session.add(cw)
                db.session.commit()
                flash("Cardio workout added", "success")

        return redirect(url_for('dashboard'))

    # Query data for dashboard
    strength_workouts = StrengthWorkout.query.filter_by(user_id=current_user.id).order_by(StrengthWorkout.date.desc()).limit(10).all()
    cardio_workouts = CardioWorkout.query.filter_by(user_id=current_user.id).order_by(CardioWorkout.date.desc()).limit(10).all()

    # For graph: weights over time
    strength_graph_data = [
        {"date": w.date.strftime("%Y-%m-%d"), "weight": w.weight}
        for w in StrengthWorkout.query.filter_by(user_id=current_user.id).order_by(StrengthWorkout.date).all()
    ]

    return render_template("dashboard.html", strength_workouts=strength_workouts, cardio_workouts=cardio_workouts, strength_graph_data=strength_graph_data)


@app.route('/workouts')
@login_required
def workouts_page():
    workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.date.desc()).all()
    return render_template('workouts.html', workouts=workouts)

# Health check route
@app.route('/health')
def health():
    return {"status": "ok"}, 200

# Helper to create DB quickly
@app.cli.command('init-db')

def init_db():
    """Initialize the database."""
    db.create_all()
    print("Initialized the database.")

if __name__ == '__main__':
    app.run(debug=True)

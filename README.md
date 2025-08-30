# ACEest Fitness & Gym Tracker

A Flask web application for tracking workouts (strength & cardio), progress, and personal fitness profile.

---

## 🚀 Features
- User authentication (signup/login/logout)
- Add **strength workouts** (exercise, reps, weight)
- Add **cardio workouts** (activity, duration, distance, calories)
- View **progress graph** for strength over time
- (Planned) Manage personal **profile** (height, weight, age, profile picture, BMI)
- Dockerized for easy deployment
- CI/CD pipeline with GitHub Actions (builds Docker image + runs tests inside container)

---

## 🛠️ Setup (Local)

### 1. Clone repository
	git clone git@github.com:<your-username>/ACEest_Fitness-and-Gym.git

	cd aceest_fitness

### 2. Create virtual environment
	python -m venv .venv
	# Windows PowerShell:
	.venv\Scripts\Activate.ps1
	# macOS/Linux:
	source .venv/bin/activate


### 3. Install dependencies
	pip install -r requirements.txt

### 4. Initialize the database
	flask --app app init-db

### 5. Run the application
	flask --app app run

	Visit: http://127.0.0.1:5000


## 🧪 Testing

To run tests, activate your virtual environment and execute:

	pytest -q

**Note**: Ensure the test database is set up in your environment variables.

## 🐳 Running with Docker

Build image

	docker build -t aceest-fitness .

Run container

	docker run --rm -p 5000:5000 aceest-fitness

Run tests inside container

	docker run --rm aceest-fitness pytest -q

---

## 📋 API Endpoints

| Route                  | Methods  | Description                                | Auth Required |
| ---------------------- | -------- | ------------------------------------------ | ------------- |
| `/`                    | GET      | Home page                                  | No            |
| `/signup`              | GET/POST | User registration                          | No            |
| `/login`               | GET/POST | User login                                 | No            |
| `/logout`              | GET      | User logout                                | Yes           |
| `/dashboard`           | GET/POST | Add/view workouts                          | Yes           |
| `/workouts`            | GET      | View all workouts                          | Yes           |
| `/health`              | GET      | Health check endpoint (returns status)     | No            |
| *(Planned)* `/profile` | GET/POST | Manage personal info (height, weight, BMI) | Yes           |

---

## 🗄️ Database Models

- **User**: id, username, password_hash, created_at
- **Workout**: id, user_id, workout, duration, date
- **StrengthWorkout**: id, user_id, exercise, reps, weight, date
- **CardioWorkout**: id, user_id, activity, duration, distance, calories, date
- **Profile**: (Planned) id, user_id, height_cm, weight_kg, age, profile_pic, bmi

---

## 🎨 UI Overview

- **Home Page**: Welcome, sign up/log in options
- **Dashboard**: Add/view strength & cardio workouts, progress graph
- **Workouts Page**: List of all workouts
- **Profile**: (Planned) Manage personal info and BMI

---

## 📝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes
4. Push to the branch
5. Open a pull request

---

## 📄 License

**ACEest Fitness & Gym Tracker is licensed under the GNU General Public License v3.0**

Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights.

**Permissions**
- Commercial use
- Modification
- Distribution
- Patent use
- Private use

**Limitations**
- Liability
- Warranty

**Conditions**
- License and copyright notice
- State changes
- Disclose source
- Same license

For full license text, see [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

---

## 🙋 FAQ

**Q: How do I reset the database?**  
A: Delete `database.db` and run `flask --app app init-db`.

**Q: How do I run tests?**  
A: Activate your virtual environment and run `pytest -q`.

**Q: How do I deploy with Docker?**  
A: See the Docker section above.

---

## 👨‍💻 Maintainers

- [Himanshu S Gautam](https://github.com/himanshugy2j)

---

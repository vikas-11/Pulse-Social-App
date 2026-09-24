# Pulse — Social Media Web Application

Pulse is a modern micro-social platform where users can share posts, upload images, interact through likes and comments, save posts, manage profiles, and discover content through a clean and responsive interface.

The project also includes a custom staff Control Center for content moderation and administration.

---

## ✨ Features

### User Features
- User registration, login, and logout
- Create, edit, and delete posts
- Upload images with posts
- Like and unlike posts
- Comment on posts
- Save and unsave posts
- Search posts and users
- User profile pages
- Profile avatar, bio, and location
- Edit profile information
- Pagination
- Light and dark themes
- Responsive desktop, tablet, and mobile interface
- Copy/share post links

### Admin / Staff Features
- Dedicated Control Center
- View posts from all users
- Search posts from the dashboard
- Edit any user's post
- Delete any user's post
- Moderate comments
- View platform activity statistics
- Staff-only moderation controls

---

## 🛠️ Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** SQLite
- **Image Handling:** Pillow
- **Authentication:** Django Authentication System
- **ORM:** Django ORM
- **Version Control:** Git & GitHub

---

## 📸 Screenshots

Add screenshots of your application inside a folder such as:

```text
screenshots/
├── home.png
├── login.png
├── profile.png
└── admin.png
```

Then display them here:

```markdown
![Home Page](screenshots/home.png)
![Profile Page](screenshots/profile.png)
![Admin Dashboard](screenshots/admin.png)
```

---

## 🚀 Live Demo

A deployed version can be added here after hosting:

```text
https://your-pulse-app.onrender.com
```

> GitHub stores the source code for this project. The live web application should be deployed to a Python-compatible hosting platform such as Render.

---

## 📁 Project Structure

```text
django_basics/
│
├── django_basics/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── tweet/
│   ├── migrations/
│   ├── templates/
│   │   └── tweet/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   ├── layout.html
│   └── registration/
│
├── static/
│   ├── styles.css
│   └── app.js
│
├── media/
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/pulse.git
cd pulse
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## 🔐 Environment Variables

For production, do not commit secrets directly to GitHub.

Example environment variables:

```env
DJANGO_SECRET_KEY=replace-with-a-secure-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com
```

---

## 🧑‍💼 Staff Control Center

Staff and superuser accounts can access the Control Center at:

```text
/admin/
```

A superuser can be created using:

```bash
python manage.py createsuperuser
```

---

## 🗃️ Core Models

### Tweet
Stores:
- Post author
- Text content
- Optional image
- Likes
- Bookmarks
- Creation and update timestamps

### Comment
Stores:
- Related post
- Comment author
- Comment content
- Creation timestamp

### Profile
Stores:
- User
- Avatar
- Bio
- Location

---

## 🌐 Deployment

This application requires a Python web server, so GitHub Pages cannot run it directly.

A suitable deployment flow is:

```text
Local Project
     ↓
GitHub Repository
     ↓
Render Web Service
     ↓
Public Live URL
```

For production deployment, consider:

- PostgreSQL instead of SQLite
- Environment variables for secrets
- `DEBUG=False`
- Production static-file configuration
- Gunicorn/Uvicorn
- Persistent media storage if users upload images

---

## 🔮 Future Improvements

Possible enhancements:

- Follow / unfollow users
- Notifications
- Direct messaging
- Hashtags
- Trending topics
- Infinite scrolling
- Email verification
- Password reset
- Social login
- Cloud image storage
- REST API
- Automated tests and CI/CD

---

## 🤝 Contributing

Contributions, issues, and feature suggestions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push the branch
5. Open a pull request

---

## 👨‍💻 Author

**Vikas Yadav**

Backend Developer | Python | Django | FastAPI | REST APIs

GitHub: `https://github.com/vikas-11`

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

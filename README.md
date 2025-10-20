# 🏋️‍♂️ CoachLink — Demo Version

A **modern coaching platform** built with **Django + DRF**, designed to connect users and coaches seamlessly. This demo showcases modular design, JWT authentication, internal chat, notifications, and scheduling — all containerized via **Docker Compose**.

---

## 🚀 Features Overview

### (a) **User Module** 👤

* Register & Login with **Email or Phone**
* Secure **JWT Authentication**
* Profile setup (photo, goals, activity type)
* Browse coaches via filters (field, experience, city)
* Direct messages to request collaboration

### (b) **Coach Module** 🧑‍🏫

* Register as a **Coach** and build a professional profile
* Add **descriptions**, **certifications**, and **specializations**
* Define **session price**, **currency**, and **duration**
* Receive and manage **session requests** from users
* Integrated admin dashboard for moderation

### (c) **Communication Section** 💬

* Simple internal **chat system** with threads
* Automatic **notifications** for new messages or session updates
* Lightweight **session calendar** (auto-sync on accepted requests)

---

## 🧩 Tech Stack

| Component     | Technology                  |
| ------------- | --------------------------- |
| Backend       | Django 5 + DRF              |
| Auth          | SimpleJWT (email / phone)   |
| DB            | PostgreSQL 16 (Dockerized)  |
| Cache / Queue | Redis 7                     |
| Media         | Pillow (for profile photos) |
| Environment   | django-environ              |

---

## 🐳 Quick Start (Docker Compose)

```bash
# clone the repo
git clone https://github.com/yourname/coachlink-demo.git
cd coachlink-demo

# build containers
docker compose build

# run migrations
docker compose run --rm web python manage.py migrate

# create superuser
docker compose run --rm web python manage.py createsuperuser

# start services
docker compose up
```

> App will be live at **[http://localhost:8000](http://localhost:8000)** 🌐

---

## 🔐 API Endpoints Summary

### 🔸 Auth (User)

```
POST   /api/auth/register/       → Sign up (email/phone + password)
POST   /api/auth/login/          → Login with email or phone
GET    /api/auth/me/             → Get current user info
```

### 🔸 Profiles

```
GET/PATCH  /api/profile/me/      → My profile
GET        /api/coaches/         → Filtered list of coaches
```

### 🔸 Coaches

```
POST   /api/coaches/become/                      → Register as a coach
GET    /api/coaches/me/                          → My coach profile
GET    /api/coaches/<user_id>/detail/            → Public coach detail
POST   /api/coaches/session-requests/send/       → Send session request
GET    /api/coaches/session-requests/incoming/   → View received requests
PATCH  /api/coaches/session-requests/<id>/status/→ Accept/Decline
```

### 🔸 Messaging

```
POST   /api/messages/send/        → Send direct message
GET    /api/threads/              → List all chat threads
GET    /api/threads/<id>/messages/→ Thread messages
```

### 🔸 Notifications

```
GET    /api/notifications/         → All notifications
GET    /api/notifications/unread-count/ → Count unread
PATCH  /api/notifications/<id>/read/   → Mark as read
```

### 🔸 Calendar

```
GET/POST /api/calendar/sessions/   → View or create sessions
```

---

## 🧠 Admin Panel Highlights

* Custom user model (`core.User`) — email/phone based
* Rich profile admin with photo preview
* Coach admin (search, verify flag, filters)
* Message & Notification tracking

Login at: **[http://localhost:8000/admin/](http://localhost:8000/admin/)** 🛡️

---

## 🧱 Folder Structure

```
coachlink/
├── core/            # Custom user + JWT auth
├── profiles/        # User profiles & filtering
├── coaches/         # Coach data & session requests
├── messaging/       # Chat + threads
├── notifications/   # Signals + alerts
├── calendarx/       # Session calendar (auto-sync)
├── config/          # Django settings & URLs
└── docker/          # Compose & entrypoints
```

---

## ❤️ Future Enhancements

* Real-time WebSocket chat (Channels)
* Push notifications & email alerts
* Advanced calendar with reminders
* Stripe/PayPal integration for session payments

---

### 🏁 Demo Summary

> CoachLink is modular, clean, and scalable — a perfect foundation for a real coaching marketplace.

🪶 **Made with Python, Docker, and a lot of ☕.**

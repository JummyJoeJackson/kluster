# Kluster

Kluster is a full-stack web platform for tracking and managing user collections. Built with Python and Flask, Kluster provides secure user authentication and robust, scalable database operations through SQLAlchemy.

***

## Table of Contents

- [Features](#features)
- [Access Instructions](#access-instructions)
- [Getting Started](#getting-started)
- [Coming Soon](#coming-soon)

***

## Features

- User registration, authentication, and session management
- Persistent collection tracking (add, view, edit, delete items)
- Modern, responsive web interface
- Robust backend API using Flask
- Data persistence with SQLAlchemy
- Modular Flask blueprint architecture

***

## Access Instructions

- For local deployment, follow the steps under "Getting Started".
- To access the live production site, visit:
`https://kluster-flax.vercel.app/`
- For developer/admin access, contact the project maintainer.

***

## Getting Started

1. **Clone the repository**

```
git clone https://github.com/yourusername/kluster-repo.git
cd kluster-repo
```

2. **Install dependencies**

```
pip install -r requirements.txt
```

3. **Set up your environment**
    - Copy `.env.example` to `.env` and configure accordingly.
4. **Initialize the database**

```
flask db upgrade
```

5. **Run the application**

```
flask run
```

    - Visit `http://localhost:5000` in your browser.

***

## Coming Soon

- User-to-user messaging notifications
- Advanced search and filtering
- REST API for mobile integration
- Data export (CSV/JSON)
- Customizable themes and user profiles

***

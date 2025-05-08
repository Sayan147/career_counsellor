# Career Guidance Application

A FastAPI-based web application for career guidance and profile management. This application helps users manage their profiles, explore career options, and interact with a career guidance system.

## 🚀 Features

- User Authentication and Authorization
- Profile Management
- Career Guidance System
- Interactive Dashboard
- Chat Functionality
- Responsive Web Interface

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Templates**: Jinja2
- **Data Storage**: CSV-based storage system
- **Static Files**: CSS and JavaScript assets

## 📁 Project Structure

```
├── app/
│   ├── api/           # API endpoints and routers
│   ├── core/          # Core application logic
│   ├── db/            # Database and storage management
│   ├── models/        # Data models
│   ├── services/      # Business logic services
│   └── main.py        # Application entry point
├── data/
│   ├── chats.csv      # Chat history data
│   ├── profiles.csv   # User profiles data
│   └── users.csv      # User authentication data
├── static/
│   ├── css/          # Stylesheets
│   └── js/           # JavaScript files
└── templates/
    ├── index.html    # Landing page
    ├── dashboard.html # User dashboard
    └── profile.html  # Profile management page
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5200 --reload
```

The application will be available at `http://localhost:5200`

## 🔑 API Endpoints

- `/auth` - Authentication endpoints
- `/career` - Career guidance related endpoints
- `/api/profile` - Profile management endpoints
- `/dashboard` - Dashboard interface
- `/profile` - Profile management interface

## 📝 Data Structure

The application uses CSV files for data storage:
- `users.csv`: Stores user authentication information
- `profiles.csv`: Contains user profile data
- `chats.csv`: Stores chat history and interactions

## 🔒 Security

- CORS is configured to allow requests from localhost
- Authentication system in place
- Secure password handling

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## 👥 Authors

- Sayan Chakraborty  - Initial work

## 🙏 Acknowledgments

- FastAPI documentation
- Jinja2 templating engine

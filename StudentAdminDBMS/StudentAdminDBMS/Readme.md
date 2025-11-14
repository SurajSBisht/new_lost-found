# Lost and Found Management System

## Overview
A comprehensive database-driven Lost and Found Management System built with Python Flask backend, PostgreSQL database, and modern responsive frontend. The system helps users report, track, and recover lost items in campus or organizational settings.

## Project Status
**Current State:** Fully functional MVP with all core features implemented and tested.

## Recent Changes (November 11, 2025)
- Created PostgreSQL database with normalized schema (3NF)
- Implemented Flask backend with authentication and session management
- Built automated matching algorithm with similarity scoring
- Created modern responsive frontend with role-based dashboards
- Set up workflows and verified all features working correctly

## Technology Stack
- **Backend:** Python 3.11, Flask 3.0.0, Flask-Login
- **Database:** PostgreSQL (Replit managed)
- **Frontend:** HTML5, CSS3, JavaScript
- **Authentication:** Flask-Login with Werkzeug password hashing
- **Server:** Flask development server (port 5000)

## Database Architecture
Normalized PostgreSQL database with 5 main tables:

1. **users** - User accounts with role-based access (student/admin)
2. **lost_items** - Records of items reported as lost
3. **found_items** - Records of items reported as found
4. **match_table** - Many-to-many matches between lost and found items
5. **notifications** - User notifications for potential matches

### Key Features:
- Automated triggers for timestamp updates
- Indexes for optimized query performance
- Foreign key relationships for data integrity
- Check constraints for data validation

## User Roles

### Student Role
- Report lost items with detailed descriptions
- Report found items they discover
- View personal submissions and status
- Receive notifications for potential matches
- Track item recovery progress

### Admin Role
- Full access to all lost and found records
- View all registered users
- Update item statuses (unfound/found/resolved)
- Verify matches between items
- Access system statistics dashboard
- Manage and resolve cases

## Core Features

### 1. Authentication System
- Secure login/registration with password hashing
- Role-based access control (student/admin)
- Session management with Flask-Login
- Protected routes based on user roles

### 2. Item Reporting
- Comprehensive forms for lost/found items
- Category selection (Electronics, Documents, Books, etc.)
- Location and date tracking
- Detailed description fields

### 3. Automated Matching Algorithm
Calculates similarity scores based on:
- Category matching (30% weight)
- Item name similarity (25% weight)
- Description keyword matching (20% weight)
- Location proximity (15% weight)
- Date proximity (10% weight)

Automatically creates notifications when match score ≥ 40%

### 4. Notification System
- Real-time notifications for potential matches
- Unread notification tracking
- Mark as read functionality
- Notification history

### 5. Admin Dashboard
- Statistics overview (total items, matches, users)
- Complete item management
- Status updates for lost/found items
- User management and activity tracking

### 6. Modern UI/UX
- Responsive design for all screen sizes
- Clean, professional interface
- Tab-based navigation
- Color-coded status badges
- Gradient backgrounds and modern styling

## Demo Accounts
- **Admin:** username: `admin`, password: `admin123`
- **Student 1:** username: `john_doe`, password: `student123`
- **Student 2:** username: `jane_smith`, password: `student123`

## Project Structure
```
/
├── app.py                  # Main Flask application
├── app/
│   ├── __init__.py        # App package marker
│   └── database.py        # Database operations class
├── templates/             # HTML templates
│   ├── login.html
│   ├── register.html
│   ├── student_dashboard.html
│   └── admin_dashboard.html
├── static/                # Static assets
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   └── js/
│       └── dashboard.js  # Dashboard interactivity
├── database_schema.sql    # Database schema definition
├── requirements.txt       # Python dependencies
└── .gitignore            # Git ignore rules
```

## Environment Variables
- `DATABASE_URL` - PostgreSQL connection string (auto-configured)
- `SESSION_SECRET` - Flask session secret key
- `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE` - Database credentials

## Running the Application
The Flask server runs automatically on port 5000 via the configured workflow.

## Database Management
All database operations use parameterized queries for security. The Database class handles:
- Connection pooling
- Transaction management
- CRUD operations for all tables
- Complex queries with joins
- Error handling and rollback

## Future Enhancements
- Email/SMS notifications for matches
- Advanced text similarity algorithms (fuzzy matching)
- Image upload for items
- Admin reporting and analytics dashboard
- QR code generation for items
- Mobile app version
- Search and filter functionality

## Security Features
- Password hashing with Werkzeug (scrypt)
- SQL injection prevention (parameterized queries)
- CSRF protection
- Role-based access control
- Session management
- Input validation

## Design Principles
- Database normalization (3NF)
- Clean code architecture
- Separation of concerns
- Responsive design
- User-friendly interface
- DBMS-oriented approach


# EduText Backend

Backend API service for EduText - A digital textbook management system for Yaba College of Technology.

## Features

- 📚 Textbook Management
- 🛒 Order Processing
- 👥 User Authentication & Authorization
- 📊 Sales & Inventory Reports
- 🔍 Search & Filtering
- 📱 RESTful API

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- pip

### Installation

1. Clone the repository
2. Install dependencies
3. Configure database settings
4. Run migrations
5. Start the server


## 📁 Project Structure
backend/
├── api/ # Main API application
│ ├── views/ # API views and viewsets
│ ├── serializers/ # Data serializers
│ ├── models/ # Database models
│ └── urls.py # API URL configurations
├── core/ # Core application settings
├── media/ # User uploaded files
├── static/ # Static files
└── manage.py # Django management script

## 🔑 Environment Variables

Create a `.env` file in the root directory with the following variables:

env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/edutext
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000



## API Documentation

## 📚 API Endpoints

### Authentication
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/register/` - User registration
- `GET /api/v1/auth/profile/` - Get user profile

### Textbooks
- `GET /api/v1/textbooks/` - List all textbooks
- `POST /api/v1/textbooks/` - Create new textbook
- `GET /api/v1/textbooks/{id}/` - Get textbook details
- `PUT /api/v1/textbooks/{id}/` - Update textbook
- `DELETE /api/v1/textbooks/{id}/` - Delete textbook

### Orders
- `GET /api/v1/orders/` - List all orders
- `POST /api/v1/orders/` - Create new order
- `GET /api/v1/orders/{id}/` - Get order details
- `PUT /api/v1/orders/{id}/` - Update order status

### Reports
- `GET /api/v1/reports/sales/` - Generate sales report
- `GET /api/v1/reports/low-stock/` - Generate low stock report

## 🔒 Security

- JWT Authentication
- CORS configuration
- Request rate limiting
- Input validation and sanitization

## 📊 Database Schema

### Textbook
- id (UUID)
- title (String)
- course_code (String)
- department (String)
- level (String)
- price (Decimal)
- stock (Integer)
- description (Text)
- created_at (DateTime)
- updated_at (DateTime)

### Order
- id (UUID)
- reference (String)
- student (ForeignKey)
- items (ManyToMany)
- total_amount (Decimal)
- status (String)
- created_at (DateTime)
- updated_at (DateTime)

### User
- id (UUID)
- email (String)
- full_name (String)
- role (String)
- department (String)
- level (String)

## 🧪 Testing

coverage report

## 📝 Development Guidelines

1. Follow PEP 8 style guide
2. Write tests for new features
3. Update documentation when adding endpoints
4. Use meaningful commit messages
5. Create feature branches for new development

## 🔧 Troubleshooting

Common issues and solutions:

1. Database connection errors
   - Check PostgreSQL service is running
   - Verify database credentials in .env

2. Migration errors
   - Delete migrations and recreate
   - Reset database if in development

3. CORS issues
   - Check CORS_ALLOWED_ORIGINS in settings
   - Verify frontend origin

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details
# MKC Fitness - Professional Gym Membership Management System

A comprehensive, modern gym membership management system built with Flask and MySQL. This system provides complete functionality for managing gym members, trainers, attendance, payments, and more.

## 🚀 Features

### Core Features
- **Member Management**: Add, view, edit, and manage gym members
- **Trainer Management**: Manage fitness trainers and their specializations
- **Membership Plans**: Flexible membership plans with different durations and pricing
- **Attendance Tracking**: Real-time check-in/check-out system
- **Payment Management**: Track payments and billing
- **Admin Dashboard**: Comprehensive analytics and management interface

### Advanced Features
- **Responsive Design**: Modern, mobile-friendly interface
- **Real-time Statistics**: Live dashboard with key metrics
- **Search & Filter**: Advanced search and filtering capabilities
- **Security**: Admin authentication and authorization
- **Data Validation**: Comprehensive form validation
- **Modern UI**: Beautiful, animated interface with gradient effects

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with CSS Grid and Flexbox
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Poppins)

## 📋 Prerequisites

- Python 3.7 or higher
- MySQL 5.7 or higher
- pip (Python package installer)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gym-membership-management
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL database**
   - Create a MySQL database
   - Update database credentials in `app.py`
   - Run the SQL script to create tables:
   ```bash
   mysql -u root -p < database_setup.sql
   ```

4. **Configure the application**
   - Update database connection details in `app.py`
   - Change the secret key for production use

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - Use admin credentials to access the admin panel

## 🗄️ Database Schema

The system includes the following main tables:

- **admin_users**: System administrators and staff
- **members**: Gym members with personal and membership information
- **trainers**: Fitness trainers and their specializations
- **membership_plans**: Available membership plans and pricing
- **payments**: Payment tracking and billing
- **attendance**: Member check-in/check-out records
- **classes**: Group fitness classes
- **class_schedules**: Class scheduling
- **class_bookings**: Member class bookings
- **equipment**: Gym equipment management
- **equipment_maintenance**: Equipment maintenance records
- **notifications**: System notifications
- **system_settings**: Application configuration

## 🎯 Usage

### Admin Login
- Navigate to `/admin/login`
- Use the default admin credentials (update in production)
- Access the comprehensive admin dashboard

### Member Management
- Add new members with complete information
- Track membership status and expiration
- Manage trainer assignments
- View member statistics and analytics

### Attendance Tracking
- Real-time check-in/check-out system
- Track member visit duration
- Monitor daily attendance statistics
- Generate attendance reports

### Payment Management
- Track membership payments
- Monitor revenue and billing
- Handle different payment methods
- Generate financial reports

## 🎨 Customization

### Styling
- Modify `static/style.css` for custom styling
- Update color variables in CSS for brand colors
- Customize animations and effects

### Database
- Add new fields to existing tables
- Create additional tables for new features
- Modify membership plans and pricing

### Features
- Add new admin routes in `app.py`
- Create additional templates for new pages
- Implement new functionality as needed

## 🔒 Security Features

- Admin authentication system
- Password hashing
- Session management
- Input validation and sanitization
- SQL injection prevention

## 📱 Responsive Design

The system is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- Various screen sizes

## 🚀 Deployment

### Production Deployment
1. Update database credentials
2. Change secret key
3. Set up proper MySQL database
4. Configure web server (Nginx/Apache)
5. Use WSGI server (Gunicorn)
6. Set up SSL certificates
7. Configure domain and DNS

### Environment Variables
Create a `.env` file for production:
```
DB_HOST=your-db-host
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=your-db-name
SECRET_KEY=your-secret-key
```

## 📊 Admin Dashboard Features

- **Statistics Overview**: Total members, trainers, daily attendance, revenue
- **Quick Actions**: Easy access to common tasks
- **Recent Activity**: Latest members and upcoming classes
- **Real-time Updates**: Live data and statistics

## 🎯 Future Enhancements

- Mobile app integration
- Email/SMS notifications
- Advanced reporting and analytics
- Equipment booking system
- Class scheduling improvements
- Member portal
- Payment gateway integration
- API development

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🎉 Acknowledgments

- Flask framework for the web framework
- MySQL for the database
- Font Awesome for icons
- Google Fonts for typography
- Modern CSS techniques for styling

---

**MKC Fitness Management System** - Professional gym management made simple and efficient.
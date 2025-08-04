# 🏢 Warehouse Management System

A comprehensive warehouse management system built with Python Flask and modern web technologies. This system allows administrators to set up warehouse configurations, manage products, receive items, pick items, and generate detailed reports.

## 🚀 Features

### Core Functionality
- **Warehouse Setup**: Configure warehouse dimensions (aisles × tiers matrix)
- **Product Management**: Add and manage products with SKU tracking
- **Item Receiving**: Receive items from dock and automatically place in available locations
- **Item Picking**: Pick items from specific aisle/tier locations
- **Visual Warehouse View**: Interactive grid showing product locations
- **Comprehensive Reports**: Occupancy statistics and transaction history

### Key Features
- **Automatic Location Assignment**: Items are automatically placed in the first available location
- **Real-time Updates**: Warehouse view updates immediately after operations
- **Transaction Tracking**: All receive and pick operations are logged
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Beautiful, intuitive interface with smooth animations

## 📋 Requirements

- Python 3.7 or higher
- Flask
- Flask-SQLAlchemy
- Flask-CORS

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the system**:
   Open your web browser and navigate to `http://localhost:5000`

## 📖 Usage Guide

### 1. Warehouse Setup
1. Navigate to the "Warehouse Setup" tab
2. Enter warehouse name and dimensions:
   - **Aisles**: Number of horizontal layers (e.g., 5)
   - **Tiers**: Number of vertical layers (e.g., 3)
3. Click "Setup Warehouse" to create the warehouse structure

### 2. Product Management
1. Go to the "Products" tab
2. Add products with:
   - **Product Name**: Descriptive name
   - **SKU**: Unique stock keeping unit
   - **Description**: Optional product details
3. Click "Add Product" to save

### 3. Receiving Items
1. Navigate to "Receive Items" tab
2. Select a product from the dropdown
3. Enter the quantity to receive
4. Click "Receive Items" - the system will automatically find an available location

### 4. Picking Items
1. Go to "Pick Items" tab
2. Enter the specific aisle and tier numbers
3. Specify the quantity to pick
4. Click "Pick Items" to remove items from that location

### 5. Warehouse View
1. Click "Warehouse View" tab
2. See a visual representation of your warehouse:
   - **Green cells**: Occupied locations with product details
   - **Gray cells**: Available locations
   - **Click any cell**: View detailed information about that location

### 6. Reports
1. Navigate to "Reports" tab
2. View:
   - **Occupancy Statistics**: Total, occupied, and available locations
   - **Transaction History**: Complete log of all receive and pick operations

## 🗄️ Database Schema

### Tables
- **Warehouse**: Stores warehouse configuration (name, aisles, tiers)
- **Product**: Product catalog with SKU tracking
- **Location**: Individual storage locations (aisle/tier combinations)
- **Transaction**: Log of all receive and pick operations

### Key Relationships
- Each warehouse has multiple locations (aisles × tiers)
- Locations can be occupied by products
- All operations create transaction records

## 🔧 API Endpoints

### Warehouse Management
- `GET /api/warehouse` - Get current warehouse configuration
- `POST /api/warehouse` - Setup new warehouse

### Product Management
- `GET /api/products` - List all products
- `POST /api/products` - Add new product

### Operations
- `GET /api/locations` - Get all warehouse locations
- `POST /api/receive` - Receive items (auto-assign location)
- `POST /api/pick` - Pick items from specific location

### Reports
- `GET /api/reports/occupancy` - Get occupancy statistics
- `GET /api/reports/transactions` - Get transaction history

## 🎯 Business Logic

### Location Assignment
- Items are automatically placed in the first available location
- If no locations are available, the system returns an error
- Users cannot manually choose locations during receiving

### Quantity Management
- Each location can hold one product type with a quantity
- When quantity reaches zero, the location becomes available again
- Partial picking is supported

### Data Integrity
- SKU must be unique across all products
- All operations are logged in transaction history
- Warehouse setup clears existing data

## 🎨 UI Features

### Modern Design
- Responsive layout that works on all devices
- Smooth animations and hover effects
- Color-coded warehouse grid (green = occupied, gray = available)
- Interactive modals for location details

### User Experience
- Tabbed interface for easy navigation
- Real-time feedback with success/error messages
- Auto-hiding alerts after 5 seconds
- Intuitive form validation

## 🔒 Security Features

- Input validation on all forms
- SQL injection protection via SQLAlchemy
- CORS enabled for API access
- Error handling for all operations

## 📱 Mobile Support

The interface is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set up a production web server (nginx, Apache)
2. Use a WSGI server (gunicorn, uwsgi)
3. Configure environment variables for production settings
4. Set up a proper database (PostgreSQL, MySQL) instead of SQLite

## 🐛 Troubleshooting

### Common Issues
1. **Port already in use**: Change the port in `app.py` line 200
2. **Database errors**: Delete `warehouse.db` and restart the application
3. **CORS issues**: Ensure Flask-CORS is properly installed

### Logs
Check the console output for detailed error messages and debugging information.

## 📈 Future Enhancements

Potential improvements for future versions:
- User authentication and role-based access
- Barcode scanning integration
- Advanced inventory forecasting
- Multi-warehouse support
- Export reports to PDF/Excel
- Real-time notifications
- Mobile app companion

## 📄 License

This project is open source and available under the MIT License.

---

**Happy Warehousing! 🏢📦** 

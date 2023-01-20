
# Tech Shop

A fully functional Ecommerce Application for selling and purchasing Mobiles,
Laptops and Headphones

## Technologies Used

- Python
- Django
- Postgres SQL
- Jinja Templating
- HTML
- CSS
- Nginx
- Gunicorn

## Services Used
- AWS
- Razorpay
- Paypal

## Features

#### User Side

- Guest user
- Login with OTP
- Reset User Password
- User Profile
- Edit User Details
- Multiple Address Management
- Search Products
- Filter and Sort Products
- Image Zooming
- User Cart and Wishlist
- User Checkout
- Multiple Checkout Options
- Online Payment via Razorpay and Paypal
- Order History
- Cancel or Return an Order
- Invoice for delivered Products

#### Admin Side

- Admin Dashboard with charts
- Multiple Image Upload
- Category,Brand,Product Management
- User Block/Unblock
- Image Cropping
- View User Orders
- Change Order Status
- Coupon,Offer Management
- Sales Report
- Download Sales Report in excel and pdf
- Sort Sales Report based on year, month, dates

## Deployment

#### To deploy this project run

Clone the github repository:

```bash
  https://github.com/ramshadvv/ecommerce_project.git
```

Go to the project directory:

```bash
  cd ecommerce_project
```

Create virtualenv:

```bash
  python3 -m venv env
```

Activate environment:

```bash
  env/Scripts/activate
```

install dependencies:

```bash
  pip install -r requirements.txt
```

Add .env file to the folder:

```bash
  Assign values to SECRET_KEY, SQL_PASSWORD
  
  For razorpay ACCOUNT_SID, AUTH_TOKEN, services, KEY_ID, KEY_SECRET
```

Migarte all models:

```bash
  python manage.py makemigrations
  python manage.py migrate
```

Start the server:

```bash
  python manage.py runserver
```

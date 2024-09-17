# AutoMart E-Commerce Backend System

## Overview
This e-commerce backend system is built with Django and Django REST Framework (DRF) to manage products, sales, and purchases. It includes JWT-based authentication, with OAuth2.0 configurations also available but not in use. The system features product management, sales/purchase orders, low stock notifications, and scheduled tasks to notify the admin when inventory is low. Docker is used to ease deployment and scalability. You can also access the API documentation via Swagger/DRF docs at `127.0.0.1:8080/en/docs` and test email functionality using Mailpit at `http://localhost:8025/`.

## Table of Contents
- [Overview](#overview)
- [Business flow](#Business_Logic_and_Flow)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Build_docker_images](#Build_docker_images)
- [Deployment](#Deployment)
- [Postman Collection](#postman-collection)

## Requirements
- Python 3.x
- pip
- Docker
- Redis
- PostgreSQL

## Business_Logic_and_Flow

### Product Management
The system allows full CRUD operations for managing products in the store. Each product contains fields like `name`, `description`, `price`, and `stock`. The unique identifier for products is the `SKU` (Stock Keeping Unit). When a product is created or updated, the inventory is adjusted accordingly.

- **Create/Update Product**: Admin users can create and update product information, ensuring that all necessary details such as the name, description, price, and stock are filled.
- **Delete Product**: Only admin users are authorized to delete products from the system.
- **List Products**: Both admin and regular users can list available products.
- **Retrieve Product**: Individual product details can be retrieved by both regular users and admin.

### Sales Flow
The system manages the sales process by allowing authenticated users to place orders for available products. When a sales order is created, the stock of the product is automatically decreased according to the quantity sold.

- **Create Sales Order**: Authenticated users can create a sales order with details like the product, quantity, price, and customer information. After the sale, the product’s stock is decreased accordingly.
- **List Sales Orders**: Admin users can view all sales orders in the system. Regular users can only view their own sales orders.
- **Retrieve Sales Order**: Individual sales orders can be retrieved by users if they are the ones who created the order. Admin users have access to view all sales orders.
- **Delete Sales Order**: Only admin users are authorized to delete sales orders.

### Purchases Flow
Purchases allow the business to restock inventory. When a purchase order is created, the stock of the product is increased by the specified quantity.

- **Create Purchase Order**: Admin and authorized staff members can create a purchase order to restock inventory. The purchase order specifies the product, quantity, supplier name, and purchase date. Once a purchase is made, the product’s stock is automatically increased.
- **List Purchase Orders**: Admin and staff can view all purchase orders.
- **Retrieve Purchase Order**: Admin and staff can retrieve details of individual purchase orders.
- **Delete Purchase Order**: Admin users can delete purchase orders.

### Inventory Management
The inventory management system is automated to handle stock changes after successful sales and purchases. Additionally, the system periodically checks for products that have low stock levels (e.g., less than 5 units) and generates notifications for the admin.

- **Low Stock Notifications**: When the stock of a product falls below a defined threshold (e.g., 5), a notification is created in the system. Admin users can view these notifications to take appropriate action such as restocking.
- **Scheduled Task**: A cron job is implemented to periodically check product stock levels. If a product falls below the threshold, a notification is triggered and stored in the database for the admin to review.

### Authentication and Authorization
The system uses **JWT-based authentication** to secure the API. All endpoints are protected, and only authenticated users can access them. Admin and staff permissions are enforced on critical actions such as product management, order deletion, and purchase creation.

- **JWT Authentication**: The system ensures that users must log in and receive a token before interacting with the API.
- **Authorization**: Different permission levels are enforced to protect sensitive operations:
    - **Admin**: Full access to all operations (product management, sales and purchase order management, inventory notifications).
    - **Staff**: Can manage purchases but not products.
    - **Customers**: Can create and view their own sales orders but have no access to product or purchase management.

### Notifications Flow
Notifications are created when product stock is low. The notification contains the product name, a message indicating the low stock level, and the current stock value.

- **View Notifications**: Admin users can view all notifications through a dedicated API endpoint.
- **Delete Notifications**: Admin users are also authorized to delete notifications once they have been handled.



## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/Abdurahman-hassan/AutoMart
    cd AutoMart
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements/requirements.txt
    ```

## Configuration
1. Copy the `.env.template` and `.admin.template` files to `.env` and `.admin`, and fill in the required values:
    ```sh
    cp .envs/.env.template .envs/.env
    cp .envs/.admin.template .envs/.admin
    ```

2. Edit the `.env` and `.admin` files:
    ```sh
    nano .envs/.env
    nano .envs/.admin
    ```

3. Set up your configurations for professional JWT. OAuth2.0 configuration is available but not in use.

## Build_docker_images
1. Build and run Docker containers for development:
 ```sh
 docker-compose -f docker-compose.dev.yml up --build -d
 ```

## inside_Docker
1. Run the following command to create a superuser:
    ```sh
    just create-admin
    ```
   
1. Make and apply migrations:
    ```sh
    just migrate
    ```

2. Seed the database with initial data:
    ```sh
    just seed
    ```

3. Collect static files:
    ```sh
    just collectstatic
    ```

### Deployment

1. Build and run Docker containers for Gunicorn production:
    ```sh
    just gunicorn-docker up --build -d
    ```

2. Build and run Docker containers for uWSGI production:
    ```sh
    just uwsgi-docker up --build -d
    ```

3. Stop Docker containers:
    ```sh
    docker-compose down
    ```

## You_can_access
1. Access the app at `http://localhost:8080/en/`.

2. Access Mailpit for email testing at:
    ```sh
    http://localhost:8025/
    ```
3. Access the API documentation via Swagger at:
    ```sh
    http://localhost:8080/en/docs/
    ```

## Postman Collection
- A Postman collection is provided in the repository. You can import this collection into Postman to test the API endpoints.
- Follow these steps:
    1. Open Postman.
    2. Click "Import" and select the provided Postman collection.
    3. Test the available endpoints.


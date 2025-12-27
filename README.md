# SellTools

**SellTools** is a Django-based e-commerce platform designed to facilitate online product sales, featuring specific integrations for the Ethiopian market.

## Project Overview

*   **Framework**: Django 5.2
*   **Database**: MySQL
*   **Frontend**: Bootstrap 4, Alpine.js, HTMX, jQuery
*   **Asset Management**: Webpack

## Key Features

### 1. Store Management (`store` app)
*   **Product Catalog**: Manage products with detailed attributes (price, weight, categories).
*   **Shopping Experience**: Full cart functionality, product ratings, and discount management.
*   **Payments**:
    *   Built-in payment tracking models.
    *   Integrations for **Chapa**.

### 2. User Management (`users` app)
*   **Authentication**:
    *   Primary login via **Phone Number** (Ethiopian format).
    *   Social login support for **Google** and **Telegram**.
*   **Profiles**: User profiles with location, age, and image support.

### 3. Administration (`manager` app)
*   Dedicated dashboard/interface for store management.
*   API endpoints for management tasks.

### 4. Real-time Capabilities
*   WebSocket support for real-time features (e.g., notifications, updates).

## Tech Stack Details

*   **Backend**: Python, Django, Django REST Framework
*   **Frontend**: HTML5, CSS3 (Bootstrap), JavaScript (Alpine.js, HTMX)
*   **Dependencies**: Managed via `uv` / `pip` (see `pyproject.toml`)

## ENV requirments

### For Chapa Pay
* publickey 
* secretkey 

### Django specfic Settings

* SECRET_KEY 
* DEBUG 
* DB_NAME
* DB_USER
* DB_PASSWORD
* DB_HOST
* DB_PORT

### For Google Auth
* GOOGLE_CLIENT_ID 
* GOOGLE_SECRET
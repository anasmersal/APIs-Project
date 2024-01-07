# Django Project: Restaurant Management API

## Overview

This Django project comprises various API views for managing menu items, users, carts, and orders within a restaurant context.

## Views Description

### Menu Items View

- `multiple_items(request)`: Handles GET requests to fetch multiple menu items or POST requests to add new menu items.
- `single_item(request, id)`: Handles GET, PUT, PATCH, and DELETE requests for a single menu item by its ID.

### Managers and Delivery Crew View

- `managers(request, user_id=None)`: Manages manager users, allowing GET, POST, and DELETE operations.
- `delivery_crew(request, user_id=None)`: Manages delivery crew users, allowing GET, POST, and DELETE operations.

### Cart and Order View

- `cart(request, user_id=None)`: Manages cart items, allowing GET, POST, and DELETE operations.
- `order(request, user_id=None)`: Manages orders, allowing GET and POST operations.

### Single Order View

- `single_order(request, id)`: Handles GET, PUT, PATCH, and DELETE requests for a single order by its ID.

## Permissions

- `IsAdminUser`: Permission class used in various views to control access to specific functionalities (e.g., manager, delivery crew, and authenticated user permissions).

## Usage

- The API endpoints provided in these views allow CRUD operations for managing menu items, users, carts, and orders within the restaurant system.
- The permissions assigned to different user groups (Managers, Delivery Crew) ensure controlled access to specific functionalities.

## Note

- This README offers an overview of the project's API views, their functionalities, and the permissions required for different user groups. It provides a concise summary of the API endpoints available in this Django project.

# Product Catalog API

This repository contains a RESTful API for managing a product catalog. Built with FastAPI, PostgreSQL, and SQLAlchemy, it provides a robust foundation for creating, reading, updating, and deleting users and products. The entire application is containerized using Docker and Docker Compose for a simplified setup and deployment process.

## Features

*   **Modern Python Backend**: Built with Python 3.13 and the high-performance FastAPI framework.
*   **Asynchronous Support**: Leverages `asyncpg` and SQLAlchemy's async capabilities for non-blocking database operations.
*   **JWT Authentication**: Secure authentication system with role-based access control.
*   **Role-Based Authorization**: Admin and anonymous user roles with different permission levels.
*   **Containerized Environment**: Fully containerized with Docker and orchestrated with Docker Compose for consistency across development and production environments.
*   **Database Migrations**: Uses `dbmate` for clear, simple, and plain SQL database migrations.
*   **Data Validation**: Employs Pydantic for robust data validation and serialization.
*   **Structured Project**: A clean and organized project structure that separates concerns like database logic, API endpoints, and business logic.
*   **Custom Exception Handling**: Provides clear, user-friendly error messages for request validation failures.

<!-- > [!IMPORTANT]
> TODO
> Users auth.
> Users notified when item is updated by admin. -->

## Technology Stack

*   **Framework**: FastAPI
*   **Database**: PostgreSQL
*   **ORM**: SQLAlchemy 2.0 (async)
*   **Containerization**: Docker, Docker Compose
*   **Data Validation**: Pydantic
*   **Migrations**: Dbmate
*   **Web Server**: Uvicorn

## Getting Started

Follow these instructions to get the project running on your local machine.

### Prerequisites

*   [Docker](https://www.docker.com/get-started)
*   [Docker Compose](https://docs.docker.com/compose/install/)

### Installation & Configuration

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/carlosochoa8/catalog_api.git
    cd catalog_api
    ```

2.  **Create an environment file:**
    Create a `.env` file in the root directory of the project by copying the example below. These variables are used by Docker Compose to configure the services.

    ```env
    # Application Image Name
    IMAGE_NAME=catalog_api

    # PostgreSQL Configuration
    POSTGRES_PORT=5432
    POSTGRES_HOST=db
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_NAME=postgres

    # Database URLs
    DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_NAME}
    DATABASE_URL_DBMATE=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_NAME}?sslmode=disable

    # JWT Configuration
    AUTH_SECRET_KEY=your-super-secret-key-here
    AUTH_ALGORITHM=HS256
    AUTH_ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

### Running the Application

1.  **Build and run the services using Docker Compose:**
    ```sh
    docker-compose up --build
    ```
    This command will:
    *   Build the Docker image for the FastAPI application (`catalog-service`).
    *   Start the PostgreSQL database container (`db`).
    *   Run database migrations automatically using the `migration` service.
    *   Start the FastAPI application.

2.  **Access the API:**
    The API will be available at `http://localhost:8080`. The interactive API documentation (Swagger UI) can be accessed at `http://localhost:8080/docs`.

## API Endpoints

The API is served under the `/catalog_api` root path.

### Health Check

*   **GET** `/catalog_api/`

Returns a simple JSON response to indicate that the service is running.

**Success Response (200 OK):**
```json
{
  "Message": "Ok"
}
```

### Authentication

*   **POST** `/catalog_api/authenticate/`

Authenticates a user and returns a JWT access token.

**Request Body:**
```json
{
  "email": "admin@example.com",
  "password": "YourPassword123!"
}
```

**Success Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Users

> [!NOTE]  
> User creation requires admin authentication. Include the JWT token in the Authorization header: `Authorization: Bearer <token>`

*   **POST** `/catalog_api/users/` 🔒 **Admin Only**

Creates a new user in the system. Only admin users can create other users.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "password": "SecurePass123!",
  "user_type": "anonymous"
}
```

**Success Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "newuser@example.com",
  "user_type": "anonymous",
  "created_at": "2025-08-13 20:15:30",
  "updated_at": "2025-08-13 20:15:30"
}
```

### Products

*   **POST** `/catalog_api/products/` 🔒 **Admin Only**

Creates a new product in the system.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "sku": "PROD-001",
  "name": "Sample Product",
  "price": 99.99,
  "brand": "Nike"
}
```

**Success Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "sku": "PROD-001",
  "name": "Sample Product",
  "price": 99.99,
  "brand": "Nike",
  "created_at": "2025-08-13 20:15:30",
  "updated_at": "2025-08-13 20:15:30"
}
```

*   **GET** `/catalog_api/products/{product_id}` 🌐 **Public**

Retrieves product information by ID. Available to all users (no authentication required).

**Success Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "sku": "PROD-001",
  "name": "Sample Product",
  "price": 99.99,
  "brand": "Nike",
  "created_at": "2025-08-13 20:15:30",
  "updated_at": "2025-08-13 20:15:30"
}
```

*   **PUT** `/catalog_api/products/{product_id}` 🔒 **Admin Only**

Updates an existing product.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "name": "Updated Product Name",
  "price": 149.99
}
```

**Success Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "sku": "PROD-001",
  "name": "Updated Product Name",
  "price": 149.99,
  "brand": "Nike",
  "created_at": "2025-08-13 20:15:30",
  "updated_at": "2025-08-13 20:25:45"
}
```

*   **DELETE** `/catalog_api/products/{product_id}` 🔒 **Admin Only**

Deletes a product from the system.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Success Response (204 No Content)**

## Authentication & Authorization

The API uses JWT (JSON Web Tokens) for authentication and role-based access control:

*   **Anonymous Users**: Can only retrieve product information (GET endpoints)
*   **Admin Users**: Can create, update, and delete users and products

### Password Requirements

Passwords must meet the following criteria:
*   8-25 characters long
*   At least one uppercase letter
*   At least one lowercase letter
*   At least one number
*   At least one special character (!@#$%&*._)
*   No spaces allowed

### User Types

*   `anonymous`: Standard users with read-only access to products
*   `admin`: Administrative users with full CRUD access to users and products

<!-- ## Database Migrations

This project uses `dbmate` to manage SQL database migrations.

*   **Location**: Migration files are located in the `db/migrations/` directory.
*   **Automatic Application**: Migrations are automatically applied when the services are started with `docker-compose up`, thanks to the `migration` service.

### Creating a New Migration

To create a new migration file, run the following command from the project root:

```sh
docker-compose run --rm migration dbmate new <migration_name>
```

Replace `<migration_name>` with a descriptive name for your migration (e.g., `add_description_to_products`). This will generate a new `.sql` file in the `db/migrations` directory, where you can add your `migrate:up` and `migrate:down` SQL statements. -->

## Error Responses

The API returns consistent error responses in the following format:

**Authentication Error (400):**
```json
{
  "detail": "Could not validate credentials"
}
```

**Validation Error (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Not Found Error (404):**
```json
{
  "detail": "Product not found"
}
```
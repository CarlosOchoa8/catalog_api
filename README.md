# Product Catalog API

This repository contains a RESTful API for managing a product catalog. Built with FastAPI, PostgreSQL, and SQLAlchemy, it provides a robust foundation for creating, reading, updating, and deleting users and products. The entire application is containerized using Docker and Docker Compose for a simplified setup and deployment process.

## Features

*   **Modern Python Backend**: Built with Python 3.13 and the high-performance FastAPI framework.
*   **Asynchronous Support**: Leverages `asyncpg` and SQLAlchemy's async capabilities for non-blocking database operations.
*   **Containerized Environment**: Fully containerized with Docker and orchestrated with Docker Compose for consistency across development and production environments.
*   **Database Migrations**: Uses `dbmate` for clear, simple, and plain SQL database migrations.
*   **Data Validation**: Employs Pydantic for robust data validation and serialization.
*   **Structured Project**: A clean and organized project structure that separates concerns like database logic, API endpoints, and business logic.
*   **Custom Exception Handling**: Provides clear, user-friendly error messages for request validation failures.
> [!IMPORTANT]
> TODO
> Users auth.
> Users notified when item is uptaed by admin.

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

    # Dbmate URL (for the migration container)
    DATABASE_URL_DBMATE=postgres://myuser:mypassword@db:5432/catalogdb?sslmode=disable
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

### Users

*   **POST** `/catalog_api/users/`

Registers a new user in the system.

**Request Body:**
```json
{
  "email": "test.user@example.com",
  "user_type": "anonymous"
}
```

**Success Response (200 OK):**
```json
{
  "email": "test.user@example.com",
  "user_type": "anonymous"
}
```

## Database Migrations

This project uses `dbmate` to manage SQL database migrations.

*   **Location**: Migration files are located in the `db/migrations/` directory.
*   **Automatic Application**: Migrations are automatically applied when the services are started with `docker-compose up`, thanks to the `migration` service.

### Creating a New Migration

To create a new migration file, run the following command from the project root:

```sh
docker-compose run --rm migration dbmate new <migration_name>
```

Replace `<migration_name>` with a descriptive name for your migration (e.g., `add_description_to_products`). This will generate a new `.sql` file in the `db/migrations` directory, where you can add your `migrate:up` and `migrate:down` SQL statements.


<!-- NOTES
Backend Technical Test
Hello! Thanks for your interest in applying to ZeBrands. As a part of the recruiting process, we ask you to complete this task as a way for you to showcase your abilities and knowledge.

Description of the task
We need to build a basic catalog system to manage products. A product should have basic info such as sku, name, price and brand.

In this system, we need to have at least two type of users: (i) admins to create / update / delete products and to create / update / delete other admins; and (ii) anonymous users who can only retrieve products information but can't make changes.

As a special requirement, whenever an admin user makes a change in a product (for example, if a price is adjusted), we need to notify all other admins about the change, either via email or other mechanism.

We also need to keep track of the number of times every single product is queried by an anonymous user, so we can build some reports in the future.

Your task is to build this system implementing a REST or GraphQL API using the stack of your preference.

What we expect
We are going to evaluate all your choices from API design to deployment, so invest enough time in every step, not only coding. The test may feel ambiguous at points because we want you to feel obligated to make design decisions. In real life you will often find this to be the case.

We are going to evaluate these dimensions:

Code quality: We expect clean code and good practices
Technology: Use of paradigms, frameworks and libraries. Remember to use the right tool for the right problem
Creativity: Don't let the previous instructions to limit your choices, be free
Organization: Project structure, versioning, coding standards
Documentation: Anyone should be able to run the app and to understand the code (this doesn't mean you need to put comments everywhere :))
If you want to stand out by going the extra mile, you could do some of the following:

Add tests for your code
Containerize the app
Deploy the API to a real environment
Use AWS SES or another 3rd party API to implement the notification system
Provide API documentation (ideally, auto generated from code)
Propose an architecture design and give an explanation about how it should scale in the future
Delivering your solution
Please provide us with a link to your personal repository and a link to the running app if you deployed it.
 -->
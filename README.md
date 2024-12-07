# Rate It

The **Rate It** is a Django Application where users can create and view posts and rate them.


## Table of Contents
- [Project Overview](#project-overview)
- [Installation](#installation)
- [Usage](#usage)


## Project Overview

This Django application, built using Django Rest Framework (DRF), allows users to view a list of posts and submit ratings. Each post contains a title and text, and users can rate the posts on a scale of 0 to 5. The rating system ensures that each user's rating can be updated if they rate a post again.

### Features

- **Post List View:** Displays the title of each post, the number of users who have rated it, and the average rating. If a user has rated a post, their rating is shown as well.
- **Submit Rating:** Users can submit a rating for a post, and their rating is updated if they rate the post again. There is no functionality to delete a rating.
- **Performance at Scale:** The application is designed to handle a large number of ratings per post (potentially millions), ensuring it performs well under high traffic, capable of handling thousands of requests per second.
- **Rating Stability:** To prevent short-term events like organized campaigns or emotional ratings from affecting the post's average score, a mechanism has been implemented to stabilize the rating system against unrealistic spikes.

This project focuses on providing an efficient and scalable solution for displaying and rating posts, ensuring reliability even under heavy load and high traffic.


## Installation

### Prerequisites
Make sure you have the following installed on your local machine:
- Docker
- Docker Compose
- Python

1. Clone the repository:
   ```bash
   git clone https://github.com/AliE99/rate-it.git
   cd rate-it
   ```

2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
   
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
   
4. Configuration:
   Set up environment variables in a `.env` file in the root directory of your project. For example:

    ```
    DATABASE_HOST=localhost
    DATABASE_NAME=db_name
    DATABASE_PASSWORD=db_pass
    DATABASE_PORT=5432
    DATABASE_USER=db_user
    REDIS_ADDR=localhost
    ```


## Usage
**Build and start the postgres and redis services:**
   ```bash
   docker-compose up --build
   ```

**Shutting down the services:**

```bash
docker compose  down
```

**To set up PostgreSQL, create the necessary database, and apply migrations, run the following script:**
```bash
sh setup_postgres.sh
```
This script will configure your PostgreSQL instance and prepare the database for the application by running the required migrations. Make sure PostgreSQL service is running on your system before executing the script.

**To start the Celery worker, use the following command**:
```bash
sh run_celery_worker.sh
```
This will launch the Celery worker with the application name `rateIt`. Ensure that Celery and a message broker(Redis) are properly configured before running this command.

**To start the Django development server, use the following command**:
```bash
python3 manage.py runserver
```
This will launch the server, and you can access the application in your browser at http://127.0.0.1:8000/. Make sure that all previous setup steps (database, migrations, Celery) have been completed before running the server.


**API Authentication**
This project uses JWT for authentication. To access endpoints, obtain a token through the login endpoints then include it as a Bearer token in request headers.

```
Authorization: Bearer <token>
```

## API Endpoints

You can open http://localhost:8000/api/docs/ for documentation and working with APIs.
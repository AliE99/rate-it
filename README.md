# Rate It

The **Rate It** is a Django Application where users can create and view posts and rate them.

## Table of Contents

- [Project Overview](#project-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Performance and Rating Stability](#performance-and-rating-stability)

## Project Overview

This Django application, built using Django Rest Framework (DRF), allows users to view a list of posts and submit
ratings. Each post contains a title and text, and users can rate the posts on a scale of 0 to 5. The rating system
ensures that each user's rating can be updated if they rate a post again.

### Features

- **Post List View:** Displays the title of each post, the number of users who have rated it, and the average rating. If
  a user has rated a post, their rating is shown as well.
- **Submit Rating:** Users can submit a rating for a post, and their rating is updated if they rate the post again.
  There is no functionality to delete a rating.
- **Performance at Scale:** The application is designed to handle a large number of ratings per post (potentially
  millions), ensuring it performs well under high traffic, capable of handling thousands of requests per second.
- **Rating Stability:** To prevent short-term events like organized campaigns or emotional ratings from affecting the
  post's average score, a mechanism has been implemented to stabilize the rating system against unrealistic spikes.

This project focuses on providing an efficient and scalable solution for displaying and rating posts, ensuring
reliability even under heavy load and high traffic.

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

This script will configure your PostgreSQL instance and prepare the database for the application by running the required
migrations. Make sure PostgreSQL service is running on your system before executing the script.

**Create Superuser:**
To create a superuser for authentication and to manage APIs, run the following command:

```bash
python3 manage.py createsuperuser
```

This command will prompt you to enter a username, email, and password for the superuser. Once created, you can log in to
the Django admin interface or use the superuser account for interacting with the APIs.
Note:
In the next version of the project, an API will be implemented to register users, enabling self-service user creation
via the application.

**To start the Celery worker, use the following command**:

```bash
sh run_celery_worker.sh
```

This will launch the Celery worker with the application name `rateIt`. Ensure that Celery and a message broker(Redis)
are properly configured before running this command.

**To start the Django development server, use the following command**:

```bash
python3 manage.py runserver
```

This will launch the server, and you can access the application in your browser at http://127.0.0.1:8000/. Make sure
that all previous setup steps (database, migrations, Celery) have been completed before running the server.

**API Authentication**
This project uses JWT for authentication. To access endpoints, obtain a token through the login endpoints then include
it as a Bearer token in request headers.

```
Authorization: Bearer <token>
```

**API Endpoints**

You can open http://localhost:8000/api/docs/ for documentation and working with APIs.

## Performance and Rating Stability

To ensure the system can handle millions of ratings efficiently under heavy load and to stabilize ratings against
short-term fluctuations, the following strategies have been implemented:

#### 1. **Delayed Updates**

Instead of immediately updating the average rating of a post upon each new rating, the updates are queued and processed
asynchronously using background workers(Celery). This approach ensures that the system is not blocked by expensive
rating calculations and can scale more effectively under high traffic.

**Status:** Done

#### 2. **Saved Average Rating and Count in the Model**

To avoid recalculating the average rating every time a rating is added, the average rating and the number of ratings are
saved directly in the Post model. This improves performance by reducing the need for repetitive calculations.

**Status:** Done

#### 3. **Indexing for Faster Queries**

To optimize query performance, particularly for filtering ratings based on the post and user fields, the `Rating` model
fields will be indexed. This ensures faster lookups and smoother operations when querying for user ratings on specific
posts.

**Status:** To Do

#### 4. **Exponential Moving Average for Rating Stability**

To prevent short-term events (such as organized campaigns or emotional ratings) from dramatically affecting the post's
average rating, an exponential moving average (EMA) mechanism has been added. This allows the system to smooth out
sudden spikes and maintain a more stable average rating over time.

**Status:** Done

These strategies together ensure that the system can handle large-scale usage efficiently while maintaining accurate and
stable ratings, even under heavy load or in the face of short-term rating spikes.
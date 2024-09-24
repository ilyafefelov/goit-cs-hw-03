# Task Manager Project

## Overview

The **Task Manager Project** is a simple web application designed to help users manage their tasks efficiently. It utilizes PostgreSQL for data storage, Docker for containerization, and Python's `unittest` framework for automated testing. This project demonstrates the integration of these technologies to create a robust and scalable application.

## Technologies Used

- **Docker & Docker Compose:** Containerize the application and PostgreSQL database for easy deployment.
- **PostgreSQL:** Relational database to store users, tasks, and status information.
- **Python 3.9:** Backend scripting and automated testing.
- **Psycopg2:** PostgreSQL adapter for Python to interact with the database.
- **Unittest:** Python's built-in testing framework for writing and running tests.

## Project Structure
```
├── Dockerfile 
├── docker-compose.yml 
├── create_tables.sql 
├── seed.py 
├── test_database.py 
├── README.md 
└── ... (other project files)
```

- **Dockerfile:** Defines the Docker image for the application, including dependencies and setup commands.
- **docker-compose.yml:** Configures the Docker services for the application and PostgreSQL database.
- **create_tables.sql:** SQL script to create the necessary database tables.
- **seed.py:** Python script to populate the database with initial data.
- **test_database.py:** Python script containing automated tests for database operations.
- **README.md:** Project documentation.

## Prerequisites

Ensure you have the following installed on your system:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.9](https://www.python.org/downloads/)
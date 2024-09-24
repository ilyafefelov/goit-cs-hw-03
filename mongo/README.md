Запуск Проекту
To run the project, use Docker Compose. The process involves two main steps:

Running MongoDB in the Background

This command starts the MongoDB service in the background, allowing you to continue using the terminal for other commands.

```bash
docker-compose up -d mongodb
```

Explanation:

- `up`: Creates and starts the containers.
- `-d`: Runs the services in detached mode.
- `mongodb`: The name of the service you want to start (defined in docker-compose.yml).

Running the Application in Interactive Mode

This command starts the application service in interactive mode, allowing you to interact with it through the terminal.

```bash
docker-compose run app
```

Explanation:

- `run`: Starts a new container for the specified service.
- `app`: The name of the application service defined in docker-compose.yml.

Example Output:

```markdown
---😺 Task Manager ---
1. Add a cat
2. Show all cats
3. Show a cat by name
4. Update a cat's age
5. Add a cat's characteristic
6. Delete a cat by name
7. Delete all cats
8. Exit 🐈‍⬛
Choose an option:
```

Interacting with the Application:

Enter the option number and press Enter.
The application will prompt for additional data based on the selected action.

import psycopg2
from faker import Faker

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host="postgres", # This is the name of the service in the docker-compose file
    database="task_manager_db",
    user="test_user",
    password="password"
)
cursor = conn.cursor()

faker = Faker()

# Insert statuses into the status table
statuses = ['new', 'in progress', 'completed']
for status in statuses:
    cursor.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", (status,))

# Insert users into the users table
for _ in range(10):
    fullname = faker.name()
    email = faker.unique.email()
    cursor.execute("INSERT INTO users (fullname, email) VALUES (%s, %s);", (fullname, email))

# Get user ids and status ids
cursor.execute("SELECT id FROM users;")
user_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id FROM status;")
status_ids = [row[0] for row in cursor.fetchall()]

# Insert tasks into the tasks table
for _ in range(30):
    title = faker.sentence(nb_words=6)
    description = faker.text(max_nb_chars=200)
    status_id = faker.random.choice(status_ids)
    user_id = faker.random.choice(user_ids)
    cursor.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);", (title, description, status_id, user_id))

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()

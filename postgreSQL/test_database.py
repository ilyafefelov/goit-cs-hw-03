import unittest
import psycopg2

class TestDatabaseQueries(unittest.TestCase):
    def setUp(self):
        # Create a new connection for each test
        self.connection = psycopg2.connect(
            dbname='task_manager_db',
            user='test_user',
            password='password',
            host='postgres',  # Use 'postgres' if running inside Docker
            port=5432
        )
        # Start a transaction
        self.connection.autocommit = False
        self.transaction = self.connection.cursor()

    def tearDown(self):
        # Roll back any changes made during the test
        self.connection.rollback()
        self.transaction.close()
        self.connection.close()

    def test_1_get_tasks_by_user(self):
        """1. Отримати всі завдання певного користувача (user_id = 1)"""
        self.transaction.execute("""
            SELECT * FROM tasks
            WHERE user_id = 1;
        """)
        results = self.transaction.fetchall()
        self.assertIsNotNone(results)
        print(f"Знайдено {len(results)} завдань для user_id = 1")

    def test_2_get_tasks_by_status(self):
        """2. Вибрати завдання за певним статусом ('new')"""
        self.transaction.execute("""
            SELECT * FROM tasks
            WHERE status_id = (SELECT id FROM status WHERE name = 'new');
        """)
        results = self.transaction.fetchall()
        self.assertIsNotNone(results)
        print(f"Знайдено {len(results)} завдань зі статусом 'new'")

    def test_3_update_task_status(self):
        """3. Оновити статус конкретного завдання (id = 5) на 'in progress'"""
        self.transaction.execute("""
            UPDATE tasks
            SET status_id = (SELECT id FROM status WHERE name = 'in progress')
            WHERE id = 5;
        """)
        self.connection.commit()
        # Перевіримо, чи статус оновлено
        self.transaction.execute("""
            SELECT s.name FROM tasks t
            JOIN status s ON t.status_id = s.id
            WHERE t.id = 5;
        """)
        result = self.transaction.fetchone()
        self.assertEqual(result[0], 'in progress')
        print("Статус завдання з id = 5 успішно оновлено на 'in progress'")

    def test_4_get_users_without_tasks(self):
        """4. Отримати список користувачів, які не мають жодного завдання"""
        self.transaction.execute("""
            SELECT * FROM users
            WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);
        """)
        results = self.transaction.fetchall()
        print(f"Кількість користувачів без завдань: {len(results)}")

    def test_5_add_new_task_for_user(self):
        """5. Додати нове завдання для користувача (user_id = 2)"""
        self.transaction.execute("""
            INSERT INTO tasks (title, description, status_id, user_id)
            VALUES ('Нове завдання', 'Опис нового завдання', (SELECT id FROM status WHERE name = 'new'), 2)
            RETURNING id;
        """)
        new_task_id = self.transaction.fetchone()[0]
        self.connection.commit()
        # Перевіримо, чи завдання додано
        self.transaction.execute("SELECT * FROM tasks WHERE id = %s;", (new_task_id,))
        task = self.transaction.fetchone()
        self.assertIsNotNone(task)
        print(f"Нове завдання додано з id = {new_task_id}")

    def test_6_get_incomplete_tasks(self):
        """6. Отримати всі завдання, які ще не завершено"""
        self.transaction.execute("""
            SELECT * FROM tasks
            WHERE status_id != (SELECT id FROM status WHERE name = 'completed');
        """)
        results = self.transaction.fetchall()
        self.assertIsNotNone(results)
        print(f"Кількість незавершених завдань: {len(results)}")

    def test_7_delete_task(self):
        """7. Видалити конкретне завдання (id = 10)"""
        self.transaction.execute("DELETE FROM tasks WHERE id = 10;")
        self.connection.commit()
        # Перевіримо, чи завдання видалено
        self.transaction.execute("SELECT * FROM tasks WHERE id = 10;")
        task = self.transaction.fetchone()
        self.assertIsNone(task)
        print("Завдання з id = 10 успішно видалено")

    def test_8_find_users_by_email_domain(self):
        """8. Знайти користувачів з електронною поштою, яка містить 'gmail.com'"""
        self.transaction.execute("""
            SELECT * FROM users
            WHERE email LIKE '%gmail.com';
        """)
        results = self.transaction.fetchall()
        print(f"Кількість користувачів з 'gmail.com': {len(results)}")

    def test_9_update_user_fullname(self):
        """9. Оновити ім'я користувача (id = 3)"""
        new_fullname = "Нове Ім'я"
        self.transaction.execute("""
            UPDATE users
            SET fullname = %s
            WHERE id = 3;
        """, (new_fullname,))
        self.connection.commit()
        self.transaction.execute("SELECT fullname FROM users WHERE id = 3;")
        fullname = self.transaction.fetchone()[0]
        self.assertEqual(fullname, new_fullname)
        print("Ім'я користувача з id = 3 успішно оновлено")

    def test_10_count_tasks_by_status(self):
        """10. Отримати кількість завдань для кожного статусу"""
        self.transaction.execute("""
            SELECT s.name AS status_name, COUNT(t.id) AS task_count
            FROM status s
            LEFT JOIN tasks t ON s.id = t.status_id
            GROUP BY s.name;
        """)
        results = self.transaction.fetchall()
        for status_name, task_count in results:
            print(f"Статус: {status_name}, Кількість завдань: {task_count}")
        self.assertIsNotNone(results)

    def test_11_get_tasks_by_user_email_domain(self):
        """11. Отримати завдання, призначені користувачам з '@example.com'"""
        self.transaction.execute("""
            SELECT t.*
            FROM tasks t
            JOIN users u ON t.user_id = u.id
            WHERE u.email LIKE '%@example.com';
        """)
        results = self.transaction.fetchall()
        print(f"Кількість завдань для '@example.com': {len(results)}")
        self.assertIsNotNone(results)

    def test_12_get_tasks_without_description(self):
        """12. Отримати список завдань, що не мають опису"""
        self.transaction.execute("""
            SELECT * FROM tasks
            WHERE description IS NULL OR description = '';
        """)
        results = self.transaction.fetchall()
        print(f"Кількість завдань без опису: {len(results)}")
        self.assertIsNotNone(results)

    def test_13_get_users_with_in_progress_tasks(self):
        """13. Користувачі та їхні завдання зі статусом 'in progress'"""
        self.transaction.execute("""
            SELECT u.fullname, t.title, s.name AS status_name
            FROM users u
            JOIN tasks t ON u.id = t.user_id
            JOIN status s ON t.status_id = s.id
            WHERE s.name = 'in progress';
        """)
        results = self.transaction.fetchall()
        print(f"Кількість завдань 'in progress': {len(results)}")
        self.assertIsNotNone(results)

    def test_14_get_users_and_task_counts(self):
        """14. Отримати користувачів та кількість їхніх завдань"""
        self.transaction.execute("""
            SELECT u.fullname, COUNT(t.id) AS task_count
            FROM users u
            LEFT JOIN tasks t ON u.id = t.user_id
            GROUP BY u.fullname;
        """)
        results = self.transaction.fetchall()
        for fullname, task_count in results:
            print(f"Користувач: {fullname}, Кількість завдань: {task_count}")
        self.assertIsNotNone(results)

if __name__ == '__main__':
    unittest.main()

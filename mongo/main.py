import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import sys

def get_database():
    """
    Підключення до MongoDB та повернення об'єкта бази даних.
    """
    try:
        # Підключаємось до MongoDB, використовуючи сервісне ім'я 'mongodb' з docker-compose.yml
        client = MongoClient('mongodb://mongo:27017/')
        db = client['task_manager_db']
        return db
    except pymongo.errors.ConnectionError as ce:
        print(f"Помилка підключення: {ce}")
        sys.exit(1)

def create_cat(db, name, age, features):
    """
    Додавання нового кота до колекції.
    """
    try:
        cat = {
            "name": name,
            "age": age,
            "features": features
        }
        result = db.cats.insert_one(cat)
        print(f"Кіт додано з _id: {result.inserted_id}")
    except Exception as e:
        print(f"Помилка при додаванні кота: {e}")

def read_all_cats(db):
    """
    Виведення всіх котів з колекції.
    """
    try:
        cats = db.cats.find()
        for cat in cats:
            print(cat)
    except Exception as e:
        print(f"Помилка при читанні котів: {e}")

def read_cat_by_name(db, name):
    """
    Виведення інформації про кота за іменем.
    """
    try:
        cat = db.cats.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"Кіт з ім'ям '{name}' не знайдений.")
    except Exception as e:
        print(f"Помилка при читанні кота: {e}")

def update_cat_age(db, name, new_age):
    """
    Оновлення віку кота за іменем.
    """
    try:
        result = db.cats.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count:
            print(f"Вік кота '{name}' оновлено до {new_age}.")
        else:
            print(f"Кіт з ім'ям '{name}' не знайдений.")
    except Exception as e:
        print(f"Помилка при оновленні віку кота: {e}")

def add_cat_feature(db, name, new_feature):
    """
    Додавання нової характеристики до списку features кота за іменем.
    """
    try:
        result = db.cats.update_one({"name": name}, {"$push": {"features": new_feature}})
        if result.matched_count:
            print(f"Характеристика '{new_feature}' додана до кота '{name}'.")
        else:
            print(f"Кіт з ім'ям '{name}' не знайдений.")
    except Exception as e:
        print(f"Помилка при додаванні характеристики: {e}")

def delete_cat_by_name(db, name):
    """
    Видалення кота за іменем.
    """
    try:
        result = db.cats.delete_one({"name": name})
        if result.deleted_count:
            print(f"Кіт з ім'ям '{name}' успішно видалений.")
        else:
            print(f"Кіт з ім'ям '{name}' не знайдений.")
    except Exception as e:
        print(f"Помилка при видаленні кота: {e}")

def delete_all_cats(db):
    """
    Видалення всіх котів з колекції.
    """
    try:
        result = db.cats.delete_many({})
        print(f"Видалено {result.deleted_count} котів з колекції.")
    except Exception as e:
        print(f"Помилка при видаленні всіх котів: {e}")

def main():
    db = get_database()

    while True:
        print("\n---😺 Task Manager ---")
        print("1. Додати кота")
        print("2. Показати всіх котів")
        print("3. Показати кота за ім'ям")
        print("4. Оновити вік кота")
        print("5. Додати характеристику коту")
        print("6. Видалити кота за ім'ям")
        print("7. Видалити всіх котів")
        print("8. Вийти 🐈‍⬛")
        
        choice = input("Виберіть опцію: ")

        if choice == '1':
            name = input("Введіть ім'я кота: ")
            age = int(input("Введіть вік кота: "))
            features = input("Введіть характеристики кота через кому: ").split(',')
            features = [feature.strip() for feature in features]
            create_cat(db, name, age, features)
        
        elif choice == '2':
            read_all_cats(db)
        
        elif choice == '3':
            name = input("Введіть ім'я кота: ")
            read_cat_by_name(db, name)
        
        elif choice == '4':
            name = input("Введіть ім'я кота: ")
            new_age = int(input("Введіть новий вік кота: "))
            update_cat_age(db, name, new_age)
        
        elif choice == '5':
            name = input("Введіть ім'я кота: ")
            new_feature = input("Введіть нову характеристику: ")
            add_cat_feature(db, name, new_feature)
        
        elif choice == '6':
            name = input("Введіть ім'я кота для видалення: ")
            delete_cat_by_name(db, name)
        
        elif choice == '7':
            confirm = input("Ви впевнені, що хочете видалити всіх котів? (так/ні): ")
            if confirm.lower() == 'так':
                delete_all_cats(db)
        
        elif choice == '8':
            print("Вихід...")
            break
        
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()

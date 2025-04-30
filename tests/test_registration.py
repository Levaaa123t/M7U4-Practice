import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."


def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."


def test_successful_authentication(setup_database, connection):
    username = 'user1'
    email = 'user1@gmail.com'
    password = 'pass1'
    add_user(username, email, password)
    assert authenticate_user(username, password), 'Авторизация успешна.'

def test_non_existent_user(setup_database, connection):
    username = 'user123'
    email = 'user123@gmail.com'
    password = 'pass123'
    assert not authenticate_user(username, password)

def test_display_list_user(setup_database, connection):
    username = 'username12'
    email = 'username@gmail.com'
    password = 'password123'
    users = [
        ('testuser', 'testuser@example.com', 'password123'),
        ('user1', 'user1@gmail.com', 'pass1'),
        ('user123', 'user123@gmail.com', 'pass123'),
        ('username12','username@gmail.com', 'password123')
        ]
    for username, email, password in users:
        add_user(username, email, password)
    cursor = connection.cursor()
    cursor.execute('SELECT username, email FROM users')
    db_users = cursor.fetchall()
    expected_users = {(user[0], user[1]) for user in users}
    actual_users = set(db_users)
    assert actual_users == expected_users, f"Ожидалось {expected_users}, получено {actual_users}"
    #for user in cursor.fetchall():
    #    print(f"Логин: {user[0]}, Электронная почта: {user[1]}")
    #assert display_users(), f"Логин: {user[0]}, Электронная почта: {user[1]}"
    
def test_authentication_error_password():
    username = 'usertest10'
    email = 'usertest10@gmail.com'
    password = 'password100'
    password_error = 'password200'
    add_user(username,email,password)
    assert not authenticate_user(username, password_error), 'Неверный логин или пароль.'

def test_addition_login_exist():
    username = 'new_user1'
    email = 'new_user1@gmail.com'    
    password = 'newuserpass'
    username_exist = 'new_user1'
    add_user(username,email,password)
    assert add_user(username_exist, email,password) == False
"""
Тест отображения списка пользователей.
"""
# Прежде, чем приступать к написанию Flask-приложения, полезно разработать функции, для работы с данными и сложить их в отдельном файле, например, `utils.py.` Например:

import json


# Загружаем посты из json


def get_posts_all() -> list[dict]:
    with open('./data/posts.json', 'r', encoding='utf-8') as posts_file:
        return json.load(posts_file)

# Загружаем комменты из json


def get_comments_all() -> list[dict]:
    with open('./data/comments.json', 'r', encoding='utf-8') as comments_file:
        return json.load(comments_file)

# Подгружаем закладки


def get_bookmarks_all() -> list[dict]:
    with open('./data/bookmarks.json', 'r', encoding='utf-8') as bookmarks_file:
        return json.load(bookmarks_file)

def get_bookmarks_by_user(bookmark_number: str) -> list[dict]:
    bookmarks_result = []
    for bookmark in get_bookmarks_all():
        if bookmark_number.lower() == bookmark['bookmark_number'].lower():
            bookmarks_result.append(bookmark)
            # assert ValueError  - проверка если такого пользователя нет и пустой список, если у пользователя нет закладок.
    return bookmarks_result


def delete_bookmarks():
    with open('./data/bookmarks.json', 'w', encoding='utf-8') as outfile:
        data = json.load(bookmarks_file_del)

    for i in data:
        data["bookmark_number"].remove(bookmark_number)


# `get_posts_by_user(user_name)` – возвращает посты определенного пользователя. Функция должна вызывать

def get_posts_by_user(user_name: str) -> list[dict]:
    posts_result = []
    for post in get_posts_all():
        if user_name.lower() == post['poster_name'].lower():
            posts_result.append(post)
            # assert ValueError  - проверка если такого пользователя нет и пустой список, если у пользователя нет постов.
    return posts_result


def get_comments_by_post_id(post_id: int) -> list[dict]:
    comments_result = []
    for comment in get_comments_all():
        if post_id == comment['post_id']:
            comments_result.append(comment)
            # Assert если такого поста нет и пустой список, если у поста нет комментов.
    return comments_result


# `search_for_posts(query)` – возвращает список постов по ключевому слову

def search_for_posts(query: str) -> list[dict]:
    search_result = []
    for posts in get_posts_all():
        if query.lower() in posts['content'].lower():
            search_result.append(posts)
    return search_result


# `get_post_by_pk(pk)` – возвращает один пост по его идентификатору.

def get_post_by_pk(pk: int) -> dict:
    for post in get_posts_all():
        if pk == post['pk']:
            return post
    return {}

def test_zero():
    assert get_post_by_pk(1) == 1, "Неверно для 1"

# Напишите к каждой функции юнит тесты, расположите тесты в отдельной папке `/tests`.

# Организуйте тесты в виде классов или функций, на ваше усмотрение.

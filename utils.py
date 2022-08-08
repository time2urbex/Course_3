
import json


# Функция, которая загружает посты из json и в случае распознования тега # делает ссылку на него



def get_posts_all() -> list[dict]:
    with open('./data/posts.json', 'r', encoding='utf-8') as posts_file:
        posts = json.load(posts_file)
        for post in posts:

            content = post["content"].split(" ")
            new_content = []
            for element in content:
                if element.startswith("#"):
                    new_content.append(f' <a href="/tag/{element[1:]}">#{element[1:]}</a> ')
                else:
                    new_content.append(element)
            new_content = " ".join(new_content)
            post["content"] = new_content

        return posts


# Загружаем комменты из json


def get_comments_all() -> list[dict]:
    with open('./data/comments.json', 'r', encoding='utf-8') as comments_file:
        return json.load(comments_file)

# Подгружаем закладки

def get_bookmarks_all() -> list[dict]:
    with open('./data/bookmarks.json', 'r', encoding='utf-8') as bookmarks_file:
        return json.load(bookmarks_file)

# Добавление / удаление закладок


def add_bookmark(bookmark_number: int):
    post = get_post_by_pk(bookmark_number)
    bookmarks = get_bookmarks_all()
    if post not in bookmarks:
        bookmarks.append(post)
        with open('./data/bookmarks.json', 'w', encoding='utf-8') as bookmarks_file:
            json.dump(bookmarks, bookmarks_file)

# Добавление / удаление комментария

def post_new_comment(content, user_name, postid):
    comments = get_comments_all()
    pk=len(comments)+1
    comment =   {
    "post_id": postid,
    "commenter_name": user_name,
    "comment": content ,
    "pk": pk,
  }
    comments.append(comment)
    with open('./data/comments.json', 'w', encoding='utf-8') as comments_file:
        json.dump(comments, comments_file)




"""    bookmarks_result = []
    for bookmark in get_bookmarks_all():
        if bookmark_number.lower() == bookmark['bookmark_number'].lower():
            bookmarks_result.append(bookmark)
            # assert ValueError  - проверка если такого пользователя нет и пустой список, если у пользователя нет закладок.
 return bookmarks_result   """

# Добавление / удаление закладки

def delete_bookmarks(bookmark_number):
    post = get_post_by_pk(bookmark_number)
    bookmarks = get_bookmarks_all()
    bookmarks.remove(post)
    with open('./data/bookmarks.json', 'w', encoding='utf-8') as bookmarks_file:
        json.dump(bookmarks, bookmarks_file)

# Возвращаем посты определенного пользователя

def get_posts_by_user(user_name: str) -> list[dict]:
    posts_result = []
    for post in get_posts_all():
        if user_name.lower() == post['poster_name'].lower():
            posts_result.append(post)
            # assert ValueError  - проверка если такого пользователя нет и пустой список, если у пользователя нет постов.
    return posts_result

# Возвращаем посты по ID


def get_comments_by_post_id(post_id: int) -> list[dict]:
    if type(post_id) != int:
        raise TypeError("Должно быть целое число")
    comments_result = []
    for comment in get_comments_all():
        if post_id == comment['post_id']:
            comments_result.append(comment)
            # Assert если такого поста нет и пустой список, если у поста нет комментов.
    return comments_result



# `Ввозвращаем список постов по ключевому слову

def search_for_posts(query: str) -> list[dict]:
    search_result = []
    for posts in get_posts_all():
        if query.lower() in posts['content'].lower():
            search_result.append(posts)
    return search_result



# Возвращаем один пост по его идентификатору.

def get_post_by_pk(pk: int) -> dict:
    for post in get_posts_all():
        if pk == post['pk']:

            return post
    return {}

# При просмотре поста, добавляем +1 к просмотрам


def add_views(post_id: int):
    with open('./data/posts.json', 'r', encoding='utf-8') as posts_file:
        posts = json.load(posts_file)
        for i in range(len(posts)):
            if posts[i]["pk"] == post_id:
                posts[i]["views_count"] += 1

    with open('./data/posts.json', 'w', encoding='utf-8') as posts_file:
        json.dump(posts, posts_file)




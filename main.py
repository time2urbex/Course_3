# Импортируем необходимые модули
import logging

import json
from flask import Blueprint, render_template, request, Flask, jsonify, redirect
from utils import *

app = Flask(__name__)

# Добавляем логировани в файл api.log



logging.basicConfig(filename="logs/api.log", filemode='a', format="%(asctime)s [%(levelname)s] %(message)s", level = logging.INFO)

#logging.ERROR


app.config["JSON_AS_ASCII"] = False

# Создаем роут главной страницы


@app.route('/')
def main_page():
    total_posts = get_posts_all()
    total_bookmarks = len(get_bookmarks_all())
    if total_posts:
        for post in total_posts:
            add_views(post["pk"])
    return render_template('index.html', posts=total_posts, bookmarks = total_bookmarks )


# Создаем роут просмотра поста GET /posts/<post_id>

@app.route('/posts/<int:post_id>')
def one_post(post_id):
    post = get_post_by_pk(post_id)
    comments = get_comments_by_post_id(post_id)
    if post:
        add_views(post_id)

        return render_template('post.html', post=post, comments=comments)
    else: return "Такого поста нет"
# Добавить комментарии

# Создаем роут поиска постов по слову


@app.route('/search/')
def search_page():
    search_query = request.args.get('s', ' ')
    logging.info('Выполняю поиск')

    # Делаем проверку на наличие и работоспособность файла

    try:
        posts = search_for_posts(search_query)

        for post in posts:
            add_views(post["pk"])

    except FileNotFoundError:
        return 'Файл не найден'

    except JSONDecoderError:
        return 'Невалидный файл'


    return render_template('/search.html', query=search_query, posts=posts)



# Обработчик ошибок 404

@app.errorhandler(404)
def page(error):
    return ("Страница не найдена", 404)

# Обработчик ошибок 500

@app.errorhandler(500)
def server(error):
    return ("Внутренняя ошибка сервера", 500)


# Представления, которые обрабатывает запрос GET /api/posts и возвращает полный список постов в виде JSON-списка.


@app.route('/api/posts')
def all_posts():
    total_posts = get_posts_all()
    logging.info("User gets all posts")
    return jsonify(total_posts)

@app.route('/api/posts/<int:post_id>')
def all_posts_by_id(post_id):
    post = get_post_by_pk(post_id)
    logging.info("User gets post by id")
    return jsonify(post)


# Представления, которые обрабатывает запрос GET /users/<username> и возвращает полный список постов в виде JSON-списка.


@app.route('/users/<username>')
def all_posts_by_user(username):
    total_posts = get_posts_by_user(username)
    if total_posts:
        for post in total_posts:
            add_views(post["pk"])
        return render_template('user-feed.html', username=username, posts=total_posts)
    else: return "У пользователя нет постов"

# Представления, которые обрабатывает запрос GET /bookmarks/ и возвращает полный список закладок в виде JSON-списка.


@app.route('/bookmarks/')
def all_bookmarks():
    total_bookmarks = get_bookmarks_all()
    logging.info("User gets all bookmarks")
    if total_bookmarks:
        return render_template('bookmarks.html', total_bookmarks=total_bookmarks)
    else: return "У вас нет постов в закладках"

# Представление для добавления закладки

@app.route('/bookmarks/add/<int:postid>')
def add_getbookmark(postid):
    add_bookmark(postid)
    return redirect("/", code=302)

# Представление для удаления закладки


@app.route('/bookmarks/remove/<int:postid>')
def remove_bookmark(postid):
    delete_bookmarks(postid)
    return redirect("/", code=302)

# Представление для добавления комментария


@app.route('/add_comment/<int:postid>', methods=["POST"])
def add_comment(postid):
    content = request.form["content"]
    name = request.form["user_name"]
    post_new_comment(content, name, postid)
    return redirect("/posts/"+str(postid), code=302)

# Представление для поиска по тегу


@app.route('/tag/<tag_name>')
def tag_find(tag_name):
    posts = search_for_posts("#" + tag_name)
    for post in posts:
        add_views(post["pk"])
    return render_template('tag.html', posts=posts, tag_name=tag_name  )



if __name__ == "__main__":
    app.run()
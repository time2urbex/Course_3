
import logging

import json
from flask import Blueprint, render_template, request, Flask, jsonify
from utils import get_posts_all, get_comments_all, get_posts_by_user, get_comments_by_post_id, search_for_posts, get_post_by_pk, test_zero, get_bookmarks_all, get_bookmarks_by_user

app = Flask(__name__)

logging.basicConfig(filename="logs/api.log", filemode='a', format="%(asctime)s [%(levelname)s] %(message)s", level = logging.INFO)

#logging.ERROR

# Создаем роут главной страницы

app.config["JSON_AS_ASCII"] = False


@app.route('/')
def main_page():
    total_posts = get_posts_all()
    return render_template('index.html', posts=total_posts)

#Как правильно написать  GET запрос ?


# Создаем роут просмотра поста GET /posts/<post_id>

@app.route('/posts/<int:post_id>')
def one_post(post_id):
    post = get_post_by_pk(post_id)
    comments = get_comments_by_post_id(post_id)
    return render_template('post.html', post=post, comments=comments)

# Добавить комментарии



@app.route('/search/')
def search_page():
    search_query = request.args.get('s', ' ')
    logging.info('Выполняю поиск')

    # Делаем проверку на наличие и работоспособность файла

    try:
        posts = search_for_posts(search_query)

    except FileNotFoundError:
        return 'Файл не найден'

    except JSONDecoderError:
        return 'Невалидный файл'
    return render_template('/search.html', query=search_query, posts=posts)



#добавить обработчик ошибок 404
@app.errorhandler(404)
def page(error):
    return ("Страница не найдена", 404)

#добавить обработчик ошибок 500

@app.errorhandler(500)
def server(error):
    return ("Внутренняя ошибка сервера", 500)


# Шаг 6 – сделайте 2 API - эндпоинта
# представление, которое обрабатывает запрос GET /api/posts и возвращает полный список постов в виде JSON-списка.


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


@app.route('/users/<username>')
def all_posts_by_user(username):
    total_posts = get_posts_by_user(username)
    return render_template('user-feed.html', username=username, posts=total_posts)

@app.route('/api/bookmarks/<bookmark_number>')
def all_bookmarks_by_user(bookmark_number):
    total_bookmarks = get_bookmarks_by_user(bookmark_number)
    logging.info("User gets all bookmarks")
    return render_template('bookmarks.html', total_bookmarks=total_bookmarks, bookmark_number=bookmark_number)


if __name__ == "__main__":

    app.run(port=5000, debug=True)
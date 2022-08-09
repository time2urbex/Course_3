# Тест классами, фикстуры, ui тесты

from main import app
from utils import *
import pytest


@pytest.fixture()
def response_keys():
    keys = {"poster_name",
            "poster_avatar",
            "pic",
            "content",
            "views_count",
            "likes_count",
            "pk"}
    return keys


@pytest.fixture()
def client():
    return app.test_client()


# Тестируем возврат постов
class TestApi:

    def test_get_post_all(self, client, response_keys):
        response = client.get("/api/posts")
        assert response.status_code == 200, "Api не работает, ошибка 200"
        assert type(response.json) == list, "Api возвращает не список"
        for el in response.json:
            assert type(el) == dict
            assert el.keys() == response_keys

    # Тестируем возврат одного поста по id

    def test_get_post_one(self, client, response_keys):
        response = app.test_client().get("/api/posts/1")
        assert response.status_code == 200, "Api не работает, ошибка 200"
        assert type(response.json) == dict, "Api возвращает не словарь"
        assert response.json.keys() == response_keys


#
#
# # Тестируем возврат комментов по id поста
#

def test_get_comments_by_post_id():
    assert type(get_comments_by_post_id(1)) == list, "Функция возвращает не список"

    comments = get_comments_by_post_id(1)
    for comment in comments:
        assert comment["post_id"] == 1


comments_exceptions = [
    ("one", TypeError),
    (["1"], TypeError),
    ({1: 2}, TypeError)
]


# Тестируем некорректный ввод данных


@pytest.mark.parametrize("post_int, exception", comments_exceptions)
def test_get_comments_by_post_id_exceptions(post_int, exception):
    with pytest.raises(exception):
        get_comments_by_post_id(post_int)


# Тестируем возврат поста по его pk (для пример взят пост под номером 1)


def test_get_post_by_pk(response_keys):
    assert get_post_by_pk(1).keys() == response_keys
    assert get_post_by_pk(-1) == dict(), "Ошибка для номера pk"
    # assert get_post_by_pk.status_code == 200, "Api не работает, ошибка 200"


# Тестируем возврат поста в виде списка

def test_get_posts_all():
    assert type(get_posts_all()) == list, "Ошибка для типа список"

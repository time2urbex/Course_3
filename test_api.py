from main import app
from utils import *
import pytest


# Тестируем возврат постов


def test_get_post_all():
    response = app.test_client().get("/api/posts")
    assert response.status_code == 200, "Api не работает, ошибка 200"
    assert type(response.json) == list, "Api возвращает не список"
    post = response.json[0]

# Тестируем возврат одного поста по id


def test_get_post_one():
    response = app.test_client().get("/api/posts/1")
    assert response.status_code == 200, "Api не работает, ошибка 200"
    assert type(response.json) == dict, "Api возвращает не словарь"
    post = response.json
    assert post.get("pk"), "Нету идентификатора"

# Тестируем возврат комментов по id поста


def test_get_comments_by_post_id():
    assert type(get_comments_by_post_id(1)) == list, "Функция возвращает не список"


    comments = get_comments_by_post_id(1)
    assert comments.status_code == 200, "Api не работает, ошибка 200"
    assert type(comments.json) == dict, "Api возвращает не словарь"
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


def test_get_post_by_pk():
    assert get_post_by_pk(1) == {
        "poster_name": "leo",
        "poster_avatar": "https://randus.org/avatars/w/c1819dbdffffff18.png",
        "pic": "https://images.unsplash.com/photo-1525351326368-efbb5cb6814d?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=580&q=80",
        "content": "Ага, опять еда! Квадратная тарелка в квадратном кадре. А на тарелке, наверное, пирог! Мне было так жаль, что я не могу ее съесть. Я боялась, что они заметят, и если я не съем это, то, значит, они все подумают, что я плохая девочка... Но потом мне вспомнилось, как они на меня смотрели. Когда я была маленькой, на кухне всегда были родители, бабушка, дедушка, дядя Борис... Все вместе. И всегда одна я, потому что все остальные приходили туда лишь изредка. Мне казалось, если бы все ходили на работу, как и я, в этот свой офис, было бы совсем неинтересно.",
        "views_count": 376,
        "likes_count": 154,
        "pk": 1
    }
    assert get_post_by_pk(1) == dict(), "Ошибка для номера pk"
    #assert get_post_by_pk.status_code == 200, "Api не работает, ошибка 200"


# Тестируем возврат поста в виде списка

def test_get_posts_all():
    assert type(get_posts_all()) == list, "Ошибка для типа список"



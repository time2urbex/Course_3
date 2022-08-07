from utils import get_posts_all, get_comments_all, get_posts_by_user, get_comments_by_post_id, search_for_posts, get_post_by_pk, test_zero
import json
import pytest
#это тест



def test_get_post_by_user_name_type_error(self):
    post = Posts(DATA_PATH)
    with pytest.raises(TypeError):
        post.get_posts_by_user(1)

def test_get_post_by_user_name_type_error(self):
    post = Posts(DATA_PATH)
    with pytest.raises(ValueError):
        post.get_posts_by_user('1')



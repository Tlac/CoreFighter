import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_client(api_client, django_user_model):
    def _login(user=None, **user_kwargs):
        if user is None:
            username = user_kwargs.pop("username", "admin")
            password = user_kwargs.pop("password", "password1234")
            user = django_user_model.objects.create_user(
                username=username, password=password, **user_kwargs
            )
        api_client.force_authenticate(user=user)
        return api_client, user
    return _login


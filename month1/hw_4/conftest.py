import pytest

import requests


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        default="https://ya.ru",
        help="This is request url"
    )

    parser.addoption(
        "--status_code",
        default=200,
        choices=[200, 300, 400, 404, 500],
        type=int,
        help="Status code to check"
    )


@pytest.fixture
def url(request):
    return request.config.getoption("--url")


@pytest.fixture
def status_code(request):
    return request.config.getoption("--status_code")


def test_url_status_code(url, status_code):
    try:
        response = requests.get(url)
        assert response.status_code == status_code
    except requests.exceptions.ConnectionError:
        assert 404 == status_code

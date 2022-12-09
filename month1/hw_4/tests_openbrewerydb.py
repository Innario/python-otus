import pytest
import requests


@pytest.mark.parametrize('city', ['new_york', 'akron', 'kansas_city'])
def test_check_city_by_city_filter(city):
    response = requests.get(f'https://api.openbrewerydb.org/breweries?by_city={city}')
    data = response.json()
    assert 200 == response.status_code
    assert len(data) <= 20
    for brewery in data:
        assert city.title().replace("_", " ") in brewery['city']


@pytest.mark.parametrize('n_breweries', ["a", -1, '', 0, 4.9, 19, 20, 50, 51, 100])
def test_number_of_breweries_per_page(n_breweries):
    response = requests.get(f'https://api.openbrewerydb.org/breweries?per_page={n_breweries}')
    assert 200 == response.status_code
    data = response.json()
    if isinstance(n_breweries, float):
        n_breweries = int(n_breweries)
    if not isinstance(n_breweries, int):
        assert len(data) == 20
    elif n_breweries < 0:
        assert len(data) == 20
    elif n_breweries > 50:
        assert len(data) == 50
    else:
        assert len(data) == n_breweries


@pytest.mark.parametrize('random_size', ["a", -1, '', 0, 4.9, 19, 20, 50, 51, 100])
def test_random_breweries(random_size):
    response = requests.get('https://api.openbrewerydb.org/breweries/random')
    assert 200 == response.status_code
    data = response.json()
    assert len(data) == 1

    response = requests.get('https://api.openbrewerydb.org/breweries/random?size={random_size}')
    assert 200 == response.status_code
    data = response.json()
    if isinstance(random_size, float):
        brewery_size = int(random_size)
    if not isinstance(random_size, int):
        assert len(data) == 1
    elif random_size <= 0:
        assert len(data) == 1
    elif random_size > 17:
        assert len(data) == 1
    else:
        assert len(data) == random_size


@pytest.mark.parametrize('random_size, keys', [(1, ["name", "city"]), (5, ["brewery_type"]), (10, ["phone"])])
def test_autocomplete(random_size, keys):
    response = requests.get(f'https://api.openbrewerydb.org/breweries/random?size={random_size}')
    assert 200 == response.status_code
    data = response.json()
    assert len(data) == random_size

    for brewery in data:
        for key in keys:
            if brewery[key]:
                response_2 = requests.get(f'https://api.openbrewerydb.org/breweries/search?query={brewery[key]}')
                assert 200 == response_2.status_code
                data_autocomplete = response_2.json()
                assert len(data_autocomplete) == 0


@pytest.mark.parametrize('sort_type, key', [('asc', "phone"), ('desc', "id")])
def test_sort(sort_type, key):
    response = requests.get(f'https://api.openbrewerydb.org/breweries?sort=type,{key}:{sort_type}&per_page=15&page=6')
    assert 200 == response.status_code
    data = response.json()
    values = [brewery[key] for brewery in data if brewery[key]]
    if sort_type == 'asc':
        assert values == sorted(values)
    elif sort_type == 'desc':
        assert values == sorted(values, reverse=True)

import pytest
import requests


@pytest.mark.parametrize('url', ['https://dog.ceo/api/breeds/list/all',
                                 'https://dog.ceo/api/breeds/image/random',
                                 'https://dog.ceo/api/breeds/image/random/3',
                                 'https://dog.ceo/api/breed/hound/images',
                                 'https://dog.ceo/api/breed/hound/images/random',
                                 'https://dog.ceo/api/breed/hound/images/random/3',
                                 'https://dog.ceo/api/breed/hound/list',
                                 'https://dog.ceo/api/breed/hound/afghan/images',
                                 'https://dog.ceo/api/breed/hound/afghan/images/random',
                                 'https://dog.ceo/api/breed/hound/afghan/images/random/3'
                                 ])
def test_response_ok(url):
    response = requests.get(url)
    data = response.json()
    assert 200 == response.status_code
    assert data['status'] == 'success'


@pytest.mark.parametrize('n_images', [51, 0, -3, 1, 35, 50])
def test_random_images(n_images):
    response = requests.get(f'https://dog.ceo/api/breeds/image/random/{n_images}')
    assert 200 == response.status_code
    data = response.json()
    assert data['status'] == 'success'

    if n_images < 2:
        assert len(data['message']) == 1
    elif n_images > 50:
        assert len(data['message']) == 50
    else:
        assert len(data['message']) == n_images


@pytest.mark.parametrize('breed',
                         ['hound/afghan', 'pug', 'boxer', 'dalmatian', 'pekinese', 'husky', 'labrador', 'newfoundland'])
def test_random_breeds_image(breed):
    response = requests.get(f'https://dog.ceo/api/breed/{breed}/images/random')
    assert 200 == response.status_code
    data = response.json()
    assert data['status'] == 'success'
    assert type(data['message']) == str
    breed = breed.replace('/', '-')
    assert data['message'].startswith(f'https://images.dog.ceo/breeds/{breed}/')
    assert data['message'].endswith('.jpg')


@pytest.mark.parametrize('breed_with_sub_breed',
                         ['australian', 'buhund', 'bulldog', 'bullterrier', 'cattledog', 'collie', 'corgi',
                          'dane', 'deerhound', 'elkhound', 'finnish', 'frise', 'greyhound', 'hound', 'mastiff',
                          'mountain', 'ovcharka', 'pinscher', 'pointer', 'poodle', 'retriever', 'ridgeback',
                          'schnauzer'])
def test_sub_breeds_list(breed_with_sub_breed):
    response = requests.get(f'https://dog.ceo/api/breed/{breed_with_sub_breed}/list')
    assert 200 == response.status_code
    data = response.json()
    assert data['status'] == 'success'
    assert len(data['message']) > 0
    for sub_breed in data["message"]:
        response = requests.get(f'https://dog.ceo/api/breed/{breed_with_sub_breed}/{sub_breed}/images')
        assert 200 == response.status_code
        data = response.json()
        assert data['status'] == 'success'
        assert len(data['message']) > 0
        for image in data['message']:
            assert image.startswith(f'https://images.dog.ceo/breeds/{breed_with_sub_breed}-{sub_breed}')
            assert image.endswith('.jpg')


def test_all_list_sub_breeds():
    response = requests.get(f'https://dog.ceo/api/breeds/list/all')
    assert 200 == response.status_code
    data = response.json()
    assert data['status'] == 'success'
    for i, (breed, sub_breeds) in enumerate(data["message"].items()):
        print(f"{i} {breed} -> {sub_breeds}")
        response = requests.get(f'https://dog.ceo/api/breed/{breed}/list')
        assert 200 == response.status_code
        data = response.json()
        assert data['status'] == 'success'
        assert data["message"] == sub_breeds

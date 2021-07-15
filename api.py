import json
import os

import pytest

data = {"name": "Test",
        "universe": "Marvel Universe",
        "education": "High school (unfinished)",
        "weight": 104,
        "height": 1.90,
        "identity": "Publicly known"}


def test_get_characters(ivi_api):
    """
    Отправляем запрос на получение всех записей по персонажам.
    Проверяем код ответа, длину JSON, наличие ключа 'name' у первой записи.
    Используем проверку try/except так как возможна ошибка в написании url. Данная проверка ловит ошибку "json.decoder.JSONDecodeError". В случае срабатывания части кода, выдается ошибка с текстом и ссылкой на ту строку, к которой идет обращение


    :param ivi_api: фикстура из файла conftest.py, срабатывающая на каждый запуск теста. В параметрах записывается end point
    :type ivi_api: функция
    """
    try:
        print(os.getenv('LOG'))
        r = ivi_api.get('/characters')
        r_len = len(r.json()["result"])
        assert r.status_code == 200, f'Ошибка, код ответа = {r.status_code}, а не 200'
        assert r_len != None, f"Ошибка, длина записи 'result' должно быть больше 0. Текущая длина записи {r_len}"
        assert r.json()['result'][0]['name'] != None, "Ошибка, отсутствует поле Name в выдаче"
    except json.decoder.JSONDecodeError:
        raise ValueError(f"Ошибка в URL строке: {r.url}")


@pytest.mark.parametrize("name, code", [("Avalanche", 200),
                                        ("Ben Parker", 200),
                                        ("BenParker", 400),
                                        ("Ben_Parker", 400),
                                        ("mark", 400)])
def test_get_character_by_name(ivi_api, name, code):
    """
    Отправляем запрос на получение всех записей персонажа по имени.
    Проверяем код ответа, длину JSON, наличие ключа 'name' у первой записи.
    Тест имеет параметры для проверки 4 разных вариантов запроса


    :param ivi_api: фикстура из файла conftest.py, срабатывающая на каждый запуск теста. В параметрах записывается end point
    :type ivi_api: функция
    :param name: передаем различный вариант запроса персонажа по имени
    :type name: string
    :param code: передаем ожидаемый код ответа
    :type code: integer
    """
    r = ivi_api.get('/character', params={"name": {name}})
    assert r.status_code == code


def test_post_create_character(ivi_api):
    """
    Создаем нового персонажа методом POST, передаем хедер. Далее проверяем кол-во записей в БД так как не может быть больше 500 и код ответа. В случае ошибок выводится соответствующий текст


    :param ivi_api: фикстура из файла conftest.py, срабатывающая на каждый запуск теста. В параметрах записывается end point
    :type ivi_api: функция
    """
    r = ivi_api.post('/character', headers={'Content-type': 'application/json'},
                     json=data)
    r_get = ivi_api.get('/characters')
    assert len(r_get.json()['result']) < 500, "Достигнуто ограничение на количество персонажей. Максимальнок количество - 500 "
    assert r.status_code == 200, f'Ошибка, код ответа = {r.status_code}, а не 200. Текст ошибки: {r.json()["error"]}'


def test_post_create_character_wrong_headers(ivi_api):
    """
    Отправляем запрос с неправильных хедером и ожидаем код ответа 400


    :param ivi_api: фикстура из файла conftest.py, срабатывающая на каждый запуск теста. В параметрах записывается end point
    :type ivi_api: функция
    """
    r = ivi_api.post('/character', headers={'Content-type': 'application'}, json=data)
    assert r.status_code == 400, f'Ошибка, код ответа = {r.status_code}, а не 400.'


@pytest.mark.parametrize('name, universe,education, weight, height, identity, code, err',
                         [('', 'test', 'Moscow', 140, 30, 'someone', 400, "name: ['Length must be between 1 and 350.']"),
                          (666, 'test', 'Moscow', 140, 30, 'someone', 400, "name: ['Not a valid string.']"),
                          (None, 't', 'low', '123', 234, 'someone', 400, "name: ['Field may not be null.']"),
                          ('test', 't', 'low', '', 234, 'someone', 400, "weight: ['Not a valid number.']"),
                          ('test', 't', '', '123', 234, 'someone', 400, "education: ['Length must be between 1 and 350.']"),
                          ('test', 't', 312, '123', 234, 'someone', 400, "education: ['Not a valid string.']"),
                          ('test', 't', 'low', '123', '', 'someone', 400, "height: ['Not a valid number.']"),
                          ('test', '', 'low', '123', '123', 'someone', 400, "universe: ['Length must be between 1 and 350.']"),
                          ('test', 123, 'low', '123', '123', 'someone', 400, "universe: ['Not a valid string.']"),
                          ('test', 't', 'low', '123', '123', '', 400, "identity: ['Length must be between 1 and 350.']"),
                          ('test', 't', 'low', '123', '123', 666, 400, "identity: ['Not a valid string.']")])
def test_post_create_character_errors(ivi_api, name, universe, education, weight, height, identity, code, err):
    """
    Отправляем запросы, которые возвращают ошибки. Проверяем код ответа и совпадает ли текст ошибок, которые мы получаем в ответе.


    :param ivi_api: фикстура из файла conftest.py, срабатывающая на каждый запуск теста. В параметрах записывается end point
    :type ivi_api: функция
    :param name: имя персонажа
    :type name: str
    :param universe: название вселенной
    :type universe: str
    :param education: образование
    :type education: str
    :param weight: вес
    :type weight: str/int
    :param height: рост
    :type height: str/int
    :param identity: идентичность
    :type identity: int
    :param code: код ответа
    :type code: int
    :param err: текст ошибки
    :type err: str
    """
    r = ivi_api.post('/character', headers={'Content-type': 'application/json'},
                     json={"name": name,
                           "universe": universe,
                           "education": education,
                           "weight": weight,
                           "height": height,
                           "identity": identity})
    print(r.json())
    assert r.status_code == code
    assert r.json()['error'] == err


@pytest.mark.parametrize('name, text, code', [('Optimus', {'result': 'Hero Optimus is deleted'}, 200),
                                              ('Optimus Prime', {'result': 'Hero Optimus Prime is deleted'}, 200)])
def test_del_new_character(ivi_api, name, text, code):
    """
    Создаем персонаж, проверяем код ответа. Выполняем удаление созданного только что персонажа по его имени. Проверяем совпадает ли текст ответа с тем, что предано в параметрах теста

    :param ivi_api: фикстура из файла conftest.py, срабатывающая на каждый запуск теста. В параметрах записывается end point
    :type ivi_api: функция
    :param name: имя персонажа
    :type name: str
    :param text: текст ответа
    :type text: str
    :param code: код ответа
    :type code: int
    """
    r = ivi_api.post('/character', headers={'Content-type': 'application/json'},
                     json={"name": name,
                           "universe": "Marvel Universe",
                           "education": "High school (unfinished)",
                           "weight": 104,
                           "height": 1.90,
                           "identity": "Publicly known"})
    assert r.status_code == code
    r_del = ivi_api.delete('/character', params={"name": name})
    print(r_del.json())
    assert r_del.status_code == code, f"Ошибка в выполнении запроса. {r_del.json()}"
    assert r_del.json() == text


def test_del_unknown_character(ivi_api):
    """
    Удаляем персонажа, которого нет в БД. Проверяем совпадает ли текст ошибки


    :param ivi_api: фикстура из файла conftest.py, срабатывающая на каждый запуск теста. В параметрах записывается end point
    :type ivi_api: функция
    """
    r = ivi_api.delete('/character', params={"name": 'Vovan'})
    print(r.json())
    assert r.json()['error'] == 'No such name'


@pytest.mark.parametrize('name, num', [('New Guy', 140)])
def test_put_update_character(ivi_api, name, num):
    f"""
    Создаем персонажа с именем {name}, 'weight' 104 и набором остальных параметров
    Проверяем создался ли персонаж(код ответа, наличие и совпадение значения {name} и 'weight' в ответе.
    
    Обновляем данные персонажа методом PUT. Меняем значение 'weight' равное {num}.
    Проверяем код ответа об успешном изменении записи
    
    Отправляем запрос на список всех персонажей в БД. Сверяем код ответа и значение 'weight' равное {num} у персонажа с именем {name}


    :param ivi_api: фикстура из файла conftest.py, срабатывающая на каждый запуск теста. В параметрах записывается end point
    :type ivi_api: функция 
    :param name: 
    :type name: 
    :param num: 
    :type num: 
    """
    ivi_api.post('/character', headers={'Content-type': 'application/json'},
                 json={"name": name,
                       "universe": "Marvel Universe",
                       "education": "High school (unfinished)",
                       "weight": 104,
                       "height": 1.90,
                       "identity": "Publicly known"})

    r = ivi_api.get('/character', params={"name": name})
    assert r.status_code == 200
    assert r.json()['result']['name'] == name
    assert r.json()['result']['weight'] == 104

    ivi_api.put('/character', headers={'Content-type': 'application/json'},
                json={"name": name,
                      "universe": "Marvel Universe",
                      "education": "High school (unfinished)",
                      "weight": num,
                      "height": 1.90,
                      "identity": "Publicly known"})
    assert r.status_code == 200

    r = ivi_api.get('/character', params={"name": name})
    assert r.status_code == 200
    assert r.json()['result']['name'] == name
    assert r.json()['result']['weight'] == num

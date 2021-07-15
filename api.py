import json
import pytest
import string
import random
import allure


def long_name(len):
    """
    Функция генерит и возвращает случайную строку определнной длины, передааемой параметров в функцию.


    :param len: Длина строка
    :type len: int
    :return: сгенерированная строка
    :rtype: str
    """
    letters = string.ascii_letters
    rand_string = ''.join(random.choice(letters) for i in range(len))
    return rand_string


data = {"name": "Test",
        "universe": "Marvel Universe",
        "education": "High school (unfinished)",
        "weight": 104,
        "height": 1.90,
        "identity": "Publicly known"}


@allure.feature('Запрос записей из БД')
@allure.story('Получение всех записей из БД')
def test_get_characters(ivi_api):
    """
    Отправляем запрос на получение всех записей по персонажам.
    Проверяем код ответа, длину JSON, наличие ключа 'name' у первой записи.
    Используем проверку try/except так как возможна ошибка в написании url. Данная проверка ловит ошибку "json.decoder.JSONDecodeError". В случае срабатывания части кода, выдается ошибка с текстом и ссылкой на ту строку, к которой идет обращение


    :param ivi_api: фикстура из файла conftest.py, срабатывающая на каждый запуск теста. В параметрах записывается end point
    :type ivi_api: функция
    """
    try:
        with allure.step('Отправили GET запрос'):
            r = ivi_api.get('/characters')
            r_len = len(r.json()["result"])
        with allure.step('Проверяем код ответа'):
            assert r.status_code == 200, f'Ошибка, код ответа = {r.status_code}, а не 200'
        with allure.step('Проверяем кол-во записей'):
            assert r_len != None, f"Ошибка, длина записи 'result' должно быть больше 0. Текущая длина записи {r_len}"
        with allure.step('Проверяем есть ли поле "name" в первой записи'):
            assert r.json()['result'][0]['name'] != None, "Ошибка, отсутствует поле Name в выдаче"
    except json.decoder.JSONDecodeError:
        raise ValueError(f"Ошибка в URL строке: {r.url}")


@allure.feature('Запрос записей из БД')
@allure.story('Получение записи из БД по имени')
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

    with allure.step('Отправляем GET запрос на сервер'):
        r = ivi_api.get('/character', params={"name": {name}})
    with allure.step('Проверяем код ответа'):
        assert r.status_code == code


@allure.feature('Создание записи в БД')
@allure.story('Успешное создание новой записи, испульзуя различные кейсы проверки полей')
@pytest.mark.parametrize('name, universe,education, weight, height, identity, code',
                         [(long_name(1), 'test', 'Moscow', 140, 30, 'someone', 200),
                          (long_name(2), 'test', 'Moscow', 140, 30, 'someone', 200),
                          (long_name(349), 'test', 'Moscow', 140, 30, 'someone', 200),
                          (long_name(350), 'test', 'Moscow', 140, 30, 'someone', 200),
                          ('test', long_name(1), 'Moscow', 140, 30, 'someone', 200),
                          ('test', long_name(2), 'Moscow', 140, 30, 'someone', 200),
                          ('test', long_name(349), 'Moscow', 140, 30, 'someone', 200),
                          ('test', long_name(350), 'Moscow', 140, 30, 'someone', 200),
                          ('test', 'test', long_name(1), 140, 30, 'someone', 200),
                          ('test', 'test', long_name(2), 140, 30, 'someone', 200),
                          ('test', 'test', long_name(349), 140, 30, 'someone', 200),
                          ('test', 'test', long_name(350), 140, 30, 'someone', 200),
                          ('test', 'test', 'Moscow', 140, 30, long_name(1), 200),
                          ('test', 'test', 'Moscow', 140, 30, long_name(2), 200),
                          ('test', 'test', 'Moscow', 140, 30, long_name(349), 200),
                          ('test', 'test', 'Moscow', 140, 30, long_name(350), 200),
                          ('test', 'test', 'Moscow', 0, 30, 'Moscow', 200),
                          ('test', 'test', 'Moscow', -10, 30, 'Moscow', 200),
                          ('test', 'test', 'Moscow', 140, 0, 'Moscow', 200),
                          ('test', 'test', 'Moscow', 140, -20, 'Moscow', 200),
                          ])
def test_post_create_character(ivi_api, name, universe, education, weight, height, identity, code):
    """
    Создаем нового персонажа методом POST, передаем хедер. Далее проверяем кол-во записей в БД так как не может быть больше 500 и код ответа. В случае ошибок выводится соответствующий текст


    :param ivi_api: фикстура из файла conftest.py, срабатывающая на каждый запуск теста. В параметрах записывается end point
    :type ivi_api: функция
    """
    with allure.step('Отправляем POST запрос на сервер и передаем данные из маркировки Parametrize'):
        r = ivi_api.post('/character', headers={'Content-type': 'application/json'},
                         json={"name": name,
                               "universe": universe,
                               "education": education,
                               "weight": weight,
                               "height": height,
                               "identity": identity})
    with allure.step('Отправляем GET запрос на сервер'):
        r_get = ivi_api.get('/characters')
    with allure.step('Проверяем кол-во записей на сервере. Должно быть не более 500 шт'):
        assert len(r_get.json()['result']) < 500, "Достигнуто ограничение на количество персонажей. Максимальнок количество - 500 "
    with allure.step('Проверяем код овтета POST запроса'):
        assert r.status_code == 200, f'Ошибка, код ответа = {r.status_code}, а не 200. Текст ошибки: {r.json()["error"]}'


@allure.feature('Создание записи в БД')
@allure.story('Неуспешное создание записи при передаче неправильного headers')
def test_post_create_character_wrong_headers(ivi_api):
    """
    Отправляем запрос с неправильных хедером и ожидаем код ответа 400


    :param ivi_api: фикстура из файла conftest.py, срабатывающая на каждый запуск теста. В параметрах записывается end point
    :type ivi_api: функция
    """
    with allure.step('Отправялем POST запрос с неправильных headers'):
        r = ivi_api.post('/character', headers={'Content-type': 'application'}, json=data)
    with allure.step('Проверяем код ответа. Код должен быть 400'):
        assert r.status_code == 400, f'Ошибка, код ответа = {r.status_code}, а не 400.'


@allure.feature('Создание записи в БД')
@allure.story('Неуспешное создание новой записи, испульзуя различные кейсы проверки полей')
@pytest.mark.parametrize('name, universe, education, weight, height, identity, code, err',
                         [('', 'test', 'Moscow', 140, 30, 'someone', 400, "name: ['Length must be between 1 and 350.']"),
                          (666, 'test', 'Moscow', 140, 30, 'someone', 400, "name: ['Not a valid string.']"),
                          (None, 't', 'low', '123', 234, 'someone', 400, "name: ['Field may not be null.']"),
                          (long_name(351), 't', 'low', '123', 234, 'someone', 400, "name: ['Length must be between 1 and 350.']"),
                          ('test', '', 'Moscow', 140, 30, 'someone', 400, "universe: ['Length must be between 1 and 350.']"),
                          ('test', 666, 'Moscow', 140, 30, 'someone', 400, "universe: ['Not a valid string.']"),
                          ('test', None, 'low', '123', 234, 'someone', 400, "universe: ['Field may not be null.']"),
                          ('test', long_name(351), 'low', '123', 234, 'someone', 400, "universe: ['Length must be between 1 and 350.']"),
                          ('test', 'test', '', 140, 30, 'someone', 400, "education: ['Length must be between 1 and 350.']"),
                          ('test', 'test', 666, 140, 30, 'someone', 400, "education: ['Not a valid string.']"),
                          ('test', 'test', None, '123', 234, 'someone', 400, "education: ['Field may not be null.']"),
                          ('test', 'test', long_name(351), '123', 234, 'someone', 400, "education: ['Length must be between 1 and 350.']"),
                          ('test', 'test', 'test', 140, 30, '', 400, "identity: ['Length must be between 1 and 350.']"),
                          ('test', 'test', 'test', 140, 30, 666, 400, "identity: ['Not a valid string.']"),
                          ('test', 'test', 'test', '123', 234, None, 400, "identity: ['Field may not be null.']"),
                          ('test', 'test', 'test', '123', 234, long_name(351), 400, "identity: ['Length must be between 1 and 350.']"),
                          ('test', 't', 'low', '', 234, 'someone', 400, "weight: ['Not a valid number.']"),
                          ('test', 't', 'low', '123', '', 'someone', 400, "height: ['Not a valid number.']"),
                          ])
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
    with allure.step('Отправляем POST запрос на сервер и передаем данные из маркировки Parametrize'):
        r = ivi_api.post('/character', headers={'Content-type': 'application/json'},
                         json={"name": name,
                               "universe": universe,
                               "education": education,
                               "weight": weight,
                               "height": height,
                               "identity": identity})
    with allure.step('Проверяем код ответа'):
        assert r.status_code == code
    with allure.step('Проверяем текст ошибки'):
        assert r.json()['error'] == err


@allure.feature('Удаление записи из БД')
@allure.story('Удаление созданой новой записи, испульзуя различные кейсы')
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
    with allure.step('Создаем запись, отправляем POST запрос на сервер'):
        r = ivi_api.post('/character', headers={'Content-type': 'application/json'},
                         json={"name": name,
                               "universe": "Marvel Universe",
                               "education": "High school (unfinished)",
                               "weight": 104,
                               "height": 1.90,
                               "identity": "Publicly known"})
    with allure.step('Проверяем код ответа создания записи'):
        assert r.status_code == code
    with allure.step('Отправляем DELETE запрос на сервер и передаем имя созданной записи'):
        r_del = ivi_api.delete('/character', params={"name": name})
    with allure.step('Проверяем код ответа DELETE запроса'):
        assert r_del.status_code == code, f"Ошибка в выполнении запроса. {r_del.json()}"
    with allure.step('Проверяем текст ответа записи, должен совпадать с шаблоном'):
        assert r_del.json() == text
    with allure.step('Отправляем GET запрос на сервер c именем удаленной записи'):
        r_get = ivi_api.get('/character', params={"name": {name}})
    with allure.step('Проверяем код ответа GET запроса, должен быть 400'):
        assert r_get.status_code == 400
    with allure.step('Отправляем GET запрос на сервер c именем удаленной записи, получаем текст ошибки'):
        assert r_get.json() == {'error': 'No such name'}


@allure.feature('Удаление записи из БД')
@allure.story('Удаление несуществующей записи')
def test_del_unknown_character(ivi_api):
    """
    Удаляем персонажа, которого нет в БД. Проверяем совпадает ли текст ошибки


    :param ivi_api: фикстура из файла conftest.py, срабатывающая на каждый запуск теста. В параметрах записывается end point
    :type ivi_api: функция
    """

    with allure.step('Отправляем DELETE запрос на сервер и передаем имя несуществующей записи'):
        r = ivi_api.delete('/character', params={"name": 'Vovan'})
    with allure.step('Проверяем код ответа'):
        assert r.status_code == 400
    with allure.step('Проверяем текст ответа'):
        assert r.json()['error'] == 'No such name'


@allure.feature('Изменение записи в БД')
@allure.story('Создание и изменение записи')
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
    with allure.step('Создаем запись, отправляя POST запрос на сервер'):
        ivi_api.post('/character', headers={'Content-type': 'application/json'},
                     json={"name": name,
                           "universe": "Marvel Universe",
                           "education": "High school (unfinished)",
                           "weight": 104,
                           "height": 1.90,
                           "identity": "Publicly known"})
    with allure.step('Отправляем GET запрос на сервер с созданным именем'):
        r = ivi_api.get('/character', params={"name": name})
    with allure.step('Проверяем код ответа GET запроса'):
        assert r.status_code == 200
    with allure.step('Проверяем значение "name" в полученной записи'):
        assert r.json()['result']['name'] == name
    with allure.step('Проверяем значение "weight" в полученной записи'):
        assert r.json()['result']['weight'] == 104
    with allure.step('Отправляем PUT запрос на сервер с существующем именем и новым значением "weight"'):
        ivi_api.put('/character', headers={'Content-type': 'application/json'},
                    json={"name": name,
                          "universe": "Marvel Universe",
                          "education": "High school (unfinished)",
                          "weight": num,
                          "height": 1.90,
                          "identity": "Publicly known"})
    with allure.step('Проверяем код ответа PUT запроса'):
        assert r.status_code == 200
    with allure.step('Отправляем GET запрос на сервер с тем же именем'):
        r = ivi_api.get('/character', params={"name": name})
    with allure.step('Проверяем код ответа GET запроса'):
        assert r.status_code == 200
    with allure.step('Проверяем значение "name" в полученной записи'):
        assert r.json()['result']['name'] == name
    with allure.step('Проверяем значение "weight" в полученной записи. Должно измениться на новое значение'):
        assert r.json()['result']['weight'] == num

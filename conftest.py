import requests
import pytest
import os


@pytest.fixture()
def api():
    """
    Возвращает объект, через который можно обращаться к методам GET, POST, PUT, DELETE


    :return:
    :rtype: obj
    """
    return ApiClient(base_url='http://rest.test.ivi.ru/v2')


@pytest.fixture(autouse=True)
def reset(api):
    """
    Фикстура, которая возвращает изначальное состояние БД. Запускает при каждом вызове функции, чтобы тесты не зависели друг от друга.
    Взаимосвязь между разными методами вызовов (создание - изменение - удаление) работает исключительно в одном тесте


    :param api:
    :type api:
    :return:
    :rtype:
    """
    return api.post('/reset')


class ApiClient:

    def __init__(self, base_url):
        """
        Конструктор класса, который принимает в себя базовый url для дальнейшей работы с методами


        :rtype: object
        """
        self.base_url = base_url

    def get(self, path='/', params=None, headers=None):
        """
        Метод GET. Может принимать в кач-ве параметров end point, параметры, хедеры
        Возвращает ответ от серверу с методом GET с учетом переданных параметров и end point


        :param path: End point
        :type path: str
        :param params: дополнительные параметры запроса
        :type params: str
        :param headers: дополнительные хедеры, если они необходимы
        :type headers: str
        """
        url = f"{self.base_url}{path}"
        return requests.get(url, auth=(os.getenv('LOG'), os.getenv('PAS')), params=params, headers=headers)

    def post(self, path="/", json=None, headers=None):
        """
        Метод POST. Может принимать в кач-ве параметров end point, json, хедеры
        Возвращает ответ от серверу с методом POST с учетом переданных параметров и end point


        :param path: End point
        :type path: str
        :param json: параметр в формате JSON для обработки запроса
        :type json: str
        :param headers: дополнительные хедеры, если они необходимы
        :type headers: str
        """
        url = f"{self.base_url}{path}"
        return requests.post(url=url, auth=(os.getenv('LOG'), os.getenv('PAS')),
                             json=json,
                             headers=headers)

    def put(self, path="/", json=None, headers=None):
        """
        Метод PUT. Может принимать в кач-ве параметров end point, json, хедеры
        Возвращает ответ от серверу с методом PUT с учетом переданных параметров и end point


        :param path: End point
        :type path: str
        :param json: параметр в формате JSON для обработки запроса
        :type json: str
        :param headers: дополнительные хедеры, если они необходимы
        :type headers: str
        """
        url = f"{self.base_url}{path}"
        return requests.put(url=url, auth=(os.getenv('LOG'), os.getenv('PAS')),
                            json=json,
                            headers=headers)

    def delete(self, path="/", params=None, headers=None):
        """
        Метод DELETE. Может принимать в кач-ве параметров end point, параметры, хедеры
        Возвращает ответ от серверу с методом DELETE с учетом переданных параметров и end point


        :param path: End point
        :type path: str
        :param params: дополнительные параметры запроса
        :type params: str
        :param headers: дополнительные хедеры, если они необходимы
        :type headers: str
        """
        url = f"{self.base_url}{path}"
        return requests.delete(url=url, auth=(os.getenv('LOG'), os.getenv('PAS')), params=params, headers=headers)

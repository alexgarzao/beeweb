import json
import requests
from .utils import pretty_json


# TODO: Talvez teriamos GetRequest, PostRequest, DeleteRequest, ...
class Request:
    def __init__(self, event):
        self.__event = event
        self.__resource = event.resource
        self.__headers = self.__resource.get_initial_headers()
        self.__parameters = self.__resource.get_initial_parameters()
        self.__body = self.__resource.get_initial_body()

    def set_field_value(self, alias, value):
        field = self.__resource.get_field(alias)
        assert field is not None, 'Alias %s nao encontrado' % alias

        name = field.json_name
        value = field.transform_value(value)
        location = field.location

        if location == 'header':
            self.__headers[name] = value
        elif location == 'path':
            self.__parameters[name] = value
        elif location == 'body':
            self.__body[name] = value
        else:
            assert False, "Undefined location {}!".format(location)

    def __get(self, url):
        try:
            self.url = url
            self.retorno = requests.get(self.url, headers=self.__headers)
            return self.retorno
        except Exception as e:
            raise e

    def __post(self, url):
        try:
            self.url = url
            self.retorno = requests.post(self.url, headers=self.__headers, json=self.__body)
            return self.retorno
        except Exception as e:
            raise e

    def __put(self, url):
        try:
            self.url = url
            self.retorno = requests.put(self.url, headers=self.__headers, json=self.__body)
            return self.retorno
        except Exception as e:
            raise e

    def __delete(self, url):
        try:
            self.url = url
            self.retorno = requests.delete(self.url, headers=self.__headers, json=self.__body)
            return self.retorno
        except Exception as e:
            raise e

    def send(self):
        # print("Method: {}\nURL: {}\nParameters: {}\n".format(self.method, self.__get_url(), self.parameters))
        if self.__event.method == 'POST':
            self.__post(self.__get_url())
        elif self.__event.method == 'GET':
            self.__get(self.__get_url())
        elif self.__event.method == 'PUT':
            self.__put(self.__get_url())
        elif self.__event.method == 'DELETE':
            self.__delete(self.__get_url())
        else:
            assert False

        if self.retorno.status_code >= 200 and self.retorno.status_code <= 201 and self.retorno.text:
            self.result = self.retorno.json()
        else:
            self.result = {}

    def check_result(self, status_code):
        self.validar_retorno(status_code)

    def __get_url(self):
        path = self.__replace_parameters(self.__event.path, self.__parameters)
        return self.__resource.base_url + '/' + path

    def __replace_parameters(self, text, parameters):
        for parameter, value in parameters.items():
            if type(value) is not str and type(value) is not int:
                continue
            field = self.__resource.get_field_by_name(parameter)
            token_to_find = "{" + field.alias + "}"
            text = text.replace(token_to_find, str(value))

        return text

    # def post_image(self, caminho_imagem):
    #     try:
    #         url = self.url
    #         self.last_parameters = None
    #         self.retorno = requests.post(url, files={'file': open(caminho_imagem, 'rb')})
    #         return self.retorno
    #     except Exception as e:
    #         raise e
    #

    def validar_retorno(self, retorno_esperado):
        json_enviado = json.dumps(self.__parameters, indent=4, sort_keys=True, separators=(',', ': '))
        if self.retorno.status_code >= 200 and self.retorno.status_code <= 201 and self.retorno.text:
            json_recebido = json.dumps(self.retorno.json(), indent=4, sort_keys=True, separators=(',', ': '))
        else:
            json_recebido = self.retorno.text
        assert self.retorno.status_code == retorno_esperado, \
            "O resultado esperado [{}] e diferente do retorno [{}].\n\tURL={}\n\tParametros enviados={}\n\tRetorno={}".\
            format(retorno_esperado, self.retorno.status_code, self.url, json_enviado, json_recebido)

        self._verify_error_response(self.retorno)

    def success(self):
        return self.retorno.status_code >= 200 and self.retorno.status_code <= 204

    def assert_result(self, field_name, expected_result):
        json_enviado = json.dumps(self.__parameters, indent=4, sort_keys=True, separators=(',', ': '))
        if self.retorno.status_code >= 200 and self.retorno.status_code <= 201:
            json_recebido = json.dumps(self.retorno.json(), indent=4, sort_keys=True, separators=(',', ': '))
        else:
            json_recebido = self.retorno.text
        result = self.retorno.json()[field_name]
        assert result == expected_result, \
            "O resultado esperado [%s] e diferente do retorno [%s].\n\tURL=%s\n\tParametros enviados=%s\n\tRetorno=%s" % (expected_result, result, self.url, json_enviado, json_recebido)

    def json_return_value(self, key):
        msg = 'Chave %s nao encontrada no retorno: %s' % (key, pretty_json(self.retorno.json()))
        assert key in self.retorno.json(), msg
        return self.retorno.json()[key]

    def _verify_error_response(self, api_response):
        """ Verifica a estrutura de retorno em caso de erro. """
        if api_response.status_code < 400 or api_response.status_code > 499:
            return

        try:
            api_response.json()
        except Exception as e:
            if api_response.status_code == 404:
                return
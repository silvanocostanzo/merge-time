import requests.exceptions

import main
from main import Main



def helper_write_to_file(mocker, val: bool):
    mock_exists = mocker.patch('os.path.exists')
    mock_exists.return_value = val
    mock_open = mocker.patch('builtins.open')
    mock_json_dump = mocker.patch('json.dump')
    dummy_pr = [{
        'id': 1,
        'title': 'a title',
        'user': ' a user'
    }]
    main.write_prs_to_file(dummy_pr)
    mock_open.assert_called()
    mock_json_dump.assert_called()


def helper_mock_json_func_OK():
    return "a response"


def helper_mock_json_func_KO():
    raise requests.exceptions.JSONDecodeError


def test_write_prs_to_file(mocker):
    helper_write_to_file(mocker, True)
    helper_write_to_file(mocker, False)


def test_get_token_OK(mocker):
    mock_os_getenv = mocker.patch('os.getenv')
    mock_os_getenv.return_value = 'a token'
    want = 'a token'
    got = Main.get_token()
    assert got == want


class TestMain:

    def test_get_request(self, mocker):
        mock_main_get_token = mocker.patch('main.Main.get_token')
        mock_main_get_token.return_value = 'a token'
        mock_requests_get = mocker.patch('requests.get')
        mock_requests_get.return_value.json = helper_mock_json_func_OK
        mock_requests_get.return_value.ok = True
        my_instance = Main('owner', 'repo')
        want = 'a response'
        got = my_instance.get_request("localhost")
        assert want == got.json()

    def test_get_pr_OK(self, mocker):
        mock_requests_get = mocker.patch('requests.get')
        mock_requests_get.return_value.json = helper_mock_json_func_OK
        my_instance = Main('owner', 'repo')
        want = 'a response'
        got = my_instance.get_pr('123')
        assert got == want

    def test_get_prs(self, mocker):
        dummy_prs = ['1', '2']
        mock_get_pr = mocker.patch('main.Main.get_pr')
        mock_get_pr.return_value = 'a pr'
        my_instance = Main('owner', 'repo')
        got = my_instance.get_prs(dummy_prs)
        assert ['a pr', 'a pr'] == got

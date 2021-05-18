from users import NormalUser, User, Administrator
import mock
from main import BankingSystem, UserDb
import stdiomask


def test_username_password_check():
    """
    Test username_password_check
    :return:
    """
    nu = NormalUser("test", "00/00/0000", "test_user", "test_pass")

    assert nu.check_username_password("test_user", "not_my_password") == False
    assert nu.check_username_password("test_user", "test_pass") == True


def test_get_tuple():
    nu = NormalUser("test", "00/00/0000", "test_user", "test_pass", id=123456)
    ad = Administrator("test", "test_user", "test_pass", id=123456)

    assert nu.get_tuple() == (123456, "test", "00/00/0000", 0, "test_user", "test_pass")
    assert ad.get_tuple() == (123456, "test", "test_user", "test_pass")


def test_request_login():
    db = UserDb()
    sys = BankingSystem(db)

    with mock.patch.object(__builtins__, 'input', lambda: 'username'):
        with mock.patch.object(stdiomask, 'getpass', lambda: 'password'):
            assert sys.request_login(3) is not None

    with mock.patch.object(__builtins__, 'input', lambda: 'notusername'):
        with mock.patch.object(stdiomask, 'getpass', lambda: 'notpassword'):
            assert sys.request_login(3) is None

def test_get_command():
    db = UserDb()
    sys = BankingSystem(db)

    with mock.patch.object(__builtins__, 'input', lambda: 'create user'):
        assert sys.get_command() == ['create', 'user']

    with mock.patch.object(__builtins__, 'input', lambda: 'deposit $500'):
        assert sys.get_command() == ['deposit', '500']

    with mock.patch.object(__builtins__, 'input', lambda: ''):
        assert sys.get_command() is None
        assert sys.error_str == "No command was given"

def test_login_user():




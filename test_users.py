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

    assert nu.get_tuple() == (123456, "test", "00/00/0000", 0.0, "test_user", "test_pass")
    assert ad.get_tuple() == (123456, "test", "test_user", "test_pass")


def test_login_user():
    db = UserDb()
    user = db.login_user('cyan', 'cyan')

    assert user.name == 'cyanbrown'
    assert user.id == 627189



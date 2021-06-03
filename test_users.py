from users import NormalUser, User, Administrator
from main import BankingSystem, UserDb


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

    assert nu.get_tuple() == (123456, "test", "00/00/0000", 0.0, "test_user", "test_pass", False)
    assert ad.get_tuple() == (123456, "test", "2001-01-01", 0.0, "test_user", "test_pass", True)


def test_login_user():
    db = UserDb()
    user = db.login_user('user', 'user')

    assert user.name == 'user'
    assert user.id == 68061


def test_get_command():
    db = UserDb()
    bs = BankingSystem(db)

    assert bs.get_command(['withdraw', '100']) == ['withdraw', '100']
    assert bs.get_command([]) is None


def test_deposit():
    db = UserDb()
    bs = BankingSystem(db)

    # load admin user
    user = db.login_user("user", "user")

    # use bs deposit
    bs.user = user
    bs.deposit("500")

    assert bs.error_str == "Administrators cannot deposit."

    # load normal user
    user = db.login_user("normal", "normal")

    # use bs deposit
    bs.user = user
    bs.deposit("salksjdf")

    assert bs.error_str == "Amount of money to deposit is invalid."

    previous_balance = bs.user.balance
    bs.deposit("500")

    assert previous_balance + 500 == bs.user.balance


def test_withdraw():
    db = UserDb()
    bs = BankingSystem(db)

    # load admin user
    user = db.login_user("user", "user")

    # use bs deposit
    bs.user = user
    bs.withdraw("500")

    assert bs.error_str == "Administrators cannot withdraw."

    # load normal user
    user = db.login_user("normal", "normal")

    # use bs deposit
    bs.user = user
    bs.withdraw("salksjdf")

    assert bs.error_str == "Amount of money to withdraw is invalid."

    previous_balance = bs.user.balance
    bs.withdraw("500")

    assert previous_balance - 500 == bs.user.balance


def test_save_user():
    db = UserDb()

    # testing normal user
    user = db.login_user("normal", "normal")

    user.balance += 500
    new_balance = user.balance

    db.save_user(user)
    user = db.login_user("normal", "normal")

    assert user.balance == new_balance

    # testing admin user
    user = db.login_user("brown", "brown")

    user.name += "n"
    new_name = user.name

    db.save_user(user)
    user = db.login_user("brown", "brown")

    assert user.name == new_name

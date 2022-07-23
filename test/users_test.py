import pytest
import pytest_mock
from model.user import User
from exception.log_in_error import LogInError
from service.users_service import UserService


def test_user_login_positive(mocker):
    # Arrange
    def mock_user_login(username, password):
        if username == "bipul513" and password == "password":
            return User("bach21", "Bach", "Tran", "employee")
        raise LogInError("Username and Password does not match. Please try again with correct credentials !!!")

    mocker.patch("dao.users_dao.UsersDao.user_login", mock_user_login)

    # ACT
    actual = UserService.user_login("bipul513", "password")

    # Assert
    actual == User("bach21", "Bach", "Tran", "employee")


def test_user_login_negative(mocker):
    # Arrange
    def mock_user_login(username, password):
        if username == "bipul513" and password == "password":
            return User("bach21", "Bach", "Tran", "employee")
        raise LogInError("Username and Password does not match. Please try again with correct credentials !!!")

    mocker.patch("dao.users_dao.UsersDao.user_login", mock_user_login)

    # ACT & Assert
    with pytest.raises(LogInError) as e:
        actual = UserService.user_login("bipul513", "apple")

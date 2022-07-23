from dao.users_dao import UsersDao
from exception.user_name_not_found import UserNotFoundError
from exception.log_in_error import LogInError
from model.user import User


class UserService:
    @staticmethod
    def user_login(username, password):
        user_info = UsersDao.user_login(username, password)
        if user_info:
            print(f"user_info is {user_info}")
            return user_info.to_dict()
        raise LogInError("Username and Password does not match. Please try again with correct credentials !!!")

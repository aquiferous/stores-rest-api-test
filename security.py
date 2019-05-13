from werkzeug.security import safe_str_cmp # safe string compare
from models.user import UserModel

def authenticate(username, password):
    """
    Function that gets called when a user calls the /auth endpoint
    with their username / password

    :param username: User's username in string format
    :param password: User's un-encrypted password in string format
    :return: A UserModel object if authentication is successful. None, otherwise
    """

    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    """
    Function that gets called when user has aleady authenticated, and Flask-JWT
    verified their authorization header is correct.

    :param payload: A dictionary with 'identity' key, which is the user id
    :return: A UserModel object
    """

    user_id = payload['identity']
    return UserModel.find_by_id(user_id)

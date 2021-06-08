from .models import Account

class EmailAuthBackend(object):
  """
  Authenticate a user via email address
  """
  def authenticate(self, request, username=None, password=None):
    try:
      user_account = Account.objects.get(email=username)
      if user_account.check_password(password):
        return user_account
      return None
    except Account.DoesNotExist:
      return None
  
  def get_user(self, user_id):
    try:
      user = Account.objects.get(id=user_id)
    except Account.DoesNotExist:
      user = None
    return user
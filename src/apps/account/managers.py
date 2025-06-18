from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def get_by_natural_key(self, phone):
        return self.get(**{self.model.USERNAME_FIELD: phone })


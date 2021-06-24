from django.contrib.auth.mixins import UserPassesTestMixin


class HasAdminAccessMixin(UserPassesTestMixin):
    pass

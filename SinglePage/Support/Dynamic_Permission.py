from SinglePage.general_view_with_sqlalchemy import GeneralViewWithSQLAlchemy
from permissions.permissions import need_auth_header


class Dynamic_permission(GeneralViewWithSQLAlchemy):
    """docstring for Dynamic_permission"""
    permission_config = None
    login_class = None
    user_class = None
    user = None
    base = None

    def getattr_permission(self):
        self.permission = getattr(self, self.user.permissions, None)
        if self.permission is not None:
            self.set_permission(self.permission)
        else:
            raise Exception('no such permissoin: %s' %
                            self.user.permissions or 'none')

    def get_permission_passed(self, pk):
        permission = need_auth_header
        passed, memo, status_code = permission().get(
            self.db_session, self.object, pk, self)
        if not passed:
            return passed, permission, memo, status_code
        self.getattr_permission()
        return super(Dynamic_permission, self).get_permission_passed(pk)

    def put_permission_passed(self, pk):
        permission = need_auth_header
        passed, memo, status_code = permission().put(
            self.db_session, self.object, pk, self)
        if not passed:
            return passed, permission, memo, status_code
        self.getattr_permission()
        return super(Dynamic_permission, self).put_permission_passed(pk)

    def post_permission_passed(self):
        permission = need_auth_header
        passed, memo, status_code = permission().post(
            self.db_session, self.object, self)
        if not passed:
            return passed, permission, memo, status_code
        self.getattr_permission()
        return super(Dynamic_permission, self).post_permission_passed()

    def delete_permission_passed(self, pk):
        permission = need_auth_header
        passed, memo, status_code = permission().delete(
            self.db_session, self.object, pk, self)
        if not passed:
            return passed, permission, memo, status_code
        self.getattr_permission()
        return super(Dynamic_permission, self).delete_permission_passed(pk)

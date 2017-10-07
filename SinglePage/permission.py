class permission(object):

    def get(self, db_session, cls, pk, handler):
        'get permission'
        return True, None, 200

    def post(self, db_session, cls, handler):
        'post permission'
        return True, None, 200

    def put(self, db_session, cls, pk, handler):
        'put permission'
        return True, None, 200

    def delete(self, db_session, cls, pk, handler):
        'delete permission'
        return True, None, 200

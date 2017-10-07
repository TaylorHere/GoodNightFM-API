# coding:utf-8
class Dynic_permission_config():
    resources = {
        # 资源和对应方法的权限
        # resources :   GET,  POST, PUT,  DELETE
        # Escort    :  (True, True, True, True,),

    }

    fields = {
        # 资源和对应方法中字段的权限
        # resources :   POST,             PUT
        # Escort    : (('escortor_id'), ('escortor_id')),
    }

    def get(self, db_session, cls, request, pk):
        """you don't have this permission"""
        for r in self.resources:
            if r == cls:
                return self.resources[r][0]

    def post(self, db_session, cls, request):
        """you don't have this permission"""
        for r in self.resources:
            if r == cls:
                for f in self.fields:
                    if request.get_json().get(self.fields[f][0], None):
                        return False
                return self.resources[r][1]

    def put(self, db_session, cls, request, pk):
        """you don't have this permission"""
        for r in self.resources:
            if r == cls:
                for f in self.fields:
                    if request.get_json().get(self.fields[f][0], None):
                        return False
                return self.resources[r][2]

    def delete(self, db_session, cls, request, pk):
        """you don't have this permission"""
        for r in self.resources:
            if r == cls:
                return self.resources[r][3]

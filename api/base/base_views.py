

from api.base.api_view import CustomAPIView
from api.base.authentication import TokenAuthentication
from config.contanst import ADMIN_ROLE
from models.post.models import Post
from models.user.models import User
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions, HTTP_HEADER_ENCODING

class BaseAuthenticationView(CustomAPIView):
    authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    user = None
    # authorize = None

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.user = request.user
        role_list = kwargs.get("ROLE", [])
        self.check_permission(role_list)
    
    def check_permission(self, role_list):
        allow = True
        user = self.user           
        if len(role_list):
            if user.role not in role_list:
                allow = False  

        if not allow:
            raise exceptions.PermissionDenied({
                'error_code': "PERMISSION_DENIED",
                'description': "PERMISSION_DENIED",
            })

    def check_permission_by_user_type(self, pk, type_api):
        user = self.user
        allow = True

        if type_api == "POST":
            allow = self.check_permission_post(user, pk)

        elif type_api == "CATEGORY":
            allow = self.check_permission_category(user, pk)

        elif type_api == "TAG":
            allow = self.check_permission_tag(user, pk)

        elif type_api == "USER":
            allow = self.check_permission_user(user, pk)

        if not allow:
            raise exceptions.PermissionDenied({
                'error_code': "PERMISSION_DENIED",
                'description': "PERMISSION_DENIED",
            })
    
    def check_permission_post(self, user, pk):
        post = Post.objects.filter(pk=pk).first()
        if post:
            if user.id != post.author_id and user.role < ADMIN_ROLE:
                return False
        return True

    def check_permission_category(self, user, pk):
        pass

    def check_permission_tag(self, user, pk):
        pass

    def check_permission_user(self, user, pk):
        pass

class BaseView(CustomAPIView):

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)



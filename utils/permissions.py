from rest_framework import permissions
import copy

class CustomDjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self):
        # Usar deepcopy para copiar los permisos y evitar problemas con el diccionario original
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']

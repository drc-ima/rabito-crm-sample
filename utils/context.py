class PermLookupDict:
    def __init__(self, user, perm_name):
        self.user = user
        self.perm_name = perm_name
    
    def __repr__(self):
        try:
            return str(self.user.has_role_perm(self.perm_name))
        except:
            return ''

    def __getitem__(self, perm_name):
        # print(self.perm_name)
        return self.user.has_role_perm(perm=self.perm_name)
    
    def __iter__(self):
        # To fix 'item in perms.someapp' and __getitem__ interaction we need to
        # define __iter__. See #18979 for details.
        raise TypeError("PermLookupDict is not iterable.")

    def __bool__(self):
        # if self.user.role:
        return self.user.has_role_perm(perm=self.perm_name)
        # else: return False

class PermWrapper:
    def __init__(self, user):
        self.user = user

    def __getitem__(self, perm_name):
        
        return PermLookupDict(self.user, perm_name)

    def __iter__(self):
        # I am large, I contain multitudes.
        raise TypeError("PermWrapper is not iterable.")



def suth(request):

    if hasattr(request, 'user'):
        user = request.user
    else:
        from django.contrib.auth.models import AnonymousUser
        user = AnonymousUser()
    
    return {
        'role_perms': PermWrapper(user)
    }
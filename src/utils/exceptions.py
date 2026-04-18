class NotFoundError(Exception):
    pass

class ValidationError(Exception):
    pass

class DatabaseError(Exception):
    pass

class AuthenticationError(Exception):
    pass

class PermissionDeniedError(Exception):
    pass
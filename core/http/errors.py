class ApiError(Exception) :
    def __init__(self , message : str , status_code : int , payload : dict | None = None) :
        super().__init__(message)
        self.message = message,
        self.status_code = status_code
        self.status = "fail" if f"{status_code}".startswith('4') else "error"
        self.payload = payload
        
class AuthenticationError(ApiError) :
    def __init__(self , message = "Authentication failed") :
        super().__init__(message , 401)
        
class AuthorizationError(ApiError) :
    def __init__(self, message = "Access denied") :
        super().__init__(message , 403)
        
class TokenExpiredError(ApiError) :
    def __init__(self, message = "Token has expired") :
        super().__init__(message , 401)
        
class InvalidTokenError(ApiError) :
    def __init__(self, message = "Invalid Token") :
        super().__init__(message , 401)
        
class ForbiddenError(ApiError) :
    def __init__(self, message = "Access deneid") :
        super().__init__(message , 403)
        
class ValidationError(ApiError) :
    def __init__(self, message = "Validation failed") :
        super().__init__(message , 400)
        
class NotFoundError(ApiError) :
    def __init__(self, message = "Reource not found") :
        super().__init__(message , 404)
        
class RateLimitError(ApiError) :
    def __init__(self, message = "Too many requests") :
        super().__init__(message , 429)
        
class ExternalServiceError(ApiError) :
    def __init__(self, message = "External service unavailable") :
        super().__init__(message , 503)
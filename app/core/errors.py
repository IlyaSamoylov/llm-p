class BaseAppException(Exception):
	def __init__(self, detail: str = "Собственная ошибка приложения"):
		self.detail = detail
		super().__init__(detail)

class ResourceConflictError(BaseAppException):
	def __init__(self, detail: str = "Конфликт данных"):
		self.detail = detail
		super().__init__(detail)

class AuthenticationError(BaseAppException):
	def __init__(self, detail: str = "Ошибка авторизации"):
		self.detail = detail
		super().__init__(detail)

class PermissionDeniedError(BaseAppException):
	def __init__(self, detail: str = "Доступ запрещен"):
		self.detail = detail
		super().__init__(detail)

class NotFoundError(BaseAppException):
	def __init__(self, detail: str = "Запрашиваемый ресурс не найден"):
		self.detail = detail
		super().__init__(detail)

class ExternalServiceError(BaseAppException):
	def __init__(self, detail: str = "Ошибка при взаимодействии с внешним сервисом"):
		self.detail = detail
		super().__init__(detail)
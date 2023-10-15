from django.http import Http404
from ninja import NinjaAPI, schema
from ninja.errors import ValidationError


class ApiError(schema.Schema):
    title: str
    detail: str
    status: int


default_errors = {400: ApiError, 404: ApiError, 422: ApiError, 500: ApiError}


class CustomAPIException(Exception):
    def __init__(self, title: str, detail: str, status: int):
        self.title = title
        self.detail = detail
        self.status = status

    @staticmethod
    def bad_request(detail):
        return CustomAPIException(title='error.bad-request', detail=detail, status=400)


def register(api: NinjaAPI):
    @api.exception_handler(ValidationError)
    def validation_error(request, exc: ValidationError):
        error = ApiError(title='error.validation-error', detail=str(exc.errors), status=422)
        return api.create_response(
            request, error, status=error.status
        )

    @api.exception_handler(CustomAPIException)
    def custom_api_exception(request, exc: CustomAPIException):
        error = ApiError(title=exc.title, detail=exc.detail, status=exc.status)
        return api.create_response(
            request, error, status=error.status
        )

    @api.exception_handler(Http404)
    def not_found_error(request, exc: Http404):
        error = ApiError(title='error.not-found', detail=str(exc), status=404)
        return api.create_response(
            request, error, status=error.status
        )

    @api.exception_handler(Exception)
    def internal_server_error(request, exc: Exception):
        error = ApiError(title='error.unknown', detail=str(exc), status=500)
        return api.create_response(
                request, error, status=500
        )

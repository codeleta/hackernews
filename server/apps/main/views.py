from typing import Callable
from typing import Dict
from typing import TypeVar

from django import http

from server.apps.main.logic import post_forms
from server.apps.main.logic import posts

TypeFunc = Callable[[http.HttpRequest], http.JsonResponse]
TypeVarFunc = TypeVar('TypeVarFunc', bound=TypeFunc)


class JsonResponseBadRequest(http.JsonResponse):
    """Json response bad request.

    Return JsonResponse with status 400.
    body contains fields:
    - code: 'bad_request';
    - message: what`s happening;
    - details: dict with detail information.
    """

    def __init__(self, message: str, details: Dict[str, str], **kwargs):
        """Initialize JsonResponseBadRequest.

        Set status to 400, set response code to 'bad_request'.
        """
        status = 400
        response = {
            'message': message,
            'code': 'bad_request',
            'details': details,
        }
        super().__init__(response, status=status, **kwargs)


def allowed_method(method: str) -> Callable[[TypeVarFunc], TypeFunc]:
    """Decorator for validate request method.

    Allow only one method.
    :param method - request method like GET, POST, etc.
    """

    def factory(func: TypeVarFunc) -> TypeFunc:
        def decorator(request: http.HttpRequest) -> http.JsonResponse:
            if request.method != method:
                return JsonResponseBadRequest(
                    message=f'only {method} request',
                    details={},
                )
            return func(request)
        return decorator
    return factory


@allowed_method('GET')
def get_posts(request: http.HttpRequest) -> http.JsonResponse:
    """Get hackernews posts."""
    form = post_forms.PostsRequest(request.GET)
    if not form.is_valid():
        return JsonResponseBadRequest(
            message='invalid GET data',
            details=form.errors,
        )

    post_list = posts.get_posts(
        order=form.cleaned_data.get('order'),
        limit=form.cleaned_data.get('limit'),
        offset=form.cleaned_data.get('offset'),
    )

    response_posts = []
    for post in post_list:
        response_posts.append(post.to_dict())
    return http.JsonResponse({'posts': response_posts})

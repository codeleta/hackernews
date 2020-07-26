import typing_extensions

from django import forms

from server.apps.main.logic import posts

MAX_ORDER_LENGTH: typing_extensions.Final = 255


class PostsRequest(forms.Form):
    """Form for validate request posts."""

    limit = forms.IntegerField(required=False)
    offset = forms.IntegerField(required=False)
    order = forms.CharField(max_length=MAX_ORDER_LENGTH, required=False)

    def clean_order(self):
        """Validate order.

        Check the existence of the field.
        """
        order = self.cleaned_data['order']
        try:
            order = posts.clean_order(order)
        except posts.ValidationError as exc:
            raise forms.ValidationError(str(exc))
        return order

    def clean_limit(self):
        """Validate limit."""
        limit = self.cleaned_data['limit']
        try:
            limit = posts.clean_limit(limit)
        except posts.ValidationError as exc:
            raise forms.ValidationError(str(exc))
        return limit

    def clean_offset(self):
        """Validate offset."""
        offset = self.cleaned_data['offset']
        try:
            offset = posts.clean_offset(offset)
        except posts.ValidationError as exc:
            raise forms.ValidationError(str(exc))
        return offset

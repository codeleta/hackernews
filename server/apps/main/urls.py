from django import urls

from server.apps.main import views

app_name = 'main'

urlpatterns = [
    urls.path('posts', views.get_posts, name='get_posts'),
]

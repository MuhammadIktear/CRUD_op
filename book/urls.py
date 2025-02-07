from django.urls import path
from .views import CreateBook

urlpatterns = [
    path('', CreateBook.as_view()),
]
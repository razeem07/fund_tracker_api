from django.urls import path

from api import views

urlpatterns=[
     path('signup/',views.UserCreateView.as_view()),
     path('expenses/',views.ExpenseListCreateView.as_view()),
     path("expenses/<int:pk>/",views.ExpenseRetrieveUpdateDestroyView.as_view()),
]
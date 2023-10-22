from django.urls import path, include, re_path
from rest_framework import permissions

from backend.settings import BASE_URL_SWAGGER
from . import views

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from .schemas import BothHttpAndHttpsSchemaGenerator

schema_view = get_schema_view(
    openapi.Info(
        title="feedback employers API",
        default_version="v1",
        description="for greensight",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=BothHttpAndHttpsSchemaGenerator,
    url=BASE_URL_SWAGGER,
)

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("health_check/", views.health_check_view),
    path('list_slaves_of_head/<int:pk>/', views.SlavesListForItsHead.as_view()),
    path("ask_review/<int:pk>/", views.AskReview.as_view()),
    path("get_me/", views.GetMe.as_view()),
    path("list_need_to_review_users/", views.ListNeedToReviewUsers.as_view()),
    path("metric/list/", views.MetricListView.as_view()),
    path("review/<int:employee_id>/", views.ReviewListView.as_view())

]

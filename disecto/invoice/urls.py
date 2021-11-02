from django.urls import path
from invoice import views


urlpatterns = [
    path('AgentRegister/', views.AgentsRegister.as_view(), name = "AgentRegis"),
]
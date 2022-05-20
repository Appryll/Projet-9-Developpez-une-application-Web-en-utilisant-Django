"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# service des fichiers statiques en développement
from django.conf import settings
from django.conf.urls.static import static


from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView

import authentication.views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("", views.login, name='feed'),
    # path('signup/', views.signup, name='signup'),

    #conection
    path('', LoginView.as_view(template_name='authentication/login.html', redirect_authenticated_user=True), name='login'),

    #register
    path('signup/', authentication.views.signup_page, name='signup'),
   
    #deconection
    path('logout/', authentication.views.logout_user, name='logout'),

] 

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
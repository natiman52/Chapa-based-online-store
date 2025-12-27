"""
URL configuration for selltools project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path,include
from users.views import Signup,Verify,resend_OTP,passwordreset,passwordResetChange,FinsihSocialSignUp,account_logout
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .tools import ProductSitemap,CatagorySitemap,StaticViewSitemap,QuestionSitemap


urlpatterns = [
    path("",include('store.urls')),
    path("users/",include('users.urls')),
    path("manager/",include("manager.urls")),
    path('faq/', include('faq.urls')),
    path('admin/', admin.site.urls),
    path('accounts/signup/',Signup,name="account_signup"),
    path("accounts/verification/<int:id>",TemplateView.as_view(template_name="account/verification.html"),name="account_verification"),
    path('accounts/verify/<str:link>',Verify,name="accounts_verify"),
    path("accounts/resend-otp/<int:id>",resend_OTP,name="accounts_resend"),
    path("accounts/password-reset",passwordreset,name="accounts_reset"),
    path('accounts/password-change/<str:link>',passwordResetChange,name="accounts_change"),
    path("accounts/finis-account/",FinsihSocialSignUp,name="accounts_finish"),
    path("accounts/logout",account_logout,name="acc_logout"),
    path('accounts/', include('allauth.urls')),
    path("sitemap.xml",sitemap,{"sitemaps": {"products":ProductSitemap,"catagorys":CatagorySitemap,"staticpages":StaticViewSitemap,"questions":QuestionSitemap}},name="MySitemap",)
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
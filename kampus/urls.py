"""
URL configuration for kampus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from form import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as login
from django.contrib.auth import views as logout




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ListBukuTabungan.as_view(), name='home'),
    path('accounts/login/',login.LoginView.as_view(template_name='login.html'),name='login'),
    # path('accounts/login/', views.YourCustomLoginView.as_view(template_name='login.html'), name='login'),
    # path('accounts/logout/',logout.LogoutView.as_view(),name='logout',kwargs={'next_page':'/'}),
    path('accounts/logout/', logout.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
    path('mahasiswa/',views.CreateFormMahasiswa.as_view(),name='formmahasiswa'),
    path('mahasiswa/list/',views.ListMahasiswa.as_view(),name='listmahasiswa'),
    path('<int:pk>/edit/',views.UpdateFormMahasiswa.as_view(),name='editformmahasiswa'),
    path('<int:pk>/delete/',views.DeleteFormMahasiswa.as_view(),name='deletemahasiswa'),

    path('bukutabungan/',views.CreateFormBukuTabungan.as_view(),name="formbukutabungan"),
    path('bukutabungan/<int:pk>/edit/',views.UpdateFormBukuTabungan.as_view(),name="editbukutabungan"),
    path('bukutabungan/<int:pk>/delete/',views.DeleteBukuTabungan.as_view(),name="deletebukutabungan"),
    path('bukutabungan/list/',views.ListBukuTabungan.as_view(),name='listbukutabungan'),

    path('bukutabungan/<int:bukutabungan_pk>/buattransaksi/',views.buat_transaksi,name="formtransaksi"),
    path('transaksi/<int:bukutabungan_pk>/list/',views.list_transaksi,name='listtransaksi')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

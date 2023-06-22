"""
URL configuration for careproject project.

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
from careapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",index),
    path("abt",about),
    path('care_reg/',caretaker_registration),
    path('client_reg/',client_reg),
    path('edit_cms/',edit_cms),
    path('cms_dash/',cms_dash),
    path('cms_add_med/',cms_add_med),
    path('rec_request/',rec_request),
    path('approvecr/<int:id>',apprv_cr),
    path('reject/<int:id>',reject),
    path('rejectmsg/<int:id>',rejectmsg),
    path('sup/',support),
    path("vsup/",view_support),
    path("cms_view_activity/",cms_view_activity),
    path("cms_view_cr/<int:id>",cms_view_cr),
    path("cms_view_pt/<int:id>",cms_view_pt),
    path('care_dash/',care_dash),
    path('edit_care/',edit_care),
    path("care_view_patient/",care_view_patient),
    path("cr_view_appointment/",cr_view_appointment),
    path("appointment_complete/<int:id>",appointment_complete),
    path("appointment_delete/<int:id>",appointment_delete),
    path("activity_delete/<int:id>",activity_delete),
    path("activity_complete/<int:id>",activity_complete),
    path("cr_view_activity/",cr_view_activity),
    path("cr_view_med/",cr_view_med),
    path('cr_depart/<int:id>',cr_depart),
    path("ptdash/",ptdash),
    path("edit_pt/",edit_pt),
    path("pt_add_activity/",patient_add_activity),
    path("patient_add_appointment/",patient_add_appointment),
    path('patient_add_medicine/',patient_add_medicine),
    path("pt_view_activity/",pt_view_activity),
    path("remove_act/<int:id>",pt_remove_act),
    path("maps/",maps),
    path('lgin/',logins),
    path('lgout/',logouts),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

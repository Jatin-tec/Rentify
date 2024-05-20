from django.urls import path
from rent.views import post_property, dashboard, properties, edit_property, home, delete_property, inbox, property_detail
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home, name='home'),
    path('post/', post_property, name='post_property'),
    path('edit-post/<int:id>/', edit_property, name='edit_property'),
    path('delete-post/<int:id>/', delete_property, name='delete_property'),
    path('dashboard/', dashboard, name='dashboard'),
    path('inbox/', inbox, name='inbox'),
    path('properties/', properties, name='properties'),
    path('api/properties/<int:pk>/', property_detail, name='properties'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('check_booking/' , check_booking),
    path('', home , name='home'),
    path('hotel/', hotel , name='hotel'),
    path('room/', room , name='room'),
    path('hotel-detail/<uid>/' , hotel_detail , name="hotel_detail"),
    path('add-amenity/', add_amenity, name= 'add_amenity'),
    path('upload-hotel-image', upload_hotel_image, name='upload_hotel_image'),
    path('upload-room-image', upload_room_image, name='upload_room_image'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()
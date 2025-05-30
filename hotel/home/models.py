from django.contrib.auth.models import User
from django.db import models
import uuid

class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False , primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class Amenities(BaseModel):
    amenity_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.amenity_name

class Hotel(BaseModel):
    hotel_name= models.CharField(max_length=100)
    description = models.TextField()
    user = models.OneToOneField(User, related_name="user_hotel" , on_delete=models.SET_NULL, null=True, blank=True)
    mobile = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.hotel_name

class Room(BaseModel):
    room_name= models.CharField(max_length=100, null=True, blank=True)
    room_number= models.CharField(max_length=10, null=True, blank=True)
    room_price = models.IntegerField()
    description = models.CharField(null=True, blank=True)
    amenities = models.ManyToManyField(Amenities)
    hotel = models.ForeignKey(Hotel, related_name="hotel_room" , on_delete=models.CASCADE, null=True, blank=True)
    mobile = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.room_name


class HotelImages(BaseModel):
    hotel= models.ForeignKey(Hotel ,related_name="images", on_delete=models.CASCADE)
    images = models.ImageField(upload_to="hotels")
    
class RoomImages(BaseModel):
    room= models.ForeignKey(Room ,related_name="room_images", on_delete=models.CASCADE)
    images = models.ImageField(upload_to="hotels")


class HotelBooking(BaseModel):
    hotel= models.ForeignKey(Hotel  , related_name="hotel_bookings" , on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_bookings" , on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    booking_type= models.CharField(max_length=100,choices=(('Pre Paid' , 'Pre Paid') , ('Post Paid' , 'Post Paid')))

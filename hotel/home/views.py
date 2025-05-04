
from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .models import (Amenities, Hotel, HotelBooking, Room, HotelImages, RoomImages)
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from .models import Room, Hotel, Amenities


def check_booking(start_date, end_date ,uid , room_count):
    qs = HotelBooking.objects.filter(
        start_date__lte=start_date,
        end_date__gte=end_date,
        hotel__uid = uid
        )
    if len(qs) >= room_count:
        return False
    return True


def home(request, id=None):
    hotel_name = None
    if id is not None:
        hotels_objs = Hotel.objects.filter(pk = str(id))
    else:
        hotels_objs = [Hotel.objects.all().first()]
    print(id)
    print(hotels_objs)
    amenities_objs = Amenities.objects.all()
    
    rooms_objs = Room.objects.filter(hotel = hotels_objs[0])
    
    sort_by = request.GET.get('sort_by')
    search = request.GET.get('search')
    amenities = request.GET.getlist('amenities')
    print(amenities)
    # if sort_by:
    #     if sort_by == 'ASC': hotels_objs = hotels_objs.order_by('hotel_price')
    #     elif sort_by == 'DSC': hotels_objs = hotels_objs.order_by('-hotel_price')

    # if search: hotels_objs = hotels_objs.filter( Q(hotel_name__icontains = search) | Q(description__icontains = search) )
    # if len(amenities): hotels_objs = hotels_objs.filter(amenities__amenity_name__in = amenities).distinct()

    context = {'amenities_objs' : amenities_objs , 'hotels_objs' : hotels_objs , 'sort_by' : sort_by 
                , 'search' : search , 'amenities' : amenities, 'rooms_objs' : rooms_objs, }
    return render(request , 'home.html', context)


@login_required(login_url="/login")
def room(request):
    user = request.user
    hotel = Hotel.objects.filter(user=user).first()

    if not hotel:
        return render(request, 'rooms.html', {
            'error': 'You must create a hotel first before adding rooms.',
            'rooms': [],
            'hotels': [],
            'amenities': [],
        })

    # Fetch only rooms and amenities related to the user's hotel
    rooms = Room.objects.filter(hotel=hotel)
    amenities = Amenities.objects.all()

    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        room_name = request.POST.get('room_name')
        room_number = request.POST.get('room_number')
        room_price = request.POST.get('room_price')
        description = request.POST.get('description')
        mobile = request.POST.get('mobile')
        selected_amenities = request.POST.getlist('amenities')

        if room_id:
            room = get_object_or_404(Room, uid=room_id, hotel=hotel)
            room.room_name = room_name
            room.room_number = room_number
            room.room_price = room_price
            room.description = description
            room.mobile = mobile
            room.save()
            room.amenities.set(selected_amenities)
        else:
            room = Room.objects.create(
                room_name=room_name,
                room_number=room_number,
                room_price=room_price,
                description=description,
                mobile=mobile,
                hotel=hotel
            )
            room.amenities.set(selected_amenities)
        return redirect('room')

    return render(request, 'room.html', {
        'rooms': rooms,
        'hotels': [hotel],  # send only the user's hotel
        'amenities': amenities,
    })

def hotel_detail(request,uid):
    hotel_obj = Hotel.objects.get(uid = uid)

    if request.method == 'POST':
        checkin = request.POST.get('checkin')
        checkout= request.POST.get('checkout')
        hotel = Hotel.objects.get(uid = uid)
        if not check_booking(checkin ,checkout  , uid , hotel.room_count):
            messages.warning(request, 'Hotel is already booked in these dates ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        HotelBooking.objects.create(hotel=hotel , user = request.user , start_date=checkin
        , end_date = checkout , booking_type  = 'Pre Paid')
        
        messages.success(request, 'Your booking has been saved')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

        
    
    return render(request , 'hotel_detail.html' ,{
        'hotels_obj' :hotel_obj
    })

def add_amenity(request):
    return redirect('hotel')

@login_required(login_url="/login")
def hotel(request):
    user = request.user
    hotel = Hotel.objects.filter(user=user).first()

    if request.method == 'POST':
        hotel_name = request.POST.get('hotel_name')
        description = request.POST.get('description')
        mobile = request.POST.get('mobile')

        if hotel:
            # Update existing hotel
            hotel.hotel_name = hotel_name
            hotel.description = description
            hotel.mobile = mobile
            hotel.save()
        else:
            # Create new hotel
            Hotel.objects.create(hotel_name=hotel_name, description=description, mobile=mobile, user=user)

        return redirect('hotel')

    return render(request, 'hotel.html', {'hotel': hotel})


def upload_hotel_image(request):
    if request.method == 'POST':
        hotel_id = request.POST.get('hotel_id')
        image = request.FILES.get('image')
        if hotel_id and image:
            hotel = Hotel.objects.get(pk=hotel_id)
            HotelImages.objects.create(hotel=hotel, images=image)
    return redirect('hotel')

def upload_room_image(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        image = request.FILES.get('image')
        if room_id and image:
            room = Room.objects.get(pk=room_id)
            RoomImages.objects.create(room=room, images=image)
    return redirect('room')

def index(request):
    hotels = Hotel.objects.all()
    context = {
        'hotels' : hotels
    }
    return render(request, 'index.html', context)
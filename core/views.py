from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import datetime
from core.models import BufferTime,ConferenceRoom,Roombooking

def buffer_time_validation(start_time,end_time):
    if BufferTime.objects.filter(start_time=start_time,end_time=end_time).exists() or BufferTime.objects.filter(start_time__lt=start_time,end_time__gt=start_time).exists() or BufferTime.objects.filter(start_time__lt=end_time,end_time__gt=end_time).exists():
        return False
    return True
def update_vaccancy(start_time,end_time,person_qty):
    cr=ConferenceRoom.objects.filter(capacity__gte=person_qty).order_by("capacity")
    for i in cr:
        if Roombooking.objects.filter(room=i,start_time=start_time,end_time=end_time).exists() or Roombooking.objects.filter(room=i,start_time__lt=start_time,end_time__gt=start_time).exists() or Roombooking.objects.filter(room=i,start_time__lt=end_time,end_time__gt=end_time).exists():
            continue
        else:
            Roombooking.objects.create(room=i,start_time=start_time,end_time=end_time)
            return i.name
    return "NO_VACANT_ROOM"

def get_vaccant_room(start_time,end_time):
    cr_data=[]
    cr=ConferenceRoom.objects.all().order_by("capacity")
    for i in cr:
        if Roombooking.objects.filter(room=i,start_time__lte=start_time,end_time__gt=start_time).exists() or Roombooking.objects.filter(room=i,start_time__lte=end_time,end_time__gt=end_time).exists():
            continue
        else:
            cr_data.append(i.name)
    if not cr_data:
        return "NO_VACANT_ROOM"
    return " ".join(cr_data)


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def book_conference_room(request):

    input_data = request.GET
    input_string = input_data.get("input_data")
    print(input_string)
    if not input_string:
        return HttpResponse("INCORRECT_INPUT",status=400)
    input_string = input_string.strip()
    splited_list = input_string.split(' ')
    timeformat = "%H:%M"
    if splited_list[0] == "VACANCY":
        # SHOW VACCANCY LOGIC 
        if len(splited_list) != 3:
            return HttpResponse("INCORRECT_INPUT",status=400)
        start_time = splited_list[1]
        try:
            vld_start_time  = datetime.datetime.strptime(start_time, timeformat)
        except ValueError:
            return HttpResponse("INCORRECT_INPUT",status=400)
        if int(start_time.split(":")[1])%15 != 0:
            return HttpResponse("INCORRECT_INPUT",status=400)
        end_time = splited_list[2]
        try:
            vld_end_time  = datetime.datetime.strptime(end_time, timeformat)
        except ValueError:
            return HttpResponse("INCORRECT_INPUT",status=400)
        if int(end_time.split(":")[1])%15 != 0:
            return HttpResponse("INCORRECT_INPUT",status=400)
        if vld_start_time > vld_end_time:
            return HttpResponse("INCORRECT_INPUT",status=400)
        
        if buffer_time_validation(vld_start_time,vld_end_time) == False:
            return HttpResponse("NO_VACANT_ROOM",status=400)
        return HttpResponse(get_vaccant_room(vld_start_time,vld_end_time))
    elif splited_list[0] == "BOOK":
        # BOOKING LOGIC
        if len(splited_list) != 4:
            return HttpResponse("INCORRECT_INPUT",status=400)
        start_time = splited_list[1]
        end_time = splited_list[2]
        person_qty = splited_list[3]
        start_time = splited_list[1]
        try:
            vld_start_time  = datetime.datetime.strptime(start_time, timeformat)
        except ValueError:
            return HttpResponse("INCORRECT_INPUT",status=400)
        if not person_qty.isdigit():
            return HttpResponse("INCORRECT_INPUT",status=400)
        person_qty = int(person_qty)
        if person_qty < 0 :
            return HttpResponse("INCORRECT_INPUT",status=400)
        if int(start_time.split(":")[1])%15 != 0:
            return HttpResponse("INCORRECT_INPUT",status=400)
        
        try:
            vld_end_time  = datetime.datetime.strptime(end_time, timeformat)
        except ValueError:
            return HttpResponse("INCORRECT_INPUT",status=400)
        if int(end_time.split(":")[1])%15 != 0:
            return HttpResponse("INCORRECT_INPUT",status=400)
        
        if vld_start_time > vld_end_time:
            return HttpResponse("INCORRECT_INPUT",status=400)

        if buffer_time_validation(vld_start_time,vld_end_time) == False:
            return HttpResponse("NO_VACANT_ROOM",status=400)
        return HttpResponse(update_vaccancy(vld_start_time,vld_end_time,person_qty))
    else:
        return HttpResponse("INCORRECT_INPUT",status=400)
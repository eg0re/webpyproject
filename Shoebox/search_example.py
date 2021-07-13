from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models import F

from Shoebox.models import Shoebox

print("Hallo")
box = None

try:
    box = Shoebox.objects.get(id=1)
    box.description = "basic box from amazon"
    #box.description = F("description")
    #box.price = F("price") - 1
    box.save()
except ObjectDoesNotExist:
    print("Shoebox not found")
    box = None

boxes = Shoebox.objects.filter(Q(name__contains="big") & ~Q(name__contains="nike"))
if(len(boxes) > 0):
    for box in boxes:
        print(box.name)
else:
    print("Set empty.")

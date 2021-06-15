from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Shoebox(models.Model):
    name: models.CharField(max_length=100)
    description: models.CharField(max_length=1000)
    price: models.DecimalField()
    #Hinweis: Für ein Form, bei welchem man die Dateien hochladen kann wird 'enctype="multipart/form-data"' benötigt
    #Für das Anzeigen des Bildes in einer Template class.field.url benutzen! (siehe VL7 Folie 11)
    #@Georg: Du musst Pillow installieren! Wird in der 7.Vorlesung gezeigt (bei 38:58)
    image: models.ImageField(upload_to='shoebox_images/', blank=True, null=True)
    pdf: models.FileField(upload_to='shoebox_pdfs/', blank=True, null=True)

    def __str__(self):
        return "Name: " + self.name + " Price: " + self.price + " Description: " + self.description

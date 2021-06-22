from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Shoebox(models.Model):
    # Wie "dick" die Wellpappe ist
    FLUTE_TYPE = [
        ('A', 'Grobwelle'),
        ('B', 'Feinwelle'),
        ('C', 'Mittelwelle'),
        ('E', 'Mikrowelle'),
        ('F', 'Miniwelle'),
    ]

    # Wieviele Ebenen in der Pappe vorhanden sind
    FLUTE_LAYERS = [
        ('0.5', 'Einseitig beklebte Wellpappe'),
        ('1', 'Einwellige Wellpappe'),
        ('2', 'Zweiwellige Wellpappe'),
        ('3', 'Dreiwellige Wellpappe'),
    ]

    # Deckenpapiere
    LINER_TYPE = [
        ('A', 'Kraftliner'),
        ('B', 'Testliner'),
        ('C', 'Schrenzpapier'),
        ('U', 'Unbekannt'),
    ]

    name = models.CharField(max_length=100, default='box-name')
    description = models.CharField(max_length=1000, default="no description")
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False, default=10)
    flute_type = models.CharField(max_length=1,
                                  choices=FLUTE_TYPE,
                                  default='B'
                                  )
    flute_layers = models.CharField(max_length=3,
                                    choices=FLUTE_LAYERS,
                                    default='1')
    liner_type = models.CharField(max_length=1,
                                  choices=LINER_TYPE,
                                  default='B')
    # Dimensionen in Millimeter angeben
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    length = models.IntegerField(default=0)
    brand = models.CharField(max_length=100, default="shoebox")

    # Hinweis: Für ein Form, bei welchem man die Dateien hochladen kann wird 'enctype="multipart/form-data"' benötigt
    # Für das Anzeigen des Bildes in einer Template class.field.url benutzen! (siehe VL7 Folie 11)
    image = models.ImageField(upload_to='shoebox_images/', blank=True, null=True)
    pdf = models.FileField(upload_to='shoebox_pdfs/', blank=True, null=True)

    class Meta:
        ordering = ['name', 'brand']
        verbose_name = 'Shoebox'
        verbose_name_plural = 'Shoeboxes'

    def __str__(self):
        return "Name: " + self.name + " Price: " + str(self.price) + " Brand " + self.brand + " Description: "\
               + self.description + " Flute Type: " + self.flute_type + " Flute Layers: " + self.flute_layers\
               + " Liner Type: " + self.liner_type + " Dimensions: Width: " + str(self.width) + " Height: "\
               + str(self.height) + " Length: " + str(self.length)

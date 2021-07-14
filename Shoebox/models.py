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

    def get_comments(self):
        return Comment.objects.filter(shoebox_id=self.id)

    def get_comments_count(self):
        return len(self.get_comments())

    def get_box_rating(self):
        ratings = Comment.objects.filter(shoebox_id=self.id)
        overallrate = 0
        divisor = 0
        for rating in ratings:
            overallrate += rating.rating
            divisor += 1
        if len(ratings) is 0:
            return 0
        overallrate /= divisor
        return overallrate

    def __str__(self):
        return "Name: " + self.name + " Price: " + str(self.price) + " Brand " + self.brand + " Description: " \
               + self.description + " Flute Type: " + self.flute_type + " Flute Layers: " + self.flute_layers \
               + " Liner Type: " + self.liner_type + " Dimensions: Width: " + str(self.width) + " Height: " \
               + str(self.height) + " Length: " + str(self.length)


class Comment(models.Model):
    RATINGS = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]

    text = models.TextField(max_length=500)
    rating = models.IntegerField(choices=RATINGS,
                                 default='5')
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shoebox = models.ForeignKey(Shoebox, on_delete=models.CASCADE)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def get_comment_prefix(self):
        if len(self.text) > 50:
            return self.text[:50] + '...'
        else:
            return self.text

    def get_upvotes(self):
        upvotes = Vote.objects.filter(up_or_down='U', comment_id=self.id)
        return upvotes

    def get_upvotes_count(self):
        return len(self.get_upvotes())

    def get_downvotes(self):
        downvotes = Vote.objects.filter(up_or_down='D', comment_id=self.id)
        return downvotes

    def get_downvotes_count(self):
        return len(self.get_downvotes())

    def vote(self, user, up_or_down):
        u_or_d = 'U'
        if up_or_down == 'down':
            u_or_d = 'D'

        Vote.objects.create(up_or_down=u_or_d,
                            user=user,
                            comment_id=self.id,
                            shoebox_id=int(self.shoebox_id)
                            )

    def __str__(self):
        return self.get_comment_prefix() + ' (' + self.user.username + ')'

    def __repr__(self):
        return self.get_comment_prefix() + ' (' + self.user.username + '/' + str(self.timestamp) + ')' + \
               'shoeboxid = ' + str(self.shoebox_id)


class Vote(models.Model):
    VOTE_TYPES = [
        ('U', 'up'),
        ('D', 'down'),
    ]

    up_or_down = models.CharField(max_length=1,
                                  choices=VOTE_TYPES,
                                  )
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    shoebox = models.ForeignKey(Shoebox, on_delete=models.CASCADE)

    def __str__(self):
        return self.up_or_down + ' on ' + self.comment.name + ' by ' + self.user.username

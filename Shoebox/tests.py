from djanconf defined in webpyproject.urls, Django tried these URL patterns, in this order:

    admin/
    ^media/(?P<path>.*)$

The empty path didn’t match any of these.

You’re seeing this error because you have DEBUG = True in your Django settings file. Change that to False, and Django will display a standard 404 page.
go.test import TestCase

# Create your tests here.

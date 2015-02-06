from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.core.files.storage import Storage
from django.core.files import File
from django.db import connection, transaction
from django.http.response import HttpResponse, Http404
from django.conf import settings
from django.utils.deconstruct import deconstructible

import base64, StringIO, urlparse, mimetypes

from models import DbFile

@deconstructible
class ModelStorage(Storage):
    def __init__(self):
        self.base_url = getattr(settings, 'MODELSTORAGE_BASEURL', '/dbfiles/')

    def _open(self, name, mode='rb'):
        assert mode == 'rb', "Open mode should be 'rb'"

        try:
            f = DbFile.objects.get(filename=name)
        except DbFile.DoesNotExist:
            return None

        memFile = StringIO.StringIO(base64.b64decode(f.data))
        memFile.name = name
        memFile.mode = mode

        return File(memFile)

    def _save(self, name, content):
        name = name.replace('\\', '/')
        binary = content.read()

        size = len(binary)
        encoded = base64.b64encode(binary)

        f, created = DbFile.objects.get_or_create(filename=name, 
                                                  defaults={'data': encoded, 
                                                            'size': size})
        f.save()

        return name

    def exists(self, name):
        return DbFile.objects.filter(filename=name).exists()

    def delete(self, name):
        try:
            DbFile.objects.get(filename=name).delete()
        except:
            pass

    def url(self, name):
        return urlparse.urljoin(self.base_url, name).replace('\\', '/')

    def size(self, name):
        try:
            DbFile.objects.get(filename=name).size
        except:
            raise
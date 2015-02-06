from django.http.response import HttpResponse, Http404
import mimetypes

from .storage import ModelStorage

def dbfile_view(request, filename):
    print filename
    # Read file from database
    storage = ModelStorage()
    ff = storage.open(filename, 'rb')
    if not ff:
        raise Http404
    file_content = ff.read()

    # Prepare response
    content_type, content_encoding = mimetypes.guess_type(filename)
    response = HttpResponse(content=file_content, content_type=content_type)
    response['Content-Disposition'] = 'inline; filename=%s' % filename
    if content_encoding:
        response['Content-Encoding'] = content_encoding
    return response
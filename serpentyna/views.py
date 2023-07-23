from django.conf import settings
from django.views.static import serve

def serve_static(request, path):
    return serve(request, path, document_root=settings.STATICFILES_DIRS[0])
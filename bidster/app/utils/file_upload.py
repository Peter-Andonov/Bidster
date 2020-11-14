from os.path import join
from uuid import uuid4

from django.conf import settings

from app.models import Image

def save_to_galery(galery, file):
    file_ext = file.name.split('.')[-1]
    unique_fn = f'{uuid4()}.{file_ext}'
    full_path = join(settings.MEDIA_ROOT, unique_fn)
    rel_path = join(settings.MEDIA_DIR_NAME, unique_fn)
    with open(full_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

        image = Image(galery_id=galery, image=rel_path)
        image.save()
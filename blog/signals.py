from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PostImage


@receiver(post_save, sender=PostImage)
def generate_thumbnail(sender, instance, **kwargs):
    try:
        if not instance.image:
            return
        if instance.thumbnail:
            return
        img = Image.open(instance.image.path)
        img.thumbnail((320, 240))
        thumb_io = BytesIO()
        img_format = 'JPEG'
        if img.mode in ('RGBA', 'LA'):
            img = img.convert('RGB')
        img.save(thumb_io, format=img_format, quality=70)
        thumb_name = instance.image.name.rsplit('/', 1)[-1]
        instance.thumbnail.save(f"thumb_{thumb_name}", ContentFile(thumb_io.getvalue()), save=False)
        instance.save()
    except Exception:
        # don't block on thumbnail errors
        pass

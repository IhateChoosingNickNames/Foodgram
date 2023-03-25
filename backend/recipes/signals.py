from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from recipes.models import Recipe
from recipes.utils import media_folder_cleaner


@receiver(post_delete, sender=Recipe)
def post_delete_image(sender, instance, *args, **kwargs):
    """Сигнал на удаление картинки."""

    try:
        instance.image.delete(save=False)
        media_folder_cleaner()
    except:
        pass


@receiver(pre_save, sender=Recipe)
def pre_save_image(sender, instance, *args, **kwargs):
    """Сигнал на удаление старой картинки при обновлении картинки."""

    try:
        old_img = instance.__class__.objects.get(id=instance.id).image.path
        try:
            new_img = instance.image.path
        except:
            new_img = None
        if new_img != old_img:
            import os

            if os.path.exists(old_img):
                os.remove(old_img)
                media_folder_cleaner()
    except:
        pass


post_delete.connect(post_delete_image, sender=Recipe)
pre_save.connect(pre_save_image, sender=Recipe)

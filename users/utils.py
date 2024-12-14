import os

from django.utils.text import slugify


def get_avatar_upload_path(instance, filename):
    # Генерация слага из имени и фамилии пользователя
    user_slug = slugify(f'{instance.user.first_name} {instance.user.last_name}')
    # Формируем путь к файлу (путь будет выглядеть как 'photos/имя-фамилия/filename')
    return os.path.join('photos', user_slug, filename)
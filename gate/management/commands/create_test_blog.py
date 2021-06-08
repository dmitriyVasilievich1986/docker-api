from django.core.management.base import BaseCommand
from comments.models import Comments
from catalog.models import Catalog
from blog.models import Blog
from user.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User(username="user")
        user.save()
        catalog_main = Catalog(name="/", title="Главная")
        catalog_main.save()
        catalog1 = Catalog(name="cat1", title="каталог 1", parent=catalog_main)
        catalog1.save()
        text = """<h3>1. Заголовок</h3>
        <p>Параграф.</p>
        """
        blog1 = Blog(name="blog1", title="Блог 1", text=text, catalog=catalog1)
        blog1.save()
        blog2 = Blog(name="blog2", title="Блог 2", text=text, catalog=catalog1)
        blog2.save()
        comment1 = Comments(text="Простой комментарий", owner=blog1)
        comment1.save()
        comment2 = Comments(text="Простой ответ", parent=comment1, user=user)
        comment2.save()
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book


class Command(BaseCommand):
    help = 'Create default groups (Editors, Viewers, Admins) and assign book permissions'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Book)

        perms = {}
        for codename in ('can_view', 'can_create', 'can_edit', 'can_delete'):
            try:
                perms[codename] = Permission.objects.get(codename=codename, content_type=content_type)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Permission {codename} not found for Book. Run migrations first.'))
                return

        viewers, _ = Group.objects.get_or_create(name='Viewers')
        viewers.permissions.set([perms['can_view']])

        editors, _ = Group.objects.get_or_create(name='Editors')
        editors.permissions.set([perms['can_view'], perms['can_create'], perms['can_edit']])

        admins, _ = Group.objects.get_or_create(name='Admins')
        admins.permissions.set(Permission.objects.filter(content_type=content_type))

        self.stdout.write(self.style.SUCCESS('Groups created/updated: Viewers, Editors, Admins'))

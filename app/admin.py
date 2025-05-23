from django.contrib import admin
from .models import Project
from django.http import HttpResponse
from django.utils.html import format_html
from django.urls import path
import io, os
from django.conf import settings


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['full_name']
    list_display = ['full_name', 'age', 'project', 'download_file']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'download-file/<int:project_id>/',
                self.admin_site.admin_view(self.download_file_view),
                name='download-project-file',
            ),
        ]
        return custom_urls + urls

    def download_file(self, obj):
        return format_html(
            '<a class="button" href="{}">Yuklab olish</a>',
            f'./download-file/{obj.id}/'
        )
    download_file.short_description = 'Project'
    download_file.allow_tags = True


    def download_file_view(self, request, project_id):
        project = Project.objects.get(pk=project_id)

        file_path = os.path.join(settings.MEDIA_ROOT, project.project.name)

        if not os.path.exists(file_path):
            return HttpResponse("Fayl topilmadi", status=404)

        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response

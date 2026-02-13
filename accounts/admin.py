from django.contrib import admin
from .models import CustomUser
from django.utils.html import format_html
from jobs.models import Job,Application

admin.site.site_header = "job portal Admin panel "
admin.site.site_title = "Job portal Admin "
admin.site.index_title = " welcome to job portal Dashboard "

class AdminCSS(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('admin/custom_admin.css',)
        }


# Register your models here.

@admin.register(CustomUser)
class customerUserAdmin(admin.ModelAdmin):
    list_display = ("profile_image_tag","email","full_name","roles","phone","is_active","is_active","is_staff")
    list_filter = ('roles','is_active')
    search_fields = ('email', 'full_name')


    def profile_image_tag(self,obj):
        if obj.profile_image:
            return format_html(
                '<img src={} width="40" style="border-redius:50%;"/>',
                obj.profile_image.url 
            )
        return "No Image Available"                
                    

# itizamritamishra@gmail.com = "hirenexus@123"   student
# ankit@gmail.com = "django2025"    recruiter
# from django.contrib import admin
# from .models import User,Post
# # Register your models here.

# # class userAdmin(admin.ModelAdmin):
#     # list_display = ['cid', 'email', 'mobile', 'is_active']
#     # list_filter = ['is_active']
#     # list_editable = ['mobile', 'is_active']
#     # search_fields = ['mobile', 'email']
#     class userAdmin(admin.ModelAdmin):
#         list_display = ('name', 'enrollment')  

#     list_per_page = 50
# admin.site.register(User, userAdmin)
# admin.site.register(Post)

from django.contrib import admin
from .models import User, Post

class userAdmin(admin.ModelAdmin):
    list_display = ('name', 'enrollment')  # ✅ existing fields from your model
    list_per_page = 50  # ✅ now it's inside the class

admin.site.register(User, userAdmin)
admin.site.register(Post)

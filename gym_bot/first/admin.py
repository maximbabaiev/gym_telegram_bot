from django.contrib import admin
from first.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Trainer)
admin.site.register(Schedule_trainer)
admin.site.register(Product)
admin.site.register(User_product)
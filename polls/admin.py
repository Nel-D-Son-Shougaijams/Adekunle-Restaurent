from django.contrib import admin
from django.utils.html import format_html
from .models import *

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','status_indicator','current')
    list_editable = ('current',)
    def status_indicator(self,obj):
        if obj.current == "notdishpatched":
            return format_html('<span style="color:green;font-weight:bold;">❌</span>')
        elif obj.current == "outfordel":
            return format_html('<span style="color:green;font-weight:bold;">🚚</span>')
        elif obj.current == "deleivered":
            return format_html('<span style="color:green;font-weight:bold;">✔️</span>')
        elif obj.current == "cancelled":
            return format_html('<span style="color:green;font-weight:bold;">👎</span>')
    list_filter = ("current",)

class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name','status')
    list_editable = ("status",)
    list_filter = ("status",)
# Register your models here.
admin.site.register(FoodItem,FoodItemAdmin)
admin.site.register(Cart)
admin.site.register(Article)
admin.site.register(Review)
admin.site.register(Order,OrderAdmin)
admin.site.register(Worker)
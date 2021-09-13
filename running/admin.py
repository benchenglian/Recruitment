from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Country, Province, Area, City


class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields] # 将所有字段返回，列表显示

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many] # 外建的关系都加到列表中

    def has_add_permission(self, request):
        return False # 是否有添加数据权限

    def has_delete_permission(self, request, obj=None):
        return False # 是否有删除数据权限

    def has_change_permission(self, request, obj=None):
        return False # 是否有修改数据权限


@admin.register(Country)
class CountryAdmin(ReadOnlyAdmin):
    search_fields = ('chn_name', 'eng_name',)

@admin.register(Province)
class ProvinceAdmin(ReadOnlyAdmin):
    search_fields = ('chn_name', 'eng_name',)
    
#admin.register(City)
class CityAdmin(ReadOnlyAdmin):
    #list_display = ('cityid', 'countryid', 'areaid', 'provinceid', 'chn_name', 'eng_name')
    autocomplete_fields = ['provinceid','countryid',] #自动检索，从Countryadmin和ProviceAdmin来，所以两个类也要定义Search fields。

admin.site.register(City,CityAdmin)
admin.site.register(Area) 
from django.contrib import admin
import adapter.models as azt_models
# Register your models here.


class VcmdSchemaBaseAdmin(admin.ModelAdmin):

    list_display = ('id', 'updated', 'temperature', )
    search_fields = ('id', 'temperature', )
    readonly_fields = ('id', )
    ordering = ()
    filter_horizontal = ()
    autocomplete_fields = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(azt_models.VcmdSchemaBase, VcmdSchemaBaseAdmin)


class SystemDataAdmin(admin.ModelAdmin):

    list_display = ('id', 'unisat_data', 'is_expired', 'date_of_update', 'date_of_add')
    search_fields = ('id', 'is_expired',)
    readonly_fields = ('id', 'date_of_update', 'date_of_add', )
    ordering = ('-date_of_update',)
    filter_horizontal = ()
    autocomplete_fields = ()
    list_filter = ('is_expired', )
    fieldsets = ()


admin.site.register(azt_models.SystemData, SystemDataAdmin)


class BmeDataBaseAdmin(admin.ModelAdmin):

    list_display = ('id', 'temperature', 'pressure', 'humidity', 'updated', )
    search_fields = ('id', )
    readonly_fields = ('id',)
    ordering = ()
    filter_horizontal = ()
    autocomplete_fields = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(azt_models.BmeDataBase, BmeDataBaseAdmin)


class BmeDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'unisat_data', 'is_expired', 'date_of_update', 'date_of_add')
    search_fields = ('id', 'is_expired',)
    readonly_fields = ('id', 'date_of_update', 'date_of_add',)
    ordering = ('-date_of_update',)
    filter_horizontal = ()
    autocomplete_fields = ()
    list_filter = ('is_expired',)
    fieldsets = ()


admin.site.register(azt_models.BmeData, BmeDataAdmin)


class BnoDataBaseAdmin(admin.ModelAdmin):

    list_display = ('id', 'unisat_id', 'updated', )
    search_fields = ('id', 'unisat_id',)
    readonly_fields = ('id',)
    ordering = ()
    filter_horizontal = ()
    autocomplete_fields = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(azt_models.BnoDataBase, BnoDataBaseAdmin)


class BnoDataAdmin(admin.ModelAdmin):

    list_display = ('id', 'unisat_data', 'date_of_update', 'date_of_add')
    search_fields = ('id', 'unisat_data',)
    readonly_fields = ('id',)
    ordering = ()
    filter_horizontal = ()
    autocomplete_fields = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(azt_models.BnoData, BnoDataAdmin)


class SiDataBaseAdmin(admin.ModelAdmin):

    list_display = ('id', 'unisat_id', 'updated', 'vis')
    search_fields = ('id', 'unisat_id',)
    readonly_fields = ('id',)
    ordering = ()
    filter_horizontal = ()
    autocomplete_fields = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(azt_models.SiDataBase, SiDataBaseAdmin)


class SiDataAdmin(admin.ModelAdmin):

    list_display = ('id', 'unisat_data', 'is_expired',)
    search_fields = ('id',)
    readonly_fields = ('id',)
    ordering = ()
    filter_horizontal = ()
    autocomplete_fields = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(azt_models.SiData, SiDataAdmin)


class CameraDataBaseAdmin(admin.ModelAdmin):

    list_display = ('id', 'cam_num', 'path', 'updated', )
    search_fields = ('id', )
    readonly_fields = ('id',)
    ordering = ()
    filter_horizontal = ()
    autocomplete_fields = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(azt_models.CameraDataBase, CameraDataBaseAdmin)


class CameraDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'unisat_data', 'get_cam_num', 'is_expired', 'date_of_update', 'date_of_add')
    search_fields = ('id', 'is_expired',)
    readonly_fields = ('id', 'date_of_update', 'date_of_add',)
    ordering = ('-date_of_update',)
    filter_horizontal = ()
    autocomplete_fields = ()
    list_filter = ('is_expired',)
    fieldsets = ()

    def get_cam_num(self, obj):
        return obj.unisat_data.cam_num


admin.site.register(azt_models.CameraData, CameraDataAdmin)

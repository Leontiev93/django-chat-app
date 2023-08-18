from django.contrib import admin

from .models import Contract, User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'password',
        'first_name',
        'last_name',
#        '_following'
    )
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    empty_value_display = '-пусто-'
    exclude = (
        'date_joined',
        'last_login',
    )

    # def _following(self, obj):
    #     return ', '.join(
    #         [following.username for following in obj.following.all()])


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'customer',
        'contractor',
    )
    search_fields = (
        'customer',
    )
    empty_value_display = '-пусто-'

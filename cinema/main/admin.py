from datetime import date

from django.contrib import admin

from .models import PaymentCard, Profile, Movie, Promotion, ShowTime, ShowRoom

class PromotionPermissions(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        # print(f'has_change_permission_request: {request}') #simply test code
        if obj is None:
            return True
        elif obj.send == True:
            return False
        else:
            return True

    def has_add_permission(self, request):
        return True

    # This method makes sure you don't delete a sent promotion until after the promotion expires.
    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        elif obj.send == True and date.today() < obj.end_date:
            return False
        else:
            return True

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # print(f'save_model_permission_request: {request}') #test code.
        # Have it send an email right about here.
        if not self.has_change_permission(request, obj):
            subscribers = Profile.objects.filter(promotions=True)
            if subscribers is not None:
                for account in subscribers:
                    print(f'account: {account}')
            # print(f'email: {account.user.email}') #Test Lines

class ShowTimeInline(admin.TabularInline):
    model = ShowTime
    ordering = ('date','time',)
class ShowRoomPermission(admin.ModelAdmin):
    inlines = [ShowTimeInline,]
    list_display = ('room_number','number_seats','showtimes')
    def showtimes(self, obj=None):
        def __str__(self):
            if True:
                return 'a simple string here'
            #return list(ShowTime.objects.order_by('date','time').filter(show_room=obj))
        if obj is None:
            return
        else:
            ordered_display = ShowTime.objects.order_by('date', 'time').filter(show_room=obj)
            ordered_output = ''
            for x in ordered_display:
                ordered_output += str(x)
            print(ordered_output)
            return ordered_output
# Register your models here.
admin.site.register(Profile)
admin.site.register(PaymentCard)
admin.site.register(Movie)
admin.site.register(ShowRoom, ShowRoomPermission)
admin.site.register(Promotion, PromotionPermissions)
#
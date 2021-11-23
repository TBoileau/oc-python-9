from django.contrib import admin
from .models.ticket import Ticket
from .models.review import Review
from .models.user_follows import UserFollows


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user', 'image', 'time_created')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'rating', 'user', 'headline', 'body', 'time_created')

class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user')

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFollows, UserFollowsAdmin)
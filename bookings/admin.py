from django.contrib import admin

from .models import Booking, Ticket


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    inlines = (TicketInline,)
    list_display = (
        "api_id",
        "maas_operator",
        "ticketing_system",
        "status",
        "created_at",
        "updated_at",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(ticketing_system__users=request.user)

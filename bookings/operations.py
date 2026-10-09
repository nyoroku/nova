from datetime import timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Sum, Avg, F, ExpressionWrapper, DurationField
from django.shortcuts import render
from django.utils import timezone
from .models import BookingLead


@staff_member_required
def operations_overview(request):
    if not request.user.has_perm('bookings.view_bookinglead'):
        raise PermissionDenied
    leads = BookingLead.objects.filter(created_at__gte=timezone.now() - timedelta(days=30))
    response_time = leads.filter(contacted_at__isnull=False).aggregate(
        mean=Avg(ExpressionWrapper(F('contacted_at') - F('created_at'), output_field=DurationField())))['mean']
    context = {'title':'Nova activity outcomes — last 30 days', 'total':leads.count(),
        'response_hours':round(response_time.total_seconds()/3600, 1) if response_time else None,
        'outcomes':leads.values('status').annotate(count=Count('id')).order_by('status'),
        'activities':leads.values('tour__name', 'utm_campaign', 'utm_content').annotate(count=Count('id')).order_by('-count'),
        'revenues':leads.filter(status__in=['CONFIRMED','COMPLETED'], actual_revenue__isnull=False).values('currency').annotate(total=Sum('actual_revenue'))}
    response = render(request, 'bookings/operations.html', context)
    response['Cache-Control'] = 'no-store'
    return response

"""One quote path for product pages, enquiries and channel exports."""
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from django.db.models import Q
from django.utils import timezone


def valid_on(queryset, day):
    if queryset.model._meta.model_name == 'externalfee':
        for name in ('adult_amount', 'child_amount', 'student_amount'):
            queryset = queryset.filter(Q(**{name + '__isnull': True}) | Q(**{name + '__gte': 0}))
    return queryset.filter(is_active=True).filter(Q(effective_from__isnull=True) | Q(effective_from__lte=day)).filter(
        Q(effective_until__isnull=True) | Q(effective_until__gte=day))


@dataclass
class Quote:
    currency: str
    rate: object = None
    option: object = None
    boat_amount: Decimal | None = None
    hotel_amount: Decimal = Decimal('0')
    external_amount: Decimal = Decimal('0')
    lines: list = field(default_factory=list)
    reasons: list = field(default_factory=list)
    total: Decimal | None = None

    @property
    def complete(self):
        return self.total is not None and not self.reasons

    def snapshot(self):
        return {'currency': self.currency, 'rate_id': self.rate.pk if self.rate else None,
                'option_id': self.option.pk if self.option else None,
                'option_name': self.option.name if self.option else '',
                'duration_minutes': self.option.duration_minutes if self.option else None,
                'pricing_model': self.rate.pricing_model if self.rate else '',
                'unit_amount': str(self.rate.amount) if self.rate else None,
                'lines': self.lines, 'total': str(self.total) if self.complete else None,
                'reasons': self.reasons, 'confirmation': 'Availability and final price require staff confirmation.'}


def quote_activity(tour, *, adults=1, children=0, visitor_type='RESIDENT', currency='KES',
                   service_date=None, option_id=None, private=False, hotel=None):
    result = Quote(currency=currency)
    day = service_date or timezone.localdate()
    if isinstance(day, str):
        day = date.fromisoformat(day)
    if adults < 1 or children < 0 or adults + children > 500:
        result.reasons.append('Please provide a valid party size.')
        return result
    audience = {'CITIZEN': 'KENYAN_CITIZEN', 'RESIDENT': 'KENYA_RESIDENT', 'NON_RESIDENT': 'NON_RESIDENT'}.get(visitor_type)
    if audience is None or currency not in ('KES', 'USD'):
        result.reasons.append('Please choose a visitor category and currency.')
        return result
    options = tour.options.filter(is_active=True)
    if option_id:
        options = options.filter(pk=option_id)
    elif private:
        options = options.filter(mode__in=['PRIVATE', 'GROUP'])
    if options.count() != 1:
        result.reasons.append('Choose a booking option so its duration, capacity and price are clear.')
        return result
    result.option = option = options.first()
    party = adults + children
    if party < option.min_guests or party > option.max_guests:
        result.reasons.append(f'This option is for {option.min_guests}–{option.max_guests} guests. Ask us about another arrangement.')
        return result
    rates = valid_on(tour.rates.filter(option=option, is_public=True, currency=currency), day)
    exact = list(rates.filter(audience_type=audience))
    candidates = exact or list(rates.filter(audience_type='ALL'))
    if not candidates and option.mode == 'GROUP':
        candidates = list(rates.filter(audience_type='GROUP'))
    if len(candidates) != 1:
        result.reasons.append('A unique current rate is unavailable for this option and date. Please request a quote.')
        return result
    result.rate = rate = candidates[0]
    if rate.amount < 0 or (rate.child_amount is not None and rate.child_amount < 0):
        result.reasons.append('This option is awaiting a pricing check. Please request a quote.')
        return result
    if rate.pricing_model in ('FROM_PRICE', 'CUSTOM_QUOTE'):
        result.reasons.append('This option needs an individual quote.')
        return result
    if (rate.duration_minutes != option.duration_minutes or rate.min_guests != option.min_guests
            or rate.max_guests != option.max_guests):
        result.reasons.append('This option is awaiting a pricing check. Please request a quote.')
        return result
    if rate.pricing_model == 'PER_PERSON':
        if children and rate.child_amount is None:
            result.reasons.append('Child seat pricing requires confirmation. Please request a family quote.')
            return result
        result.boat_amount = rate.amount * adults + (rate.child_amount or Decimal('0')) * children
    elif rate.pricing_model in ('PER_BOAT', 'PER_GROUP'):
        result.boat_amount = rate.amount
    else:
        result.reasons.append('Please request a quote for this pricing option.')
        return result
    result.lines.append({'label': option.name, 'amount': str(result.boat_amount), 'currency': currency, 'pay_to': 'Nova'})

    if option.external_fees.exists():
        fees = list(valid_on(option.external_fees.filter(visitor_type__in=[visitor_type, 'ALL']), day))
        # Distinct providers/services may each contribute one mandatory charge.
        grouped = {}
        for fee in fees:
            grouped.setdefault((fee.provider_name, fee.service_name), []).append(fee)
        expected = set(option.external_fees.values_list('provider_name', 'service_name'))
        if set(grouped) != expected:
            result.reasons.append('Mandatory attraction fees need confirmation for your category and date.')
        for _, values in grouped.items():
            selected = [f for f in values if f.visitor_type == visitor_type] or values
            if len(selected) != 1:
                result.reasons.append('The attraction fee schedule needs confirmation.')
                continue
            fee = selected[0]
            if not fee.last_verified_at:
                result.reasons.append('The mandatory attraction fee needs a verification date.')
            if children:
                result.reasons.append('Confirm children’s ages and attraction admission eligibility with Nova.')
            if fee.currency != currency or fee.adult_amount is None or (children and fee.child_amount is None):
                result.reasons.append('Attraction fees require a separate currency or child-age quote; no currency conversion is assumed.')
                continue
            amount = fee.adult_amount * adults + (fee.child_amount or Decimal('0')) * children
            result.external_amount += amount
            result.lines.append({'label': f'{fee.provider_name} — {fee.service_name}', 'amount': str(amount),
                                 'currency': currency, 'pay_to': 'Attraction provider', 'verified_at': str(fee.last_verified_at)})
    if hotel:
        from partners.models import HotelAccess
        access = HotelAccess.objects.filter(property=hotel, is_published=True,
            access_status__in=['VERIFIED_ACTIVE', 'VERIFIED_ON_REQUEST']).exclude(
            access_mode__in=['UNAVAILABLE', 'SUBJECT_TO_CONFIRMATION']).first()
        if (not access or not access.is_operationally_verified
                or access.currency != currency or access.access_mode == 'ROAD_TRANSFER'):
            result.reasons.append('Hotel departure or road transfer costs require confirmation.')
        else:
            # Existing positioning fees apply per boat. Multi-boat allocation is quoted by staff.
            if option.mode == 'GROUP':
                result.reasons.append('Hotel positioning for multiple boats requires a group quote.')
            else:
                result.hotel_amount = access.positioning_fee
                result.lines.append({'label': 'Hotel boat positioning (subject to permission)', 'amount': str(result.hotel_amount),
                                     'currency': currency, 'pay_to': 'Nova'})
    if not result.reasons:
        result.total = result.boat_amount + result.hotel_amount + result.external_amount
    return result

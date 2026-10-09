from datetime import timedelta
from decimal import Decimal
from bs4 import BeautifulSoup
from django.test import TestCase
from django.utils import timezone
from tours.models import Tour, TourOption, ExperienceRate
from .models import BookingLead


class BookingFlowTests(TestCase):
    def setUp(self):
        self.tour=Tour.objects.create(name='Booking test ride',slug='booking-test-ride',status='PUBLISHED',legacy_publication=True)
        self.option=TourOption.objects.create(tour=self.tour,name='Private hour',mode='PRIVATE',duration_minutes=60,max_guests=7)
        ExperienceRate.objects.create(experience=self.tour,option=self.option,name='Private KES',amount=4500,
            min_guests=1,max_guests=7,duration_minutes=60,effective_from=timezone.localdate())
        response=self.client.get('/book/?tour='+self.tour.slug)
        self.token=BeautifulSoup(response.content,'html.parser').find('input',attrs={'name':'submission_token'})['value']
        self.data={'submission_token':self.token,'lead_type':'BOAT_ONLY','tour':self.tour.pk,'option':self.option.pk,
            'preferred_date':str(timezone.localdate()+timedelta(days=2)),'preferred_time':'Morning',
            'adults':3,'children':0,'guest_name':'Test Guest','guest_phone':'+254700000000',
            'transport_required':'NONE','currency':'KES','visitor_type':'RESIDENT','consent_operational':True}

    def test_post_quotes_once_and_requires_staff_confirmation(self):
        response=self.client.post('/book/',self.data,HTTP_HX_REQUEST='true')
        self.assertContains(response,'Almost on the Water')
        lead=BookingLead.objects.get(submission_key=self.token)
        self.assertEqual(lead.quoted_total_amount,Decimal('4500'))
        self.assertEqual(lead.status,'NEW')
        self.assertTrue(lead.quote_complete)
        self.assertIn('booking_enquiry_submit',response['HX-Trigger'])
        second=self.client.post('/book/',self.data,HTTP_HX_REQUEST='true')
        self.assertEqual(BookingLead.objects.filter(submission_key=self.token).count(),1)
        self.assertNotIn('HX-Trigger',second)

    def test_snapshot_survives_price_and_product_changes(self):
        self.client.post('/book/',self.data)
        lead=BookingLead.objects.get(submission_key=self.token)
        self.tour.name='Changed title';self.tour.save()
        self.tour.rates.update(amount=9900)
        lead.refresh_from_db()
        self.assertEqual(lead.quote_snapshot['unit_amount'],'4500.00')
        self.assertIn('Booking test ride',lead.generate_whatsapp_message())
        self.assertIn('Preferred time: Morning',lead.generate_whatsapp_message())

    def test_attribution_survives_internal_navigation(self):
        self.client.get('/boat-rides/?utm_source=google&utm_medium=organic&utm_campaign=gbp_activities&utm_content='+self.tour.slug)
        self.client.get('/prices/')
        self.client.post('/book/',self.data)
        lead=BookingLead.objects.get(submission_key=self.token)
        self.assertEqual(lead.utm_campaign,'gbp_activities')
        self.assertEqual(lead.utm_content,self.tour.slug)

    def test_invalid_option_past_date_or_missing_consent_creates_no_lead(self):
        other=Tour.objects.create(name='Other',slug='other-ride',status='PUBLISHED')
        wrong=TourOption.objects.create(tour=other,name='Other option',duration_minutes=60,mode='PRIVATE')
        for updates in [{'option':wrong.pk},{'preferred_date':str(timezone.localdate()-timedelta(days=1))},{'consent_operational':False}]:
            response=self.client.post('/book/',{**self.data,**updates},HTTP_HX_REQUEST='true')
            self.assertEqual(response.status_code,200)
            self.assertNotContains(response,'<html')
            self.assertFalse(BookingLead.objects.filter(submission_key=self.token).exists())

    def test_partial_quotes_do_not_show_a_fabricated_total(self):
        self.tour.rates.update(is_active=False)
        response=self.client.post('/book/',self.data)
        self.assertContains(response,'Total price awaiting confirmation')
        lead=BookingLead.objects.get(submission_key=self.token)
        self.assertFalse(lead.quote_complete)
        self.assertIsNone(lead.quote_snapshot['total'])
        self.assertIn('awaiting confirmation',lead.generate_whatsapp_message())

    def test_operations_overview_requires_permission(self):
        self.assertEqual(self.client.get('/book/operations/').status_code,302)

    def test_quote_context_prefills_the_enquiry(self):
        response=self.client.get(f'/book/?tour={self.tour.slug}&option={self.option.pk}&adults=4&children=1&preferred_date=2026-12-11&currency=USD&visitor_type=NON_RESIDENT')
        form=response.context['form']
        self.assertEqual(form['adults'].value(),4)
        self.assertEqual(form['children'].value(),1)
        self.assertEqual(form['option'].value(),self.option.pk)
        self.assertEqual(form['currency'].value(),'USD')

    def test_option_switching_only_exposes_the_selected_published_tour(self):
        response=self.client.get(f'/book/options/?tour={self.tour.pk}')
        self.assertContains(response,'Private hour')
        self.assertNotContains(response,'Sunrise')
        self.tour.status='DRAFT';self.tour.save()
        self.assertNotContains(self.client.get(f'/book/options/?tour={self.tour.pk}'),'Private hour')

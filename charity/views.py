from django.db.models import Sum
from django.shortcuts import render
from django.views import View

from charity.models import Institution, Donation


# Create your views here.
class LandingPage(View):
    def get(self, request):
        total_bags = Donation.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
        supported_institutions = Institution.objects.count()

        context = {
            'total_bags': total_bags,
            'supported_institutions': supported_institutions,
        }
        foundations = Institution.objects.filter(type=Institution.FOUNDATION)
        ngos = Institution.objects.filter(type=Institution.NGO)
        local_collections = Institution.objects.filter(type=Institution.LOCAL_COLLECTION)

        context = {
            'foundations': foundations,
            'ngos': ngos,
            'local_collections': local_collections,
        }

        return render(request, 'index.html', context)


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

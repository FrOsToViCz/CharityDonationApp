from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views import View

from charity.models import Institution, Donation


# Create your views here.
class LandingPage(View):
    def get(self, request):
        total_bags = Donation.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
        supported_institutions = Institution.objects.count()

        foundations_list = Institution.objects.filter(type=Institution.FOUNDATION).order_by('name')
        ngos_list = Institution.objects.filter(type=Institution.NGO).order_by('name')
        local_collections_list = Institution.objects.filter(type=Institution.LOCAL_COLLECTION).order_by('name')

        page_number_foundations = request.GET.get('page_foundations', 1)
        page_number_ngos = request.GET.get('page_ngos', 1)
        page_number_local_collections = request.GET.get('page_local_collections', 1)

        paginator_foundations = Paginator(foundations_list, 2)
        paginator_ngos = Paginator(ngos_list, 2)
        paginator_local_collections = Paginator(local_collections_list, 2)

        foundations = paginator_foundations.get_page(page_number_foundations)
        ngos = paginator_ngos.get_page(page_number_ngos)
        local_collections = paginator_local_collections.get_page(page_number_local_collections)

        context = {
            'total_bags': total_bags,
            'supported_institutions': supported_institutions,
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

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('register')

        user = User.objects.create_user(user=email, email=email, password=password)
        user.first_name = name
        user.last_name = surname
        user.save()

        return redirect('login')

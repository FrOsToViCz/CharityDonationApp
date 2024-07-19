from django.contrib import messages
from django.contrib.auth import login, authenticate
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

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('landing-page')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=email).exists():
                messages.error(request, 'Email is already taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=email, password=password, first_name=name, last_name=surname,
                                                email=email)
                user.save()
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

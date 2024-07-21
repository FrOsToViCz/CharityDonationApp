import json
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View
from charity.models import Institution, Donation, Category


# Create your views here.
class LandingPage(View):
    def get(self, request):
        total_bags = Donation.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
        supported_institutions = Donation.objects.values('institution').distinct().count()

        foundations_list = Institution.objects.filter(type=Institution.FOUNDATION).order_by('name')
        ngos_list = Institution.objects.filter(type=Institution.NGO).order_by('name')
        local_collections_list = Institution.objects.filter(type=Institution.LOCAL_COLLECTION).order_by('name')

        page_number_foundations = request.GET.get('page_foundations')
        page_number_ngos = request.GET.get('page_ngos')
        page_number_local_collections = request.GET.get('page_local_collections')

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


class AddDonation(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        categories = Category.objects.all()
        organizations = Institution.objects.all()
        for organization in organizations:
            category_ids = list(organization.categories.values_list('id', flat=True))
            organization.category_ids_json = json.dumps(category_ids)
        context = {
            'categories': categories,
            'organizations': organizations,
        }
        return render(request, 'form.html', context)

    def post(self, request):
        bags = request.POST.get('bags')
        categories_ids = request.POST.getlist('categories')
        organization_id = request.POST.get('organization')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        more_info = request.POST.get('more_info')

        if not (
                bags and categories_ids and organization_id and address and city and postcode and phone and date and time):
            return HttpResponseBadRequest("Missing required data")

        try:
            organization = Institution.objects.get(pk=organization_id)
        except Institution.DoesNotExist:
            return HttpResponseBadRequest("Invalid organization id")

        try:
            donation = Donation.objects.create(
                quantity=bags,
                institution=organization,
                address=address,
                phone_number=phone,
                city=city,
                zip_code=postcode,
                pick_up_date=date,
                pick_up_time=time,
                pick_up_comment=more_info,
                user=request.user
            )
            donation.categories.add(*categories_ids)

            return redirect('form-confirmation')

        except Exception as e:
            return render(request, 'form.html', {'error_message': str(e)})


class FormConfirmation(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


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

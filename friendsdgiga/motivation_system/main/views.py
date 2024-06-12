from django.contrib.auth import logout
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .models import Service, Review, Order
from .forms import ReviewForm, UserRegisterForm
from django.core.mail import send_mail
from django.conf import settings

def user_logout(request):
    logout(request)
    return redirect('home')

class CustomLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'

def home(request):
    reviews = Review.objects.all().order_by('-created_at')[:5]
    return render(request, 'main/home.html', {'reviews': reviews})

def services(request):
    services_list = Service.objects.all()

    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '')

    if search_query:
        services_list = services_list.filter(name__icontains=search_query)

    if sort_by == 'price_asc':
        services_list = services_list.order_by('price')
    elif sort_by == 'price_desc':
        services_list = services_list.order_by('-price')

    return render(request, 'main/services.html', {'services': services_list})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})

@login_required
def order_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Создание заказа
        order = Order.objects.create(user=request.user, service=service, address=address)
        
        # Отправка email
        subject = 'Ваш заказ принят'
        message = f'Уважаемый(ая) {request.user.username},\n\n' \
                  f'Ваш заказ на услугу {service.name} принят.\n\n' \
                  f'Адрес: {address}\n' \
                  f'Телефон: {phone}\n\n' \
                  f'Мы свяжемся с вами в ближайшее время для уточнения деталей.\n\n' \
                  f'С уважением,\nКоманда нашей компании'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        # Сообщение об успешном заказе
        return render(request, 'main/order_success.html')

    
    return render(request, 'main/order_service.html', {'service': service})

def admin_services(request):
    services_list = Service.objects.all()
    return render(request, 'main/admin_services.html', {'services': services_list})

@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('home')
    else:
        form = ReviewForm()
    return render(request, 'main/add_review.html', {'form': form})

def about(request):
    return render(request, 'main/about.html')

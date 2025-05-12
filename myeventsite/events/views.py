from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
import csv
from datetime import datetime
from .models import Event, Subscription
from .forms import UserRegistrationForm, UserLoginForm, EventSubscriptionForm

def home(request):
    featured_events = Event.objects.filter(is_featured=True)[:3]
    return render(request, 'events/home.html', {'featured_events': featured_events})

def events(request):
    search_query = request.GET.get('search', '')
    if search_query:
        events_list = Event.objects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    else:
        events_list = Event.objects.all()
    
    return render(request, 'events/events.html', {'events': events_list, 'search_query': search_query})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    subscribed = False
    if request.user.is_authenticated:
        subscribed = Subscription.objects.filter(user=request.user, event=event).exists()
    
    if request.method == 'POST' and request.user.is_authenticated:
        if 'subscribe' in request.POST:
            if not subscribed:
                Subscription.objects.create(user=request.user, event=event)
                messages.success(request, f'You have successfully subscribed to {event.title}')
            return redirect('event_detail', event_id=event.id)
        elif 'unsubscribe' in request.POST:
            if subscribed:
                Subscription.objects.filter(user=request.user, event=event).delete()
                messages.success(request, f'You have unsubscribed from {event.title}')
            return redirect('event_detail', event_id=event.id)
    
    return render(request, 'events/event_detail.html', {
        'event': event,
        'subscribed': subscribed
    })

def handler404(request, exception):
    return render(request, 'events/404.html', status=404)

def export_events_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="events-{datetime.now().strftime("%Y-%m-%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Title', 'Description', 'Date', 'Location', 'Featured'])
    
    events = Event.objects.all()
    for event in events:
        writer.writerow([
            event.title,
            event.description,
            event.date.strftime('%Y-%m-%d %H:%M'),
            event.location,
            'Yes' if event.is_featured else 'No'
        ])
    
    return response


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            is_admin = form.cleaned_data.get('is_admin')
            if is_admin:
                user.is_staff = True
                user.is_superuser = True
            user.save()
            login(request, user)
            if is_admin:
                messages.success(request, 'Admin registration successful!')
            else:
                messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'events/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = UserLoginForm()
    return render(request, 'events/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('home')


@login_required
def my_subscriptions(request):
    subscriptions = Subscription.objects.filter(user=request.user)
    return render(request, 'events/my_subscriptions.html', {'subscriptions': subscriptions})


# Check if the user is an admin
def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    events = Event.objects.all().order_by('-created_at')
    total_events = events.count()
    featured_events = events.filter(is_featured=True).count()
    upcoming_events = events.filter(date__gt=datetime.now()).count()
    
    context = {
        'events': events,
        'total_events': total_events,
        'featured_events': featured_events,
        'upcoming_events': upcoming_events
    }
    
    return render(request, 'events/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_event_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        location = request.POST.get('location')
        image = request.POST.get('image')
        is_featured = 'is_featured' in request.POST
        
        Event.objects.create(
            title=title,
            description=description,
            date=date,
            location=location,
            image=image,
            is_featured=is_featured
        )
        messages.success(request, 'Event created successfully')
        return redirect('admin_dashboard')
    
    return render(request, 'events/admin/event_form.html')


@login_required
@user_passes_test(is_admin)
def admin_event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.description = request.POST.get('description')
        event.date = request.POST.get('date')
        event.location = request.POST.get('location')
        event.image = request.POST.get('image')
        event.is_featured = 'is_featured' in request.POST
        event.save()
        
        messages.success(request, 'Event updated successfully')
        return redirect('admin_dashboard')
    
    return render(request, 'events/admin/event_form.html', {'event': event})


@login_required
@user_passes_test(is_admin)
def admin_event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully')
        return redirect('admin_dashboard')
    
    return render(request, 'events/admin/event_confirm_delete.html', {'event': event})


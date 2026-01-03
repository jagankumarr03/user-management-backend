from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Profile
from .serializers import UserSerializer
import re

from rest_framework.permissions import IsAdminUser
from django.core.paginator import Paginator



@login_required
def dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/dashboard.html', {'profile': profile})


def signup(request):
    error = None

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(EMAIL_REGEX, email):
            error = "Invalid email"
        elif User.objects.filter(email=email).exists():
            error = "Email already exists"
        elif User.objects.filter(username=username).exists():
            error = "Username already exists"
        else:
            try:
                validate_password(password)
            except ValidationError as e:
                error = e.messages[0]
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                Profile.objects.create(user=user)
                return redirect('login')

    return render(request, 'accounts/signup.html', {'error': error})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')

        return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    error = None

    if request.method == "POST":
        phone = request.POST.get('phone')

        if not phone.isdigit() or len(phone) != 10:
            error = "Phone must be 10 digits"
        else:
            profile.phone = phone
            profile.save()
            return redirect('dashboard')

    return render(request, 'accounts/edit_profile.html', {'profile': profile, 'error': error})


@login_required
def admin_dashboard(request):
    if request.user.profile.role != 'admin':
        return redirect('dashboard')
    return render(request, 'accounts/admin_dashboard.html')



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_api(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
def api_signup(request):
    data = request.data

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return Response({"error": "All fields are required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already exists"}, status=400)

    try:
        validate_password(password)
    except ValidationError as e:
        return Response({"error": e.messages}, status=400)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    #check Profile auto-created by signal OR create here
    Profile.objects.get_or_create(user=user)

    return Response(
        {"message": "User created successfully"},
        status=201
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile_api(request):
    user = request.user
    data = request.data

    if 'email' in data:
        if User.objects.exclude(id=user.id).filter(email=data['email']).exists():
            return Response({"error": "Email already in use"}, status=400)
        user.email = data['email']

    if 'username' in data:
        if User.objects.exclude(id=user.id).filter(username=data['username']).exists():
            return Response({"error": "Username already in use"}, status=400)
        user.username = data['username']

    user.save()

    profile = user.profile
    if 'phone' in data:
        profile.phone = data['phone']
    profile.save()

    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_api(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not user.check_password(old_password):
        return Response({"error": "Old password incorrect"}, status=400)

    try:
        validate_password(new_password, user)
    except ValidationError as e:
        return Response({"error": e.messages}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({"message": "Password updated successfully"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_users_api(request):
    if request.user.profile.role != 'admin':
        return Response({"error": "Unauthorized"}, status=403)

    page = int(request.GET.get('page', 1))
    users = User.objects.all().order_by('id')

    paginator = Paginator(users, 10)
    page_obj = paginator.get_page(page)

    data = []
    for user in page_obj:
        data.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.profile.role,
            "is_active": user.is_active
        })

    return Response({
        "users": data,
        "total_pages": paginator.num_pages,
        "current_page": page
    })

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def toggle_user_status_api(request, user_id):
    if request.user.profile.role != 'admin':
        return Response({"error": "Unauthorized"}, status=403)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    user.is_active = not user.is_active
    user.save()

    return Response({
        "message": "User status updated",
        "is_active": user.is_active
    })

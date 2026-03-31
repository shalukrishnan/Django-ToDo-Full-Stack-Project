


from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User




# ---------------- API PART ----------------
class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists"}, status=400)

    user = User.objects.create_user(username=username, password=password)
    return Response({"message": "User created successfully"})


# ---------------- HTML + HTMX PART ----------------
@login_required
def home(request):
    todos = Todo.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "index.html", {"todos": todos})


@login_required
@require_http_methods(["POST"])
def add_todo(request):
    title = request.POST.get("title")
    priority = request.POST.get("priority", "medium")

    if not title:
        return HttpResponse("Title is required", status=400)

    todo = Todo.objects.create(
        user=request.user,
        title=title,
        priority=priority
    )

    return render(request, "partials/todo_item.html", {"todo": todo})

@login_required
@require_http_methods(["POST"])
def delete_todo(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)
    todo.delete()
    return HttpResponse("")



@login_required
@require_http_methods(["POST"])
def toggle_todo(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)
    todo.is_completed = not todo.is_completed
    todo.save()
    return render(request, "partials/todo_item.html", {"todo": todo})



@login_required
@require_http_methods(["GET"])
def edit_todo(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)
    return render(request, "partials/edit_todo_form.html", {"todo": todo})


@login_required
@require_http_methods(["POST"])
def update_todo(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)
    title = request.POST.get("title")

    if not title:
        return HttpResponse("Title is required", status=400)

    todo.title = title
    todo.save()

    return render(request, "partials/todo_item.html", {"todo": todo})


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not username or not password or not confirm_password:
            messages.error(request, "All fields are required")
            return render(request, "register.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "register.html")

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, "register.html")


@login_required
@require_http_methods(["GET"])
def cancel_edit(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)
    return render(request, "partials/todo_item.html", {"todo": todo})    


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')    
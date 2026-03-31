
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import TodoViewSet, home, add_todo, delete_todo

# router = DefaultRouter()
# router.register(r'todos', TodoViewSet)

# urlpatterns = [
    
#     path('', home),
#     path('add-todo/', add_todo),
#     path('delete-todo/<int:id>/', delete_todo),

   
#     path('api/', include(router.urls)),
# ]



from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import TodoViewSet, home, add_todo, delete_todo, toggle_todo
from .views import (
    TodoViewSet,
    home,
    add_todo,
    delete_todo,
    toggle_todo,
    edit_todo,
    update_todo,
    cancel_edit,
    login_view,
    logout_view,
    register_page,
)

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_page, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('add-todo/', add_todo, name='add_todo'),
    path('delete-todo/<int:id>/', delete_todo, name='delete_todo'),
    path('toggle-todo/<int:id>/', toggle_todo, name='toggle_todo'),
    path('edit-todo/<int:id>/', edit_todo, name='edit_todo'),
    path('update-todo/<int:id>/', update_todo, name='update_todo'),
    path('cancel-edit/<int:id>/', cancel_edit, name='cancel_edit'),

    path('api/', include(router.urls)),
]
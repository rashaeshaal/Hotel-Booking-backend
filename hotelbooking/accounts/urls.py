from django.urls import path
from django.conf import settings
from .views import RegisterView, LoginView,UpdateHotelPostView,PostCreateView,HotelPostListView,DeleteHotelPostView,HotelPostDetailView
from django.conf.urls.static import static


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('handlelogin/', LoginView.as_view(), name='handlelogin'),
    path('posts/', PostCreateView.as_view(), name='create_post'),
    path('hotelposts/<int:pk>/', HotelPostDetailView.as_view(), name='hotelpost-detail'),
    path('postsviews/', HotelPostListView.as_view(), name='postsviews'),
    path('postsviews/<int:id>/update/', UpdateHotelPostView.as_view(), name='post-update'),  
    path('postsviews/<int:id>/delete/', DeleteHotelPostView.as_view(), name='post-delete'), 
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
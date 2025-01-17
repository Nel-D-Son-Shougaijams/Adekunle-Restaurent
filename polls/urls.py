from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "polls"

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('about/', views.about, name='about'),
    path('addtocart/',views.addtocart, name="addtocart"),
    path("carts/",views.cart,name="cart"),
    path("delcart/<str:name>",views.deletecart,name="delcart"),
    path("addcart/",views.createcart,name="createcart"),
    path("blogs",views.blogs,name="blogs"),
    path("blogdelete/",views.delarticle,name="blogdel"),
    path("fooditem/<str:name>",views.food_detail,name="food_detail"),
    path("shopping/",views.shop,name="shopping"),
    path("login/",views.loginV,name="login"),
    path("signup/",views.signupV,name="signup"),
    path("logout/",views.logoutV,name="logout"),
    path("addreview/",views.addrev,name="addrev"),
    path("contact/",views.contact,name="about"),
    path("faq/",views.faq,name="faq"),
    path("our-team/",views.teams,name="teams"),
    path("our-history/",views.history,name="history"),
    path("deletecartitem/",views.deleteitems,name="remove"),
    path("order/<str:cn>",views.order,name="order"),
    path("confirm/<int:pk>",views.checkoutconfirm,name="confirm"),
    path("cancel/<int:pk>",views.checkoutcancel,name="cancel"),
    path("orders",views.orders,name="orders"),
    path("buy",views.buysessioncart,name="buy"),
    path("cancel/notloggedin",views.orders,name="cn"),
    path("confirmed",views.buyssessioncart,name="orde"),
    path("deleteitemsession/",views.deletesessionitem,name="deleteitemsession"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib.auth.views import LoginView, PasswordResetView
from django.shortcuts import get_object_or_404, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from users.forms import UserRegisterForm, UserProfileForm, UserLoginForm, UserRecoveryForm
from users.models import User, Payments
import random
import string

from users.serializers import UserSerializer, PaymentsSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserLoginView(LoginView):
    model = User
    form_class = UserLoginForm
    success_url = reverse_lazy('catalog:home')


class UserPasswordResetView(PasswordResetView):
    form_class = UserRecoveryForm
    template_name = 'users/recovery_form.html'


class PaymentsViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_lesson', 'paid_course', 'pay_transfer',)
    ordering_fields = ['pay_date',]


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_lesson', 'paid_course', 'pay_method')
    ordering_fields = ('-date_payment',)


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product_id = create_stripe_product(payment)
        price_id = create_stripe_price(product_id, payment)
        session_id, session_url = create_stripe_session(price_id)
        payment.session_id = session_id
        payment.link = session_url
        payment.save()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRegisterView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


class UserUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

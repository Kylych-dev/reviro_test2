from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Обрабатывает токены сброса пароля
    При создании токена необходимо отправить электронное письмо пользователю
    :param sender: Класс представления, который отправил сигнал
    :param instance: Экземпляр представления, который отправил сигнал
    :param reset_password_token: Объект модели токена
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/password_reset_email.html', context)
    email_plaintext_message = render_to_string('email/password_reset_email.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Your Website Title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@yourdomain.com",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()











'''
вот полный код 
модель 
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('administrator', 'Administrator'),
        ('partner', 'Partner'),
        ('regularuser', 'RegularUser'),
    )
    email = models.EmailField(unique=True, max_length=60, verbose_name="Email")
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)


    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = ("user")
        verbose_name_plural = ("users")


    def __str__(self):
        return self.email


class RegularUser(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        primary_key=True
        )
    name = models.CharField(max_length=100, verbose_name="Name")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    subscription = models.BooleanField(default=False, verbose_name="Subscription")
    avatar = models.ImageField(upload_to='avatars', blank=True, verbose_name="Avatar")

    class Meta:
        verbose_name = "RegularUser"
        verbose_name_plural = "RegularUsers"    

    def __str__(self):
        return self.name


class Partner(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        primary_key=True
        )
    establishment_name = models.CharField(max_length=100, verbose_name="Establishment Name")
    location = models.CharField(max_length=100, verbose_name="Location")
    description = models.TextField(verbose_name="Description")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    avatar = models.ImageField(upload_to='avatars', blank=True, verbose_name="Avatar")


    class Meta:
        verbose_name = "Partner"
        verbose_name_plural = "Partners"

    def __str__(self):
        return self.establishment_name

сигнал

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Обрабатывает токены сброса пароля
    При создании токена необходимо отправить электронное письмо пользователю
    :param sender: Класс представления, который отправил сигнал
    :param instance: Экземпляр представления, который отправил сигнал
    :param reset_password_token: Объект модели токена
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/password_reset_email.html', context)
    email_plaintext_message = render_to_string('email/password_reset_email.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Your Website Title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@yourdomain.com",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()

сериализатор 

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

представление 

class ChangePasswordAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="Изменить пароль",
        operation_summary="Смена пароля пользователя",
        operation_id="change_password",
        tags=["Authentication"],
        responses={
            200: openapi.Response(description="OK - Пароль успешно изменен"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
        },
    )
    def post(self, request):
        if request.method == 'POST':

            email = request.data.get('email')
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response(
                    {'error': 'Пользователь с таким email не найден.'}, 
                    status=status.HTTP_404_NOT_FOUND
                    )




            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                user = request.user
                if user.check_password(serializer.data.get('old_password')):
                    user.set_password(serializer.data.get('new_password'))
                    user.save()
                    update_session_auth_hash(request, user)  # Обновляем сессию после изменения пароля
                    return Response(
                        {'message': 'Password changed successfully.'}, 
                        status=status.HTTP_200_OK
                        )
                return Response(
                    {'error': 'Incorrect old password.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                    )
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
                )

                

file password_reset_mail.html
<!DOCTYPE html>
<html>
<head>
    <title>Password Reset Email</title>
</head>
<body>
    <p>Hello {{username}},</p>
    <p>We've received a request to reset your password. Please click on the link below to reset your password:</p>
    <p><a href="{{ reset_password_url }}">Reset Password</a></p>
    <p>If you did not request this password reset, you can safely ignore this email.</p>
    <p>Best regards,</p>
    <p>Your Application Team</p>
</body>
</html>

file password_reset_email.txt
Hello {{username}}, We've received a request to reset your password. Please click on the link below to reset your password: {{ reset_password_url }}


как только в постмене отправляю запрос то пароль сразу меняется на почту письмо не приходит




'''
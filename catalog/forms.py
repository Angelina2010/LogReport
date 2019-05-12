from django import forms
from django.contrib.auth.models import User
from .models import Category, Product


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        user_name = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=user_name).exists():
            raise forms.ValidationError('Пользователь не зарегистрирован')
        user = User.objects.get(username=user_name)
        if user and not user.check_password(password):
            raise forms.ValidationError('Неверный пароль')


class RegistrationForm(forms.ModelForm):
    full_name = forms.CharField()
    post = forms.CharField(max_length=100)
    sign = forms.ImageField(required=False)
    is_provider = forms.BooleanField(required=False)
    password_check = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    okpo = forms.IntegerField()
    phone = forms.IntegerField()
    address = forms.CharField()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'post',
            'full_name',
            'okpo',
            'phone',
            'email',
            'address',
            'is_provider',
            'username',
            'password',
            'password_check',
            'sign'
        ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['password_check'].label = 'Повторите пароль'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['post'].label = 'Ваша должность'
        self.fields['full_name'].label = 'Компания'
        self.fields['full_name'].help_text = 'Введите название на РУССКОМ языке!'
        self.fields['is_provider'].label = 'Компания-поставщик'
        self.fields['okpo'].label = 'Код ОКПО'
        self.fields['phone'].label = 'Телефон'
        self.fields['email'].label = 'Почта'
        self.fields['address'].label = 'Адрес'
        self.fields['sign'].label = 'Подпись'
        self.fields['sign'].help_text = 'Подпись необходима для верификации документов, данные защищены. '

    def clean(self):
        user_name = self.cleaned_data['username']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        if password != password_check:
            raise forms.ValidationError('Ваши пароли не совпадают, попробуйте снова')

        if User.objects.filter(username=user_name).exists():
            raise forms.ValidationError('Пользователь с данным логином уже зарегистрирован в системе!')


class OrderForm(forms.Form):
    name = forms.CharField()
    phone = forms.CharField()
    comments = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
        self.fields['phone'].label = 'Контактный номер'
        self.fields['comments'].label = 'Комментарии к заказу'


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория',
                                      widget=forms.widgets.Select(attrs={'size': 2}))
    image = forms.ImageField(label='Изображение')
    price = forms.DecimalField(label='Цена', max_digits=10, decimal_places=2)
    title = forms.CharField(label='Наименование', max_length=200, help_text='Введите русское название продукта')
    description = forms.CharField(label='Описание', max_length=300, required=False)

    class Meta:
        model = Product
        fields = [
            'title',
            'category',
            'description',
            'price',
            'image'
        ]


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        self.fields['password'].label = 'Введите пароль:'

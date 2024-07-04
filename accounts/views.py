from django.shortcuts import render,redirect
from .forms import RegisterForm,DepositeForm,ProfileUpdateForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView,UpdateView
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView
from django.contrib.auth import login,logout
from .models import UserAccountModel,User
from books.models import BorrowBookModel
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
# Create your views here.

# class UserProfile(LoginRequiredMixin, TemplateView):
#     template_name = 'accounts/profile.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user_account = self.request.user.account
#         context['balance'] = user_account.balance
#         context['balance_after_transaction'] = user_account.balance_after_transaction
#         return context
# def profile(request):
#     try:
#         user_account = request.user.account  # Assuming OneToOneField is used correctly
#     except User.account.RelatedObjectDoesNotExist:
#          user_account = UserAccountModel.objects.create(user=request.user, balance=0.00, balance_after_transaction=0, amount=0)
    
#     return render(request, 'accounts/profile.html', {'user_account': user_account})

def sending_user_mail(user,subject,template,amount):
    to_mail = user.email
    message = render_to_string(template,{
        'user': user,
        'amount':amount,
    })
    sent_mail = EmailMultiAlternatives(subject,to=[to_mail])
    sent_mail.attach_alternative(message,'text/html')
    sent_mail.send()

@login_required
def profile(request):
    user = request.user

    # jodi user account exists kore,nh thakle create hobe
    try:
        user_account = request.user.account
    except ObjectDoesNotExist:
        user_account = UserAccountModel.objects.create(
            user=request.user,
            balance=0.00,
            balance_after_transaction=0,
            amount=0
        )

    # current user er borrow kora books gula pamu..
    borrowed_books = BorrowBookModel.objects.filter(user=user)

    context = {
        'user_account': user_account,
        'borrowed_books': borrowed_books
    }

    return render(request, 'accounts/profile.html', context)



class UserRegisterview(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('register')

    def form_valid(self, form):
        user = form.save()
        
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    def get_success_url(self) -> str:
        return reverse_lazy('profile')
    
    

class UserLogoutView(LogoutView):
    next_page = 'homepage'


@login_required
def DepositeMoney(request):
    user_account, created = UserAccountModel.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_account = request.user.account
        form = DepositeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user_account = request.user.account
            user_account.deposite(amount)

            # subject = 'Deposite Message'
            # to_mail = request.user.email
            # message = render_to_string('accounts/deposite_mail.html',{
            #     'user': request.user,
            #     'amount': amount,
            # })
            # sent_mail = EmailMultiAlternatives(subject,'',to=[to_mail])
            # sent_mail.attach_alternative(message,"text/html")
            # sent_mail.send()
            sending_user_mail(request.user,"Deposite Message","accounts/deposite_mail.html",amount)
            return redirect('profile')
    else:
        form = DepositeForm()  
    return render(request,'accounts/deposite.html',{'form':form})



class ProfileUpdate(LoginRequiredMixin,UpdateView):
    model = User
    form_class = ProfileUpdateForm
    pk_url_kwarg = "id"
    template_name = 'accounts/update_profile.html'
    success_url = reverse_lazy('profile')


    def form_valid(self, form):
        update_form = super().form_valid(form)
        messages.success(self.request, 'Profile Update Successfully.')
        return update_form


class UserPassChangeView(LoginRequiredMixin,PasswordChangeView):
    template_name = 'accounts/update_profile.html'
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        pass_form = super().form_valid(form)
        messages.success(self.request, 'Password change successful.')
        return pass_form
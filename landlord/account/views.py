# -*- coding: utf-8 -*-
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm

from landlord.custom.decorators import guest_or_redirect
from landlord.account.forms import SignInForm, SignUpForm


class SignInView(View):

    @method_decorator(guest_or_redirect)
    def get(self, request):
        return render(request, 'account/sign-in.html',
                      {'form': SignInForm()})

    @method_decorator(guest_or_redirect)
    def post(self, request):
        form = SignInForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(reverse('home'))

        return render(request, 'account/sign-in.html', {'form': form})


class SignUpView(View):

    @method_decorator(guest_or_redirect)
    def get(self, request):
        return render(request, 'account/sign-up.html',
                      {'form': SignUpForm()})

    @method_decorator(guest_or_redirect)
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('account:signin'))

        return render(request, 'account/sign-up.html', {'form': form})


class SignOutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('home'))


class ResetPasswordView(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'account/reset-password.html',
                      {'form': PasswordChangeForm(user=request.user)})

    @method_decorator(login_required)
    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if not form.is_valid():
            return render(request, 'account/reset-password.html',
                          {'form': form})
        form.save()
        return HttpResponseRedirect(reverse('home'))

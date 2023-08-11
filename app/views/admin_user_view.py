import os
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger

from app.utility import queries, return_message, constants, question_module_functions
from app.forms.admin_users_settings_from import SearchForm, UserSettingsForm

@question_module_functions.superuser_required()
class AdminUser(LoginRequiredMixin, BaseDetailView):

    def get(self, request, *args, **kwargs):
        """ List view of all users with search functionality and pagination"""
        page = request.GET.get("page", constants.DEFAULT_PAGE)
        search_name = request.GET.get("username")
        search_mail = request.GET.get("email")
        search_role = request.GET.get("role")
        initial_dict = {
            "username": search_name,
            "email": search_mail,
            "role": search_role
        }
        add_user_form = UserSettingsForm()
        search_form = SearchForm(initial=initial_dict)

        data = queries.get_all_user(search_name, search_mail, search_role)
        if not data.exists():
            messages.error(request, return_message.MESSAGE['no_data'])

        paginator = Paginator(data, constants.PAGE_LIMIT)
        number_pages = paginator.num_pages

        try:
            page_obj = paginator.page(page)
            page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page) 
        except (PageNotAnInteger, InvalidPage):
            page_obj = None
            messages.error(request, return_message.MESSAGE['invalid_page'])
        query_params = ""
        if (search_name or search_mail or search_role):
            query_params = (
                f"&username={search_name}&email={search_mail}&role={search_role}")
        context = {
            'query': query_params,
            'data': page_obj,
            'search_form': search_form,
            'add_user_form': add_user_form,
            "username": search_name,
            "email": search_mail,
            "role": search_role,
        }

        return render(request, "admin_user_settings.html", context)


class UserSettingsView(LoginRequiredMixin, BaseDetailView):

    def post(self, request, *args, **kwargs):
        method = request.POST.get('method')

        username = request.POST.get('username')
        password = os.environ.get('PASSWORD')
        email = request.POST.get('email')
        role = request.POST.get('role')
        status = request.POST.get('status')
        userID = request.POST.get('userID')
        is_staff = role == constants.ADMIN
        admin = False
        status = status == constants.ACTIVE

        if method:
            user_flag = True
            if not userID:
                user_flag = False
            if user_flag:
                user = queries.get_user_by_id(userID)
                if user is None:
                    user_flag = False
            if not user_flag:
                messages.error(
                    request, return_message.MESSAGE['user_not_found'])
                return redirect("/admin_user")

            if method == "put":
                """Update existing user"""
                username = username.strip()
                email = email.strip()
                if user.email != email:
                    if User.objects.filter(email=email).exists():
                        messages.error(request,
                        return_message.MESSAGE['email_exist']
                        )
                        return redirect('/admin_user')
                try:
                    user.username = username
                    user.email = email
                    user.is_active = status
                    user.is_superuser = admin
                    user.is_staff = is_staff

                    user.save()

                    messages.success(request, 
                    return_message.MESSAGE['user_update']
                    )
                    return redirect("/admin_user")

                except IntegrityError as e:
                    messages.error(request, 
                    return_message.MESSAGE['user_exist']
                    )
                    return redirect("/admin_user")

            elif method == 'delete':
                """Delete existing user"""
                try:
                    if user.is_superuser:
                        messages.error(request, return_message.MESSAGE['administrator_error'])
                        return redirect("/admin_user")
                    user.delete()
                    messages.success(request, 
                    return_message.MESSAGE['user_delete']
                    )
                    return redirect("/admin_user")

                except Exception as e:
                    messages.error(request, e)
                    return redirect("/admin_user")

        else:
            """Create new user"""
            try:
                username = username.strip()
                email = email.strip()
                
                check_email = User.objects.filter(email=email).all()
                if check_email:
                    messages.error(request, 
                    return_message.MESSAGE['email_exist']
                    )
                    return redirect('/admin_user')

                create_user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    is_active=status,
                    is_superuser=admin,
                    is_staff=is_staff
                )
                create_user.save()

                messages.success(request, 
                return_message.MESSAGE['user_added']
                )
            except IntegrityError as e:
                messages.error(request, 
                return_message.MESSAGE['user_exist']
                )

        return redirect("/admin_user")

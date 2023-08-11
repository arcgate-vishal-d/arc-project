import os
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger
from datetime import date

from app.utility import queries, return_message, constants, question_module_functions
from app.forms import PaperSearchForm
from app.models import PaperHistory,TestLevels

@question_module_functions.admin_required()
class SetTodaysPaper(LoginRequiredMixin, BaseDetailView):
    def get(self, request, *args, **kwargs):
        test_level = request.GET.get('test_levels')
        paper_sets = request.GET.get('paper_sets')
        page = request.GET.get("page", constants.DEFAULT_PAGE)
        initial_dict = {
            "paper_sets": paper_sets,
            "test_levels": test_level,
        }
        search_today_paper_form = PaperSearchForm(
            initial=initial_dict)

        data = queries.get_paper_description(
            id=paper_sets, test_level=test_level)

        if not data.exists():
            messages.error(
                request, return_message.MESSAGE['paper_not_found'])

        paginator = Paginator(data, constants.PAGE_LIMIT)

        try:
            page_obj = paginator.page(page)
            page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page) 
        except (PageNotAnInteger, InvalidPage):
            page_obj = None
            messages.error(request, return_message.MESSAGE['no_data'])

        query_params = ""
        if (paper_sets or test_level):
            query_params = (
                f"&paper_set={paper_sets}&test_level={test_level}")
        current_paper_dict = {}
        level_list = list(TestLevels.objects.all())
        for level in level_list:
            current_paper_dict[level]= PaperHistory.objects.filter(paper_set__test_level__test_level = level).last()
       
        context = {
            'query': query_params,
            'data': page_obj,
            'test_levels': test_level,
            'paper_sets': paper_sets,
            'search_paper_form': search_today_paper_form,
            'current_paper': current_paper_dict,
        }

        return render(request, "admin_set_todays_paper.html", context)

    def post(self, request, *args, **kwargs):
        today_paper_id = request.POST.get('today_paper_set_id')
        todays_paper = PaperHistory()
        todays_paper.paper_set = queries.get_paper_setup_description_by_id(today_paper_id)
        todays_paper.set_by = queries.get_user_by_username(request.user)
        todays_paper.date = date.today()
        todays_paper.save()
        messages.success(
                    request, return_message.MESSAGE['paper_set'])

        return redirect('/set_today_paper')

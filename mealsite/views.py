from dataclasses import fields
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, FormView
from .models import Meal, MealRating
from django.urls import reverse_lazy
from django.http import Http404
from django.db.models import Avg
from .forms import DetailForm


class IndexView(CreateView):
    template_name = 'index.html'
    model = Meal
    fields = ('name', 'description', 'imageUrl',
              'countryOfOrigin', 'typicalMealTime')
    success_url = reverse_lazy('mealsite:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["topRated"] = Meal.objects.annotate(avg_rating=Avg(
            "mealrating__rating")).filter(avg_rating__gte=3.5)[0:3]

        context["recentlyAdded"] = Meal.objects.all().order_by(
            '-dateAdded')[0:3]

        return context


class CategoryListView(ListView):
    template_name: str = 'mealsite/list.html'
    model = Meal

    def get_queryset(self):
        queryset = Meal.objects.all()
        category = self.kwargs['category']
        print(category)
        hash = {1: 'morning', 2: 'afternoon', 3: 'evening'}

        list_of_key = list(hash.keys())
        list_of_value = list(hash.values())

        if category in list_of_value:
            position = list_of_key[list_of_value.index(category)]
            queryset = Meal.objects.filter(typicalMealTime=position)

        elif category == 'toprate':
            queryset = queryset.annotate(avg_rating=Avg(
                "mealrating__rating")).filter(avg_rating__gte=3.5)

        elif category == 'recently':
            queryset = Meal.objects.all().order_by('-dateAdded')

        else:
            raise Http404("Question does not exist")

        # クエリパラメータ取得
        param_value = self.request.GET.get(
            "sort") if self.request.GET.get("sort") else ''

        if param_value == 'rate':
            queryset = queryset.annotate(avg_rating=Avg(
                "mealrating__rating")).order_by('-avg_rating')

        elif param_value == 'country':
            queryset = queryset.order_by('-countryOfOrigin')

        elif param_value == 'data':
            queryset = queryset.order_by('-dateAdded')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['category'].upper()
        context['category'] = self.kwargs['category']
        return context


class MealDetail(DetailView, FormView):
    template_name: str = 'mealsite/detail.html'
    model = Meal
    form_class = DetailForm
    context_object_name = "meal"

    def form_valid(self, form):
        rating = form.save(commit=False)
        meal_id = self.kwargs["pk"]
        rating.meal_id = meal_id
        rating.save()

        self.success_url = reverse(
            'mealsite:detail', kwargs={'pk': meal_id})
        return super().form_valid(form)

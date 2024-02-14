from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError

# Create your views here.
class homePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
        "title": "About us - Online Store",
        "subtitle": "About us",
        "description": "This is an about page ...",
        "author": "Developed by: Your Name",
        })
        return context
    

class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title" : "Contact Page - Online Store",
            "subtitle" : "Contact",
            "email" : "EMAIL: zxjdioajdsa@eafit.edu.co",
            "address" : "ADDRESS: 830 Courtland Ave. Suwanee, GA 30024",
            "phoneNumber" : "PHONE NUMBER: +65 4551214541",
        })
        return context


class Product: 

    products = [ 
        {"id":"1", "name":"TV", "description":"Best TV", "price": "150$ USD"}, 
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": "5000000$ USD"}, 
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": "10$ USD"}, 
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": "400$ USD"} 
    ] 


class ProductIndexView(View): 
    template_name = 'products/index.html' 
    def get(self, request): 
        viewData = {} 
        viewData["title"] = "Products - Online Store" 
        viewData["subtitle"] =  "List of products" 
        viewData["products"] = Product.products 
        return render(request, self.template_name, viewData) 


class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product_id = int(id) - 1
            product = Product.products[product_id]
            
            price_value = float(product["price"].replace('$ USD', ''))
            product["color"] = "red" if float(product["price"].replace('$ USD', '')) > 100 else "black"


            viewData = {
                "title": product["name"] + " - Online Store",
                "subtitle": product["name"] + " - Product information",
                "product": product
            }
            return render(request, self.template_name, viewData)
        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse('home'))
    
    

class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required= True)
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError('The price must be greater than zero.')
        return price
    

class ProductCreateView(View):
    template_name = 'products/create.html'
    
    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)
    
    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            
            return render(request, 'products/product_created.html', {})
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)
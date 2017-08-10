from django.shortcuts import redirect, render
from django.core import serializers
from .models import Person
import json

def index(request):
    """
    Home page view
    """

    if request.method == "POST":
        data = request.POST
        return render(request,'myapp/result.html', {'result':data['user']})

    people = Person.objects.all()  # Fetch data from database
    people_json_raw = serializers.serialize('json', people)  # Convert to JSON
    people_json_dict = json.loads(people_json_raw) # Convert to Python dict
    people_json_dict_small = [i['fields'] for i in people_json_dict] # Strip out data

    insert_dict = {} # Make another dictionary to hold nicer data structure

    insert_dict['country'] = []
    country_list = set([i['country'] for i in people_json_dict_small]) # Get unique countries

    # This loop is to take the unordered queryset and turn it into better formatted JSON-like
    # structure of {country:cities:users} instead of a list of dictionaries.
    for country in list(country_list):
        city_list = []
        for el in people_json_dict_small:
            if el['country'] == country:
                city_list.append(el['city'])

        city_list = set(city_list)
        city_list = list(city_list) # Convert set type to list type

        insert_dict['country'].append({'name':country,
                                       'cities':[{'name':city} for city in city_list]})
        for city in city_list:
            user_list = []
            for el in people_json_dict_small:
                if el['country'] == country:
                    if el['city'] == city:
                        user_list.append(el['username'])
            for item in insert_dict['country']:
                if item['name'] == country:
                    for citem in item['cities']:
                        if citem['name'] == city:
                            citem['users'] = []
                            citem['users'].append(user_list)
                            citem['users']  = [item for sublist in citem['users'] for item in sublist]
                            
    return render(request, 'myapp/index.html', {'data_in' : json.dumps(insert_dict)})

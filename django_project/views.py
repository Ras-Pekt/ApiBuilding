import random
import requests
from django.shortcuts import render


BASE_URL = "https://freetestapi.com/api/v1/"
USELESS_BASE_URL = "https://uselessfacts.jsph.pl/"

urls = {
  "books": f"{BASE_URL}/books",
  "students": f"{BASE_URL}/students",
  "today_facts": f"{USELESS_BASE_URL}/api/v2/facts/today",
  "random_facts": f"{USELESS_BASE_URL}/api/v2/facts/random",
}

# https://freetestapi.com/api/v1/books  # Get all books
# https://freetestapi.com/api/v1/books/1  # Get single book
# https://freetestapi.com/api/v1/books?limit=5  # Get five books
# https://freetestapi.com/api/v1/books?search=[query]  # Search by name or title
# https://freetestapi.com/api/v1/books?sort=name&order=dec # Sort by name or title


def index(request):
    response = requests.get(urls["books"])
    fact_response = requests.get(urls["today_facts"]).json()
    student_response = requests.get(urls["students"]).json()

    print(student_response[0].keys())
    keys = ["name", "age", "gender", "address", "email", "phone", "courses", "gpa"]

    rand_num = random.randrange(0, len(student_response))

    for key, value in student_response[rand_num].items():
        if key in keys:
            print(key, ":", value)
    # name = data2[rand_num]['name']



    fact = fact_response['text']
    dog = 'dog'  
    name = 'name'

    context = [

    ]
  
    return render(request, 'templates/index.html', {'fact': fact, 'dog': dog,  'name': name})


def random_facts(request):
    response_list = []
    
    for i in range(5):
        response = requests.get(urls["random_facts"])
        fact_response = response.json()["text"]
        response_list.append(fact_response)

    if request.session.get("response_list") is None:
        request.session['response_list'] = response_list
    else:
        request.session['response_list'] += response_list


    facts = request.session.get("response_list")
    return render(request, 'templates/random_facts.html', {"facts": facts})

def clear_facts(request):
    request.session['response_list'] = []
    return render(request, 'templates/random_facts.html', {"facts": []})
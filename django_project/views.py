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

def index(request):
    """
    This function will return a random book, student, and fact.
    
    Args:
        request (HttpRequest): The request object.
    Returns:
        render: Renders index.html.
    """
    book_response = requests.get(urls["books"]).json()
    fact_response = requests.get(urls["today_facts"]).json()
    student_response = requests.get(urls["students"]).json()


    rand_bk_num = random.randrange(0, len(book_response))
    book_dict = {}

    for key, value in book_response[rand_bk_num].items():
        if key in ["title", "author", "description"]:
            book_dict[key] = value

    params = {
        "book_title": book_dict.get("title"),
        "author_name": book_dict.get("author"),
    }
    cover_url = "http://bookcover.longitood.com/bookcover"
    img_url = requests.get(cover_url, params=params).json()

    book_dict["url"] = img_url.get("url")
    book_dict["description"] = book_dict.get("description").replace(".", ",")

    keys = ["name", "age", "gender", "address", "email", "phone", "courses", "gpa"]
    rand_num = random.randrange(0, len(student_response))
    student_dict = {}

    for key, value in student_response[rand_num].items():
        if key in keys:
            student_dict[key] = value

    student_dict["first_name"] = student_dict["name"].split(" ")[0]

    if student_dict.get("gender") == "Male":
        student_dict["pronoun"] = "He"
    elif student_dict.get("gender") == "Female":
        student_dict["pronoun"] = "She"

    fact = fact_response['text']

    context = {
        "fact": fact,
        "student_dict": student_dict,
        "book_dict": book_dict,
    }
  
    return render(request, 'templates/index.html', context)


def random_facts(request):
    """
    This function will return 5 random facts.
    
    Args:
        request (HttpRequest): The request object.
    Returns:
        render: Renders random_facts.html.
    """
    response_list = []
    
    for _ in range(5):
        response = requests.get(urls["random_facts"])
        fact_response = response.json()["text"]
        response_list.append(fact_response)

    if request.session.get("response_list") is None:
        request.session['response_list'] = response_list
    else:
        request.session['response_list'] += response_list


    facts = request.session.get("response_list")
    return render(request, 'templates/random_facts.html', {"facts": facts})


def random_books(request):
    """
    This function will return 5 random books.

    Args:
        request (HttpRequest): The request object.
    Returns:
        render: Renders random_books.html.
    """
    book_response = requests.get(urls["books"]).json()

    book_list = []

    for _ in range(5):
        rand_bk_num = random.randrange(0, len(book_response))
        book_dict = {}

        for key, value in book_response[rand_bk_num].items():
            if key in ["title", "author", "description"]:
                book_dict[key] = value

        params = {
            "book_title": book_dict.get("title"),
            "author_name": book_dict.get("author"),
        }
        cover_url = "http://bookcover.longitood.com/bookcover"
        img_url = requests.get(cover_url, params=params).json()

        book_dict["url"] = img_url.get("url")
        book_list.append(book_dict)

    return render(request, 'templates/random_books.html', {"book_list": book_list})


def clear_facts(request):
    """
    This function will clear the facts list.
    
    Args:
        request (HttpRequest): The request object.
    Returns:
        render: Renders random_facts.html.
    """
    request.session['response_list'] = []
    return render(request, 'templates/random_facts.html', {"facts": []})


def clear_books(request):
    """
    This function will clear the book list.
    
    Args:
        request (HttpRequest): The request object.
    Returns:
        render: Renders random_books.html.
    """
    request.session['book_list'] = []
    return render(request, 'templates/random_books.html', {"book_list": []})

from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect


def index(request):
    # queries db for a list of all cats,
    # then orders them by likes in descending order
    # retrieves only top five or less if there's less
    # then places it in our context dict
    category_list = Category.objects.order_by("-likes")[:5]

    # does same as above but for pages sorted by views
    page_list = Page.objects.order_by("-views")[:5]

    context_dict = {}

    context_dict["boldmessage"] = "Crunchy, creamy, cookie, candy, cupcake!"
    context_dict["categories"] = category_list
    context_dict["pages"] = page_list
    # returns rendered response to client, with the template we've set up
    # and the context dict
    return render(request, "rango/index.html", context=context_dict)


def about(request):
    context_dict = {
        "boldmessage": "This tutorial has been put together by Angus Wilson"
    }
    return render(request, "rango/about.html", context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        # tries to find cat name from given slug
        # otherwise deals with DoesNotExist exception.
        category = Category.objects.get(slug=category_name_slug)

        # retreive all pages assosciated w cat
        pages = Page.objects.filter(category=category)

        context_dict["pages"] = pages
        context_dict["category"] = category
    except Category.DoesNotExist:
        # if we can't find cat, set vals in context dict to None
        context_dict["category"] = None
        context_dict["pages"] = None

    return render(request, "rango/category.html", context=context_dict)


def add_category(request):
    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)

        # check if form valid

        if form.is_valid():
            form.save(commit=True)
            # placeholder, just returns to index if form valid
            return redirect("/rango/")

        else:
            # if errors just print to terminal
            print(form.errors)

    return render(request, "rango/add_category.html", {"form": form})

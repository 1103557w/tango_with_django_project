from django.shortcuts import render, redirect
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse


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


def add_page(request, category_name_slug):
    # check if cat exists and return to index if not
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect("/rango/")

    form = PageForm()

    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(
                    reverse(
                        "rango:show_category",
                        kwargs={"category_name_slug": category_name_slug},
                    )
                )

        else:
            print(form.errors)

    context_dict = {"form": form, "category": category}
    return render(request, "rango/add_page.html", context=context_dict)


def register(request):
    # bool to know if registration succeeded
    registered = False

    if request.method == "POST":
        # gets info from form
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # hash password
            user.set_password(user.password)
            user.save()

            # commit false so we can ensure the user profile form is properly
            # assosciated thus maintaining ref integrity
            profile = profile_form.save(commit=False)
            profile.user = user

            # check if user set picture and save it if so
            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]

            profile.save()

            # reg successful so update reg bool
            registered = True

        else:
            # prints error to terminal if form invalid
            print(user_form.errors, profile_form.errors)

    else:
        # not POST so we just render form
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(
        request,
        "rango/register.html",
        context={
            "user_form": user_form,
            "profile_form": profile_form,
            "registered": registered,
        },
    )


def user_login(request):

    # similar to register func, if request is a post process it
    if request.method == "POST":
        # use post.get(var) as opposed to post(var) as get returns None if var
        # doesn't exist and POST(var) raises a KeyError
        username = request.POST.get("username")
        password = request.POST.get("password")

        # use Django's inbuilt validation system
        user = authenticate(username=username, password=password)

        # check if user exists - eg if authentication has worked, if it hasn't
        # None will have been returned and thus if fails.
        if user:
            if user.is_active:
                # if info is correct, and user is active login
                login(request, user)
                return redirect(reverse("rango:index"))

            else:
                # inactive account
                return HttpResponse("Your Rango account is disabled")

        else:
            # bad login details
            # in the book it has us printing out the entered password
            # but i think that seems insecure, so I'm just leaving it
            # as the username and hopefully that will pass
            print(f"Invalid login details for {username}")

    else:
        # it's not a POST so it's probably a GET
        # display login form
        return render(request, "rango/login.html")

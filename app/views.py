from django.shortcuts import render

# Create your views here.
def home(request):

    if request.user.is_authenticated:
        if Join.objects.filter(user_id=request.user).exists():
            hood = Hood.objects.get(pk=request.user.join.hood_id.id)
            posts = Posts.objects.filter(hood=request.user.join.hood_id.id)
            businesses = Business.objects.filter(
                hood=request.user.join.hood_id.id)

            return render(request, 'hoods/hood.html', {"hood": hood, "businesses": businesses, "posts": posts})
        else:
            neighbourhoods = Hood.objects.all()
            return render(request, 'index.html', {"neighbourhoods": neighbourhoods})
    else:
        neighbourhoods = Hood.objects.all()
        return render(request, 'index.html', {"neighbourhoods": neighbourhoods})

def new_business(request):
    current_user = request.user

    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = current_user
            business.hood = request.user.join.hood_id
            business.save()
            return redirect('home')

    else:
        form = BusinessForm()
    return render(request, 'business.html', {"form": form})
@login_required(login_url='/accounts/login/')
def profile(request):
    profile = Profile.objects.get(user=request.user)
    hoods = Hood.objects.filter(user=request.user).all()
    business = Business.objects.filter(user=request.user).all()
    return render(request, 'profiles/profile.html', {"profile": profile, "hoods": hoods, "business": business})


@login_required(login_url='/accounts/login/')
def edit_profile(request):
    current_user = request.user
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.email = current_user.email
            profile.save()
        return redirect('profile')

    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'profiles/edit_profile.html', {"form": form})
def hoods(request):

    hood = Hood.objects.filter(user=request.user)

    return render(request, 'hoods/hood.html', {"hood": hood})


@login_required(login_url='/accounts/login/')
def join(request, hoodId):

    hood = Hood.objects.get(pk=hoodId)
    if Join.objects.filter(user_id=request.user).exists():
        Join.objects.filter(user_id=request.user).update(hood_id=hood)
    else:

        Join(user_id=request.user, hood_id=hood).save()

    messages.success(
        request, 'Success! You have succesfully joined this Neighbourhood ')
    return redirect('home')
@login_required(login_url='/accounts/login/')
def exitHood(request, hoodId):

    if Join.objects.filter(user_id=request.user).exists():
        Join.objects.get(user_id=request.user).delete()
        messages.error(
            request, 'You have succesfully exited this Neighbourhood.')
        return redirect('home')

def search(request):

    if request.GET['search']:
        hood_search = request.GET.get("search")
        hoods = Hood.search_hood(hood_search)
        message = f"{hood_search}"

        return render(request, 'hoods/search.html', {"message": message, "hoods": hoods})

    else:
        message = "You Haven't searched for any hood"
        return render(request, 'hood/search.html', {"message": message})


@login_required(login_url='/accounts/login/')
def create_post(request):

    if Join.objects.filter(user_id=request.user).exists():
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.posted_by = request.user
                post.hood = request.user.join.hood_id
                post.save()
                messages.success(
                    request, 'You have succesfully created a Post')
                return redirect('home')
        else:
            form = PostForm()
        return render(request, 'posts/createpost.html', {"form": form})


@login_required(login_url='/accounts/login/')
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.poster = current_user
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()
        return render(request, 'comment.html', {"user": current_user, "comment_form": form})

def delete_post(request, postId):
    Posts.objects.filter(pk=postId).delete()
    messages.error(request, 'Succesfully Deleted a Post')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))







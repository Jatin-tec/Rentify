from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rent.models import Property, Notification
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

def home(request):
    properties = Property.objects.all()
    page = request.GET.get('page', 1)
    property_type = request.GET.get('property_type')
    search_query = request.GET.get('search_query')

    # Filter properties by property type
    if property_type and property_type != 'all':
        properties = properties.filter(property_type=property_type)

    # Filter properties by search query
    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    paginator = Paginator(properties, 3)  # Show 3 properties per page
    
    try:
        properties = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        properties = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        properties = paginator.page(paginator.num_pages)

    properties_with_owner = []
    for property in properties:
        property_with_owner = {
            'id': property.id,
            'owner': {
                'email': property.owner.email,
                'first_name': property.owner.first_name,
                'last_name': property.owner.last_name,
                'phone_number': property.owner.phone_number,
            },
            'title': property.title,
            'description': property.description,
            'price': property.price,
            'location': property.location,
            'area': property.area,
            'property_type': property.property_type,
            'bedrooms': property.bedrooms,
            'bathrooms': property.bathrooms,
            'nearby_hospitals': property.nearby_hospitals,
            'nearby_colleges': property.nearby_colleges,
            'images': property.images
        }
        properties_with_owner.append(property_with_owner)
    
    is_authenticated = request.user.is_authenticated

    return render(request, 'home.html', {
        'properties': properties_with_owner,
        'property_type': property_type,
        'search_query': search_query,
        'is_authenticated': is_authenticated
    })


@login_required
def post_property(request):
    if request.method == 'POST':
        title = request.POST.get('title', None)
        description = request.POST.get('description', None)
        price = request.POST.get('price', None)
        location = request.POST.get('location', None)
        area = request.POST.get('area', None)
        property_type = request.POST.get('property_type', None)
        bedrooms = request.POST.get('bedrooms', None)
        bathrooms = request.POST.get('bathrooms', None)
        nearby_hospitals = request.POST.get('nearby_hospitals', None)
        nearby_colleges = request.POST.get('nearby_colleges', None)
        image = request.FILES.get('images', None)

        if title and description and price and location and area and property_type and bedrooms and bathrooms:
            property = Property(
                owner=request.user,
                title=title,
                description=description,
                price=price,
                location=location,
                area=area,
                property_type=property_type,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                nearby_hospitals=nearby_hospitals,
                nearby_colleges=nearby_colleges,
                images=image
            )
            property.save()
            messages.success(request, 'Property posted successfully!')
        else:
            messages.error(request, 'Please fill all the fields!')

    return render(request, 'property_post.html')

@login_required
def edit_property(request, id):
    property = Property.objects.get(id=id)
    if request.method == 'POST' and property.owner == request.user:

        title = request.POST.get('title', None)
        description = request.POST.get('description', None)
        price = request.POST.get('price', None)
        location = request.POST.get('location', None)
        area = request.POST.get('area', None)
        property_type = request.POST.get('property_type', None)
        bedrooms = request.POST.get('bedrooms', None)
        bathrooms = request.POST.get('bathrooms', None)
        nearby_hospitals = request.POST.get('nearby_hospitals', None)
        nearby_colleges = request.POST.get('nearby_colleges', None)
        image = request.FILES.get('images', None)
        
        if title:
            property.title = title
        if description:
            property.description = description
        if price:
            property.price = price
        if location:
            property.location = location
        if area:
            property.area = area
        if property_type:
            property.property_type = property_type
        if bedrooms:
            property.bedrooms = bedrooms
        if bathrooms:
            property.bathrooms = bathrooms
        if nearby_hospitals:
            property.nearby_hospitals = nearby_hospitals
        if nearby_colleges:
            property.nearby_colleges = nearby_colleges
        if image:
            property.images = image

        property.save()
        messages.success(request, 'Property updated successfully!')

    return render(request, 'property_edit.html', {'property': property})

@login_required
def delete_property(request, id):
    property = Property.objects.get(id=id)

    if property.owner != request.user:
        messages.error(request, 'You are not the owner of this property!')
        return render(request, 'my_properties.html')
    
    property.delete()
    messages.success(request, 'Property deleted successfully!')
    return render(request, 'my_properties.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def properties(request):
    properties_list = Property.objects.filter(owner=request.user)
    page = request.GET.get('page', 1)

    print(page)
    # Paginate the properties
    paginator = Paginator(properties_list, 3)  # Show 10 properties per page
    
    try:
        properties = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        properties = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        properties = paginator.page(paginator.num_pages)

    return render(request, 'my_properties.html', {'properties': properties})

@login_required
def inbox(request):
    notifications_list = Notification.objects.filter(user=request.user)
    page = request.GET.get('page', 1)

    # Paginate the notifications
    paginator = Paginator(notifications_list, 10)

    try:
        notifications = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        notifications = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        notifications = paginator.page(paginator.num_pages)


    return render(request, 'inbox.html', {'notifications': notifications})

@login_required
def property_detail(request, pk):
    property = get_object_or_404(Property, id=pk)

    # Create a notification for the property owner
    if request.user.is_authenticated:
        notification = Notification(
            user=property.owner,
            viewed_by=request.user,
            message=f'{request.user.first_name} {request.user.last_name} viewed your property: {property.title}'
        )
        notification.save()
        return JsonResponse({
            "status": "success",
        })

    return JsonResponse({
        "status": "user is not authenticated",
    })
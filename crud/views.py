from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders, Users
from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def gender_list(request):
    try:
        genders = Genders.objects.all()

        data = {
            'genders':genders
        }

        return render(request, 'gender/GendersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during load genders: {e}')

@login_required
def add_gender(request):
    try:
        if request.method == 'POST':
            gender = request.POST.get('gender')

            Genders.objects.create(gender=gender).save()
            messages.success(request, 'Gender added successfully!')
            return redirect('/gender/list')
        else:   
            return render(request, 'gender/AddGender.html')
    except Exception as e:
        return HttpResponse(f'Error occured during add gender: {e}')

@login_required
def edit_gender(request, genderId):
    try:
        if request.method == 'POST':
            genderObj = Genders.objects.get(pk=genderId)

            gender = request.POST.get('gender')

            genderObj.gender = gender
            genderObj.save()

            messages.success(request, 'Gender updated successfully!')

            data = {
                'gender':genderObj
            }

            return render(request, 'gender/EditGender.html', data)
        else:
            genderObj = Genders.objects.get(pk=genderId)

            data = {
                'gender':genderObj
            }

            return render(request, 'gender/EditGender.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during edit gender: {e}')

@login_required
def delete_gender(request, genderId):
    try:
        if request.method == 'POST':
            genderObj = Genders.objects.get(pk=genderId)
            genderObj.delete()

            messages.success(request, 'Gender deleted successfully!')
            return redirect('/gender/list')
        else:
            genderObj = Genders.objects.get(pk=genderId)

            data = {
                'gender':genderObj
            }

            return render(request, 'gender/DeleteGender.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during delete gender: {e}')

@login_required
def user_list(request):
    try:
        print("Logged in user:", request.user)
        search_query = request.GET.get('search', '')

        # Start with all users, filter if search is entered
        users = Users.objects.select_related('gender')

        if search_query:
            users = users.filter(
                Q(full_name__icontains=search_query) |
                Q(username__icontains=search_query) |
                Q(email__icontains=search_query)         # Search by email
            )


        paginator = Paginator(users, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        return render(request, 'user/UsersList.html', {'page_obj': page_obj, 'search_query': search_query})
    except Exception as e:
        return HttpResponse(f'Error occurred during load users: {e}')

@login_required
def add_user(request):
    try:
        if request.method == 'POST':
            fullName = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birth_date = request.POST.get('birth_date')
            address = request.POST.get('address')
            contactNumber = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirmPassword = request.POST.get('confirm_password')

            form_data = {
                'full_name': fullName,
                'gender': gender,
                'birth_date': birth_date,
                'address': address,
                'contact_number': contactNumber,
                'email': email,
                'username': username,
            }

            if not fullName: 
                messages.error(request, 'Full name is required!')
                return render(request, 'user/AddUser.html', {
                    'genders': Genders.objects.all(),
                    'form_data': form_data 
                })
            
            if not gender:
                messages.error(request, 'Gender is required!')
                return render(request, 'user/AddUser.html', {
                    'genders': Genders.objects.all(),
                    'form_data': form_data
                })

            if not birth_date:
                messages.error(request, 'Birth date is required!')
                return render(request, 'user/AddUser.html', {
                    'genders': Genders.objects.all(),
                    'form_data': form_data
                })
            
            if not address:
                messages.error(request, 'Address is required!')
                return render(request, 'user/AddUser.html', {
                    'genders': Genders.objects.all(),
                    'form_data': form_data
                })
            
            if not contactNumber:
                messages.error(request, 'Contact number is required!')
                return render(request, 'user/AddUser.html', {
                    'genders': Genders.objects.all(),
                    'form_data': form_data
                })
            
            if not username:
                messages.error(request, 'Username is required!')
                return render(request, 'user/AddUser.html', {
                    'genders': Genders.objects.all(),
                    'form_data': form_data
                })

            if not password:
                messages.error(request, 'Password is required!')
                return render(request, 'user/AddUser.html', {
                    'genders': Genders.objects.all(),
                    'form_data': form_data
                })
            

            if password != confirmPassword:
                messages.error(request, 'Password and confirm password do not match!')
                return render(request, 'user/AddUser.html', {
                    'genders': Genders.objects.all(),
                    'form_data': form_data
                })
            
            if Users.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose another one.')
                return render(request, 'user/AddUser.html', {
                    'genders': Genders.objects.all(),
                    'form_data': request.POST
                })

            Users.objects.create(
                full_name=fullName,
                gender=Genders.objects.get(pk=gender),
                birth_date=birth_date,
                address=address,
                contact_number=contactNumber,
                email=email,
                username=username,
                password=make_password(password)
            ).save()
            
            messages.success(request, 'User added successfully!')
            return redirect('/user/add')   
        else:
            genderObj = Genders.objects.all()

            data = {
                'genders':genderObj
            }

            return render(request, 'user/AddUser.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during add user: {e}')     

@login_required
def user_edit(request, userId):
    try:
        userObj = Users.objects.get(pk=userId)
        genders = Genders.objects.all()  # Get all available genders

        if request.method == 'POST':
            username = request.POST.get('username')
            gender_id = request.POST.get('gender')
            birth_date = request.POST.get('birth_date')
            email = request.POST.get('email')
            address = request.POST.get('address')
            contact_number = request.POST.get('contact_number')

            userObj.address = address
            userObj.contact_number = contact_number
            userObj.username = username
            userObj.gender_id = gender_id  # Assign the selected gender
            userObj.birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
            userObj.email = email if email else None
            userObj.save()

            messages.success(request, 'User updated successfully!')

            form_data={
                'username' : username
            }

            if Users.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose another one.')
                return render(request, 'user/AddUser.html', {
                    'genders': Genders.objects.all(),
                    'form_data': form_data
                })

        data = {
            'user': userObj,
            'genders': genders,
            'selected_gender_id': userObj.gender_id,  # For preselection
        }

        return render(request, 'user/EditUser.html', data)

    except Exception as e:
        return HttpResponse(f'Error occurred during edit user: {e}')

@login_required
def user_delete(request, userId):
    try:
        if request.method == 'POST':
            userObj = Users.objects.get(pk=userId)
            userObj.delete()

            messages.success(request, 'User deleted successfully!')
            return redirect('/user/list')
        else:
            userObj = Users.objects.get(pk=userId)

            data = {
                'user':userObj
            }

            return render(request, 'user/DeleteUser.html', data)
    except Exception as e:
        return HttpResponse(f"Error occurred during user deletion: {e}")
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login successful!")

            next_url = request.GET.get('next')
            return redirect(next_url if next_url else '/user/list')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'user/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        return redirect('user_list')  # or dashboard
    else:
        return redirect('login')

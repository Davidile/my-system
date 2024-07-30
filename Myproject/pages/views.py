from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .models import Task,User
from datetime import date,timedelta
from django.utils import timezone
from django.db.models import F, Value, FloatField
from django.db.models.functions import Coalesce
import weasyprint
from django.template.loader import render_to_string,get_template




# Create your views here.
def landing_page(request):
    return render(request,"base.html")

def home(request):
    if request.user.is_authenticated:
       tasks = Task.objects.filter(assigned_to=request.user, deadline__gte=date.today())
       score = 0
       if tasks.exists():
        score = tasks.first().calculate_score_percentage()
       return render(request, "home.html", {'tasks': tasks, 'score':score})
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have logged in successfully")
                return redirect('home')
            else:
                messages.error(request, "There was an error, please try again")
                return render(request, 'home.html')
        return render(request, "home.html")
  
def logout_user(request):
    logout(request)
    messages.success(request,'You have logged out')
    return redirect('landing_page')


"""def register_user(request):
    if request.method=="POST":
        form=Signupform(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,"you have successfull registered")
            return redirect('home')
    else:
        form=Signupform()
        return render(request,"register.html",{'form':form})
    return render(request,"register.html",{'form':form})

def record(request,pk):
    if request.user.is_authenticated:

       customer_record=Record.objects.get(id=pk)
       return render(request,"record.html",{'customer_record':customer_record})
    else:
        messages.success(request,"You must be logged in !")
        return redirect('home')
    
def delete_record(request,pk):
    if request.user.is_authenticated:
      delete_it=Record.objects.get(id=pk)
      delete_it.delete()
      messages.success(request,"Records deleted successfully....")
      return redirect('home')
    else:
        messages.success(request,"You must be logged in to do that!")
        return redirect('home')



def add_record(request):
    form=Add_record(request.POST or None)
    if request.user.is_authenticated:
       if request.method=="POST":  
            if form.is_valid():
              form.save()
              messages.success(request,"Records added successfully ...")
              return redirect('home')
         
       return render(request,"add_record.html",{'form':form})
    else:
        messages.success(request,"You must be logged in ..")
        return redirect("home")
    

def update_record(request,pk):
    if request.user.is_authenticated:
        current_record=Record.objects.get(id=pk)
        form=Add_record(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,"Record has been updated")
            return redirect("home")
        return render(request,"update_record.html",{'form':form})
    else:
         messages.success(request,"You must be logged in ..")
         return redirect("home")
    
"""

def complete_task(request, task_id):
 if request.user.is_authenticated:
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    if request.method == 'POST':
        task.is_completed = True
        task.save()
        return redirect('home')
    return render(request, 'base.html', {'task': task})
 
"""def track_progress(request):
    reviews = Task.objects.all()
    sorted_reviews = sorted(reviews, key=lambda review: review.calculate_score_percentage(), reverse=True)
    return render(request, 'track_progress.html', {'reviews': sorted_reviews})"""


"""def generate_pdf(request):
    reviews = Task.objects.all()
    sorted_reviews = sorted(reviews, key=lambda review: review.calculate_score_percentage(), reverse=True)
    template = get_template('generatepdf.html')
    html = template.render({'reviews': sorted_reviews})

    pdf = HTML(string=html,base_url=request.build_absolute_uri('/')).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline;attachment; filename="performance_report.pdf"'

    return response"""
def generate_pdf(request, user_id):
    user = User.objects.get(id=user_id)
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Start of the current week

    tasks = Task.objects.filter(assigned_to=user, completion_date__gte=start_of_week, completion_date__lte=today)
    completed_tasks = tasks.filter(is_completed=True).count()
    total_tasks = tasks.count()

    if total_tasks == 0:
        score_percentage = 0
    else:
        score_percentage = (completed_tasks / total_tasks) * 100

    print(f"User: {user.username}")
    print(f"Score Percentage: {score_percentage}")
    print(f"Tasks: {tasks}")

    html_string = render_to_string('generatepdf.html', {
        'tasks': tasks,
        'user': user,
        'score_percentage': score_percentage,
        'start_of_week': start_of_week,
        'today': today
    })
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=weekly_report.pdf'
    weasyprint.HTML(string=html_string).write_pdf(response)
    return response
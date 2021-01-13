from django.shortcuts import render,redirect
from . import forms,models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from datetime import datetime,timedelta,date
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from pymongo import MongoClient
from django.contrib.auth.models import User
import itertools
import os
# import face_recognition
# import cv2
# import numpy
#
# def facedect(loc):
#          cam = cv2.VideoCapture(0)
#          s, img = cam.read()
#          if s:
#                  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#                  MEDIA_ROOT =os.path.join(BASE_DIR,'pages')
#                  loc=(str(MEDIA_ROOT)+loc)
#                  face_1_image = face_recognition.load_image_file(loc)
#                  face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]
#                  small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
#                  rgb_small_frame = small_frame[:, :, ::-1]
#                  face_locations = face_recognition.face_locations(rgb_small_frame)
#                  face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
#                  check=face_recognition.compare_faces(face_1_face_encoding, face_encodings)
#                  print(check)
#                  if check[0]:
#                         return True
#                  else :
#                         return False

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/index.html')


def studentclick_view(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/studentclick.html')


def staffclick_view(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/staffclick.html')


def staffsignup_view(request):

    form1=forms.StaffUserForm()
    form2=forms.StaffForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StaffUserForm(request.POST)
        form2=forms.StaffForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            f2.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('stafflogin')
    return render(request,'library/staffsignup.html',context=mydict)


def studentsignup_view(request):

    form1=forms.ReaderUserForm()
    form2=forms.ReaderForm()
    form3=forms.Reader_PnoForm()
    mydict={'form1':form1,'form2':form2,'form3':form3}
    if request.method=='POST':
        form1=forms.ReaderUserForm(request.POST)
        form2=forms.ReaderForm(request.POST)
        form3=forms.Reader_PnoForm(request.POST)
        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            f2.save()
            f3=form3.save(commit=False)
            f3.userid=f2
            f3.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'library/studentsignup.html',context=mydict)



def is_staff(user):

    return user.groups.filter(name='ADMIN').exists()

def afterlogin_view(request):

    if is_staff(request.user):
        return render(request,'library/staffafterlogin.html')
    else:
        return render(request,'library/studentafterlogin.html')

def stafflogin(request):

    if request.method =="POST":
                form =forms.LoginForm(request.POST)
                if form.is_valid():
                        username=request.POST['username']
                        password=request.POST['password']
                        user = authenticate(request,username=username,password=password)
                        if user is not None:
                                # face=models.Staff.objects.get(user_id=user.id)
                                # if facedect(face.head_shot.url):
                                login(request,user)
                                messages.success(request, "Successfully Logged In")
                                return redirect('afterlogin')
                        else:
                                messages.error(request, "Invalid credentials! Please try again")
                                return render(request,'library/loginfail.html')       
                return render(request,'library/loginfail.html')
    else:
                form = forms.LoginForm()
                return render(request,"library/stafflogin.html",{"form": form})  


def studentlogin(request):
    if request.method =="POST":
                form =forms.LoginForm(request.POST)
                if form.is_valid():
                        username=request.POST['username']
                        password=request.POST['password']
                        user = authenticate(username=username,password=password)
                        if user is not None:
                            # face=models.Reader.objects.get(user_id=user.id)#user_id=request.user.id
                            # if facedect(face.head_shot.url): 
                            login(request,user)
                            messages.success(request, "Successfully Logged In")
                            return redirect('afterlogin')
                        else:
                                messages.error(request, "Invalid credentials! Please try again")
                                return redirect('library/loginfail.html')    
                return redirect('library/loginfail.html')    
    else:
                form = forms.LoginForm()
                return render(request,"library/studentlogin.html",{"form": form}) 


@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def addbook_view(request):

    form1=forms.BookForm()
    form2=forms.Book_AuthorForm()
    form3=forms.Book_CategoryForm()
    mydict={'form1':form1,'form2':form2,'form3':form3}
    if request.method=='POST':
        form1=forms.BookForm(request.POST)
        form2=forms.Book_AuthorForm(request.POST)
        form3=forms.Book_CategoryForm(request.POST)
        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            u1=form1.save()
            f2=form2.save(commit=False)
            f3=form3.save(commit=False)
            f2.isbn=u1
            f3.isbn=u1
            u1.save()
            f2.save()
            f3.save()
            return render(request,'library/bookadded.html')
    return render(request,'library/addbook.html',context=mydict)


@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def addpublisher_view(request):

    form1=forms.PublisherForm()
    form2=forms.PublishedByForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.PublisherForm(request.POST)
        form2=forms.PublishedByForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            print("BOTH THE FORMS ARE VALID")
            u1=form1.save()
            f2=form2.save(commit=False)
            f2.pid=u1
            f2.save()
            print("PUBLISHER DATA ARE SAVED")
            return render(request,'library/publisheradded.html')
        else:
            print(form1.errors)
            print(form2.errors)
            print("FORMS ARE NOT VALID")
    return render(request,'library/addpublisher.html',context=mydict)



@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def viewbook_view(request):

    book1=list(models.Book.objects.all())
    book2=list(models.Book_Author.objects.all())
    book3=list(models.Book_Category.objects.all())
    b1 = []

    li = []
    for i in range(len(book1)):
        t = (book1[i].title, book1[i].isbn,book1[i].copies, book1[i].price,book1[i].edition,book2[i].author,book3[i].category)
        li.append(t)
    mydict={'li':li}
    return render(request,'library/viewbook.html',context=mydict)


@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def viewpublisher_view(request):

    book1=list(models.Publisher.objects.all())
    book2=list(models.PublishedBy.objects.all())
    print(book1)
    print(book2)
    li=[]
    for i in range(len(book1)):
        t = (book1[i].pid, book1[i].pname,book1[i].year,book2[i].isbn)
        li.append(t)
    mydict={'li':li}
    return render(request,'library/viewpublisher.html',context=mydict)



@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def issuebook_view(request):
    form=forms.IssuedToForm()
    if request.method=='POST':
        form=forms.IssuedToForm(request.POST)
        s=models.Reader.objects.get(id=request.POST.get('userid'))
        if form.is_valid() and s.total_books_due < 10:
            b=models.Book.objects.get(isbn=request.POST.get('isbn'))
            b.copies=b.copies-1
            s.total_books_due= s.total_books_due+1
            b.save()
            obj=form.save()
            obj.save()
            s.save()
            return render(request,'library/bookissued.html')
        print("Cannot Issue Book as Not Available")
    return render(request,'library/issuebook.html',{'form':form})





@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def viewissuedbook_view(request):
    issuedbooks=models.IssuedTo.objects.all()
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.returndate.day)+'-'+str(ib.returndate.month)+'-'+str(ib.returndate.year)
        days=(date.today()-ib.issuedate)
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        a=(models.Reader.objects.get(pk=ib.userid.id).get_name)
        b=(models.Reader.objects.get(pk=ib.userid.id).getuserid)
        c=(models.Book.objects.get(pk=ib.isbn.isbn).title)
        d=(models.Reader.objects.get(pk=ib.userid.id).getcopies)
        t=(a,b,c,ib.isbn.isbn,issdate,expdate,fine,d)
        li.append(t)
        print(li)
    return render(request,'library/viewissuedbook.html',{'li':li})



@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def viewstudent_view(request):

    students=models.Reader.objects.all()
    return render(request,'library/viewstudent.html',{'students':students})


@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):

    z=models.Reader.objects.get(user_id=request.user.id).id
    issuedbooks=models.IssuedTo.objects.filter(userid_id=z)
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.returndate.day)+'-'+str(ib.returndate.month)+'-'+str(ib.returndate.year)
        days=(date.today()-ib.issuedate)
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        a=(models.Book.objects.get(pk=ib.isbn.isbn).title)
        b=(models.Book.objects.get(pk=ib.isbn.isbn).isbn)
        t=(a,b,issdate,expdate,fine)
        li.append(t)
        print(li)
    return render(request,'library/viewissuedbookbystudent.html',{'li':li})


def returnbook_view (request):

    z=models.Reader.objects.get(user_id=request.user.id)
    issuedbooks=models.IssuedTo.objects.filter(userid_id=z)
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.returndate.day)+'-'+str(ib.returndate.month)+'-'+str(ib.returndate.year)
        days=(date.today()-ib.issuedate)
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        a=(models.Book.objects.get(pk=ib.isbn.isbn).title)
        b=(models.Book.objects.get(pk=ib.isbn.isbn).isbn)
        t=(a,b,issdate,expdate,fine)
        li.append(t)
    if request.method=='POST':
        print(request.POST.get("name"))
        bookidtodelete=request.POST.get("name") 
        d=models.IssuedTo.objects.get(isbn_id=bookidtodelete,userid_id=z)
        d.delete()
        z.total_books_due= z.total_books_due-1
        z.save()
        return render(request,'library/studentafterlogin.html')
    return render(request,'library/returnbook.html',{'li':li})

@login_required(login_url='studentlogin')
def add_book_review(request):

    form=forms.ReviewForm()
    client = MongoClient('localhost', 27017)
    db_handle = client['reviews_only']
    col = db_handle['library_reivew']
    u = models.Reader.objects.get(user_id=request.user.id)
    print('request user id is ', request.user.id)
    if request.method=='POST':
        form=forms.ReviewForm(request.POST)
        if form.is_valid():
            review = models.Review(isbn=request.POST.get('isbn'), review=request.POST.get('review'))
            already_done_by_person = False
            for ib in col.find():
                if u in ib.get('people_reviewed_by') and request.POST.get('isbn') == ib.get('isbn'):
                    already_done_by_person = True

            if not already_done_by_person:
                review.save(using='mongo')
                col.update_one({'isbn':request.POST.get('isbn')},{'$set': {'people_reviewed_by[u]':1} })
            else:
                return HttpResponseRedirect('You have already reviewed this ')
            return render(request,'library/studentafterlogin.html')
    return render(request,'library/add_book_review.html',{'form':form})

@login_required(login_url='studentlogin')
def view_book_review(request):

    client = MongoClient('localhost', 27017)
    db_handle = client['reviews_only']
    col = db_handle['library_review']
    li2 = []
    for ib in col.find():

        book = models.Book.objects.get(isbn=ib.get('isbn'))
        author = models.Book_Author.objects.get(isbn=ib.get('isbn'))
        t = (ib.get('isbn'),book.title, author.author, ib.get('review'))
        print(t)
        li2.append(t)

    return render(request,'library/view_book_review.html',{'li2':li2})




# email notifiaction

from django.conf import settings
from django.core.mail import send_mail
from background_task import background

@background(schedule=10)
def doemil():
    issuedbooks=models.IssuedTo.objects.all()
    today_date = date.today()
    print('sending mail to people')
    print(issuedbooks)
    # print(today_date)
    for element in issuedbooks:
        # print('userid is ',element.userid)
        w = str(element.isbn)
        act_str = ''
        i = 0
        while w[i] != '[':
            act_str += w[i]
            i += 1
        act_str = int(act_str)
        books = models.Book.objects.get(isbn=act_str)
        book = books.title
        u = User.objects.get(username=element.userid)
        return_date_of_person = element.returndate
        number = return_date_of_person - today_date
        # print(number.days)
        if return_date_of_person >= today_date:
            # no_of_days = today_date - return_date_of_person
            message = "Hi, you have to return the book titled '{}' in {} days".format(book,number.days)
            send_mail('Reminder of Book Return',
                      message,
                    'your email',
                    [u.email],
                    fail_silently=False,)
        else:
            days_over = abs(number.days)
            fine = element.fine * days_over
            message = "Hey you are paying a hefty fine of {} Rs for the book titled '{}'. Return asap !!".format(fine,book)
            send_mail('Reminder of Book Return',
                      message,
                    'your email',
                    [u.email],
                    fail_silently=False,)

doemil(schedule=10)

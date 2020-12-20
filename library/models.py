from django.db import models as sqlmodel
from django.contrib.auth.models import AbstractUser,User
from datetime import datetime,timedelta
from djongo import models as mongomodel

class Reader(sqlmodel.Model):
    user=sqlmodel.OneToOneField(User,on_delete=sqlmodel.CASCADE)
    isfaculty=sqlmodel.BooleanField()
    dept=sqlmodel.CharField(max_length=50)
    head_shot=sqlmodel.ImageField(upload_to='profil_images',blank=True)
    
    def __str__(self):
        return str(self.user.username)
    @property
    def get_name(self):
        return self.user.first_name
    @property
    def getuserid(self):
        return self.user.id

class Reader_Pno(sqlmodel.Model):
    userid=sqlmodel.ForeignKey(Reader,on_delete=sqlmodel.CASCADE)
    pnumber=sqlmodel.CharField(max_length=10)

    def __str__(self):
        return "Pno"+str(self.pnumber)

class Book(sqlmodel.Model):
    isbn=sqlmodel.CharField(max_length=30,primary_key=True,unique=True)
    copies= sqlmodel.IntegerField()
    price= sqlmodel.IntegerField()
    title=sqlmodel.CharField(max_length=30)
    edition=sqlmodel.IntegerField()
    
    def __str__(self):
        return str(self.isbn)+'['+str(self.title)+']'

class Book_Category(sqlmodel.Model):
    catchoice= [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ]
    isbn=sqlmodel.ForeignKey(Book,on_delete=sqlmodel.CASCADE)
    category=sqlmodel.CharField(max_length=30,choices=catchoice,default='education')
    def __str__(self):
        return str(self.category)

class Book_Author(sqlmodel.Model):
    isbn=sqlmodel.ForeignKey(Book,on_delete=sqlmodel.CASCADE)
    author=sqlmodel.CharField(max_length=30)
    def __str__(self):
        return str(self.author)


class Publisher(sqlmodel.Model):
    pname=sqlmodel.CharField(max_length=30)
    pid=sqlmodel.CharField(max_length=30,primary_key=True)
    year=sqlmodel.IntegerField()

    def __str__(self):
        return str(self.pname)+' '+str(self.pid)

class Staff(sqlmodel.Model):
    user=sqlmodel.OneToOneField(User,on_delete=sqlmodel.CASCADE)
    head_shot=sqlmodel.ImageField(upload_to='profil_images',blank=True)
    def __str__(self):
        return str(self.user.id)+' '+str(self.user.first_name)

class KeepsTrack(sqlmodel.Model):
    sid=sqlmodel.ForeignKey(Staff,on_delete=sqlmodel.CASCADE)
    userid=sqlmodel.ForeignKey(Reader,on_delete=sqlmodel.CASCADE)

    def __str__(self):
        return str(self.sid.id)+str(self.userid.id)

class PublishedBy(sqlmodel.Model):
    isbn=sqlmodel.ForeignKey(Book,on_delete=sqlmodel.CASCADE)
    pid=sqlmodel.ForeignKey(Publisher,on_delete=sqlmodel.CASCADE)

    def __str__(self):
        return str(self.isbn.isbn)+' '+str(self.pid.pid)


class Maintains(sqlmodel.Model):
    isbn=sqlmodel.ForeignKey(Book,on_delete=sqlmodel.CASCADE)
    sid=sqlmodel.ForeignKey(Staff,on_delete=sqlmodel.CASCADE)
    def __str__(self):
        return str(self.isbn.isbn)+str(self.sid.id)

def get_expiry():
    return datetime.today() + timedelta(days=15)

class IssuedTo(sqlmodel.Model):
    isbn=sqlmodel.ForeignKey(Book,on_delete=sqlmodel.CASCADE)
    userid=sqlmodel.ForeignKey(Reader,on_delete=sqlmodel.CASCADE)
    fine=sqlmodel.IntegerField(default=0)
    issuedate=sqlmodel.DateField(auto_now=True)
    returndate=sqlmodel.DateField(default=get_expiry)
    def __str__(self):
        return str(self.userid.id)+str(self.isbn.isbn)

class Review(mongomodel.Model):
    isbn=mongomodel.CharField(max_length=100)
    review = mongomodel.FloatField(default=0)
    objects = mongomodel.DjongoManager()

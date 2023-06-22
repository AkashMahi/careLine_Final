from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password


# Create your models here.


class User(AbstractUser):
    email=models.EmailField(max_length=45)
    phone=models.CharField(max_length=15)
    d_o_b=models.DateField(null=True)
    address=models.TextField(max_length=600)
    dist=models.CharField(max_length=45)
    state=models.CharField(max_length=45)
    id_proof=models.CharField(max_length=40)
    dr_name=models.CharField(max_length=40,null=True)
    allot_status=models.IntegerField(null=True)
    salary=models.FloatField(null=True)
    usertype=models.IntegerField(null=True)
    resume=models.FileField(null=True)
    cr_status=models.IntegerField(null=True)
    p_id=models.IntegerField(null=True)
    cr_id=models.IntegerField(null=True)
    s_id=models.IntegerField(null=True)

    # def save(self, *args, **kwargs):
    #     self.password = make_password(self.password)
    #     super(User, self).save(*args,**kwargs)
distr=["Thiruvananthapuram","Kollam","Allapuzha","Ernakulam","Kozhikode"]


class Support(models.Model):
    fname=models.CharField(max_length=30)
    lname=models.CharField(max_length=30)
    email=models.EmailField()
    message=models.TextField(max_length=500)


class Activity(models.Model):
    aname=models.CharField(max_length=45,null=True)
    astatus=models.CharField(max_length=20,null=True)
    duration=models.IntegerField(null=True)
    p_id=models.IntegerField(null=True)
    c_id=models.IntegerField(null=True)


activities=['Walking','Abdominal contractions','Wall pushups','Toe taps','Heel raises','Step-Ups']

class Appointment(models.Model):
    apname=models.CharField(max_length=40,null=True)
    aptime=models.DateTimeField(null=True)
    dr_name=models.CharField(max_length=50,null=True)
    h_name=models.CharField(max_length=100,null=True)
    dept=models.IntegerField(null=True)
    status=models.IntegerField(null=True)
    p_id=models.IntegerField(null=True)
    c_id=models.IntegerField(null=True)


medicines={"Chronic obstructive pulmonary disease (COPD)":["Combivent","Respimat",
'Duoneb', 'Symbicort','Advair','Breo Ellipta','Dulera','Stiolto Respimat'],
"Alzheimer’s disease" :['Donepezil (also known as Aricept Exelon or Reminyl)'],
'Dementia':['Donepezil','Galantamine','Rivastigmine'],
"Diabetes":['glimepiride (Amaryl)','glimepiride-pioglitazone (Duetact)','gliclazide.','glipizide.',
'glipizide ER (Glipizide XL, Glucotrol XL)'],
"High cholesterol":['Statins Atorvastatin (Lipitor)', 'Fluvastatin (Lescol XL)', 'Lovastatin (Altoprev)', 'Pitavastatin (Livalo)', 'Pravastatin (Pravachol)', 'Rosuvastatin (Crestor)', 'Simvastatin (Zocor)']
}
class Medicine(models.Model):
    mname=models.CharField(max_length=200)
    mtype=models.CharField(max_length=200)

class Medicine_details(models.Model):
    m_name=models.CharField(max_length=250)
    m_cat=models.CharField(max_length=100)
    cons_time=models.TimeField()
    p_id=models.IntegerField()
    c_id=models.IntegerField()
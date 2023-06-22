from django.shortcuts import render,redirect
from careapp.models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
# from rest_framework_simplejwt.tokens import AccessToken
import jwt


# Create your views here.


def index(request):
    return render(request,'index_cms.html')

def about(request):
    return render(request,'aboutus.html')


def caretaker_registration(request):
    def handle_uploaded_file(f):  
        with open('careapp/static/files/'+f.name, 'wb+') as destination:  
            for chunk in f.chunks():  
                destination.write(chunk)
    try:
        if request.method == 'POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            dateofbirth = request.POST['dateofbirth']
            resume = request.FILES['res']
            email = request.POST['email']
            phone = request.POST['phone']
            address = request.POST['address']
            district = request.POST['district']
            state = request.POST['state']
            id_proof = request.POST['id_proof']
            handle_uploaded_file(request.FILES['res'])
            passw=str(fname[:4]+lname[4:])
            print(type(email))

            User.objects.create_user(first_name=fname, last_name=lname,username=email,email=email,phone=phone,password=passw, d_o_b=dateofbirth, resume=resume, address=address, dist=district, state=state, id_proof=id_proof,usertype=2,cr_status=0)

            return redirect(index) # Redirect to a success page
        else:
            return render(request, 'care_reg.html',{"dist":distr})
    except:
        return render(request,'care_reg.html',{'data':"Fill the form properly"})


def client_reg(request):
    
        user=User.objects.filter(cr_status=1,allot_status=None).all()
        if request.method == 'POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            dateofbirth = request.POST['dateofbirth']
            email = request.POST['email']
            phone = request.POST['phone']
            address = request.POST['address']
            district = request.POST['district']
            state = request.POST['state']
            cr_id=request.POST['c_id']
            dr_name=request.POST['doctorname']
            id_proof = request.POST['id_proof']
            password=request.POST['password']

            User.objects.create_user(first_name=fname, last_name=lname,username=email,email=email,phone=phone,password=password, d_o_b=dateofbirth, address=address, dist=district,dr_name=dr_name, state=state, id_proof=id_proof,cr_id=cr_id,usertype=3)
            us=User.objects.filter(email=email).get()
            User.objects.filter(id=cr_id).update(p_id=us.id,allot_status=1)
            return redirect(index) # Redirect to a success page
        else:
            return render(request, 'client_reg.html',{"data":user,"d":distr})
        
SECRET_KEY = 'CareLine_Secret'
def generate_token(data):
    # print(data.id)
    payload = {
        "id": data.id
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return access_token


def logins(request):
    if request.method=='POST':
        usern = request.POST['username']
        passw = request.POST['password']
        print(type(usern))
        print(passw)
        user = authenticate(request,username=usern,password=str(passw))
        try:
            token=generate_token(user)
            print(token)
        except:
            messages.add_message(request,messages.SUCCESS,'Incorrect Credentials')
            return redirect(logins)
        
        if user is None:
            messages.add_message(request,messages.SUCCESS,'Incorrect Credentials')
            return redirect(logins)
        elif user is not None and user.usertype == 1:
            request.session['user_id'] = user.id
            request.session['token'] = token
            login(request,user)
            return redirect(cms_dash)
        
        elif user is not None and user.cr_status==1 and user.usertype == 2:
            request.session['token'] = token
            request.session['cr_id'] = user.id
            login(request,user)
            return redirect(care_dash)

        elif user is not None and user.usertype == 3:
            request.session['token'] = token
            request.session['pt_id'] = user.id
            login(request,user)
            return redirect(ptdash)
        else:
            return "HttpResponse('Sorry Invalid details')"
    else:
        return render(request,'loginbase.html')

def logouts(request):
    logout(request)
    return redirect(logins)

def token_verify(tk):
    SECRET_KEY = 'CareLine_Secret'
    payload = jwt.decode(tk, SECRET_KEY, algorithms=['HS256'])
    if payload['id'] :
        return payload['id']
    else:
        return None    
# CMS dash board
def cms_dash(request):
    try:
        tk=request.session['token']
        print("inside cms_dash",    tk)
        access = token_verify(tk)
        print(access)

        if request.session['token']:
            if request.session['user_id'] == access:
                client_count = User.objects.filter(usertype=3).count()
                cr_count = User.objects.filter(usertype=2,cr_status=1).count()
                msg_count=Support.objects.count()
                latest_records = User.objects.filter(usertype=2,cr_status=1).order_by('date_joined')

                
                return render(request,"cms_dash.html",{'c_count':client_count,'cr_count':cr_count,'msg_count':msg_count,'latest':latest_records})
            else:
                return redirect(logins)
    except:
        messages.add_message(request,messages.SUCCESS,'Please Login Again')
        return redirect(logins)
    
@login_required
def rec_request(request):
    try:
        cr_recruit=User.objects.filter(usertype=2,cr_status=0)
        return render(request,'rec_request.html',{'recruits':cr_recruit})
    except:
        messages.add_message(request,messages.SUCCESS,'Please Login Again')
        return redirect(logins)

@login_required
def apprv_cr(request,id):
    User.objects.filter(id=id).update(cr_status=1)
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return False

    # Generate a password
    passw = user.first_name[:4]+user.last_name[4:]
    subject = 'Welcome to Careline'
    message = f'You are selected for the caretaking job with the following credentials:\n\nUsername: {user.email}\nPassword: {passw}\n\n\tPlease wait for Approval from the admin (Login After Visit to Office).'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(subject, message, email_from, recipient_list)
    return redirect(rec_request)

def reject(request,id):
    user=User.objects.get(id=id)
    user.delete()
    return redirect(cms_dash)


def view_support(request):
    try:
        msg=Support.objects.all()
        return render(request,'view_msg.html',{'msg':msg})
    except:
        messages.add_message(request,messages.SUCCESS,'Please Login Again')
        return redirect(logins)

def rejectmsg(request,id):
    user=Support.objects.get(id=id)
    user.delete()
    return redirect(view_support)

def edit_cms(request):
    try:
        id=request.session['user_id']
        if request.method=='POST':
            ph=request.POST['phone']
            ad=request.POST['address']
            User.objects.filter(id=id).update(phone=ph,address=ad)
            return redirect(cms_dash)
        else:
            user=User.objects.filter(id=id).get()
            return render(request,"cms_edit.html",{"data":user})
    except:
        messages.add_message(request,messages.SUCCESS,'Please Login Again')
        return redirect(logins)

def cms_add_med(request):
    try:
        if request.session['user_id']:
            if request.method=="POST":
                mname=request.POST['mname']
                mtype=request.POST['mtype']
                Medicine.objects.create(mname=mname,mtype=mtype)
                return redirect(cms_add_med)
            else:
                return render(request,"cms_add_medicine.html",{'med':medicines.keys()})
        else:
            return HttpResponse("Unsuccessful !!! Login Again")
    except:
        messages.add_message(request,messages.SUCCESS,'Please Login Again')
        return redirect(logins)

def cms_view_activity(request):
    ap=Activity.objects.all()
    print(ap)
    return render(request,"cms_view_activity.html",{'ap':ap})

    
def cms_view_cr(request,id):
    us=User.objects.filter(id=id).get()
    return render(request,"cms_view_cr.html",{'user':us})

    
def cms_view_pt(request,id):
    us=User.objects.filter(id=id).get()
    return render(request,"cms_view_pt.html",{'user':us})



#caretaker

def care_dash(request):
    try:
        tk=request.session['token']
        print("inside cms_dash",    tk)
        access = token_verify(tk)
        print(access)
        if request.session['cr_id']==access:
            id=request.session['cr_id']
            us=User.objects.filter(id=id).get()

            if us.allot_status==1:
                pt=User.objects.filter(id=us.p_id).get()
                return render(request,'care_dash.html',{'pt':pt})
            else:
                return render(request,'care_dash.html')
        else:
            return redirect(logins)
    except:
        messages.add_message(request,messages.SUCCESS,'Please Login Again')
        return redirect(logins)


def edit_care(request):
    try:
        id=request.session['cr_id']
        if request.method=='POST':
            ph=request.POST['phone']
            ad=request.POST['address']
            User.objects.filter(id=id).update(phone=ph,address=ad)
            return redirect(care_dash)
        else:
            user=User.objects.filter(id=id).get()
            return render(request,"care_edit.html",{"data":user})
    except:
        messages.add_message(request,messages.SUCCESS,'Please Login Again')
        return redirect(logins)

def care_view_patient(request):
    id=request.session['cr_id']
    us=User.objects.filter(id=id).get()
    pt=User.objects.filter(id=us.p_id).get()
    return render(request,"care_view_patient.html",{"pt":pt})

def cr_view_appointment(request):
    try:
            
        if request.session['cr_id']:
            id=request.session['cr_id']
            try:
                us=Appointment.objects.filter(c_id=id).get()
                pt=User.objects.filter(cr_id=id).get()
                return render(request,"cr_view_appointment.html",{'apt':us,'pt':pt})
            except:
                return render(request,"cr_view_appointment.html")
    except:
        messages.add_message(request,messages.SUCCESS,'Please Login Again')
        return redirect(logins)

def appointment_complete(request,id):
    Appointment.objects.filter(id=id).update(status=1)
    return redirect(cr_view_appointment)

def appointment_delete(request,id):
    Appointment.objects.filter(id=id).delete()
    return redirect(cr_view_appointment)

def cr_view_activity(request):
    try:
        id=request.session['cr_id']
        try:
            pt=User.objects.filter(cr_id=id).get()
            act=Activity.objects.filter(c_id=id).all()
            return render(request,'cr_view_activity.html',{'act':act,'pt':pt})
        except:
            return render(request,'cr_view_activity.html')
    except:
        messages.add_message(request,messages.SUCCESS,'Please Login Again')
        return redirect(logins)

def activity_complete(request,id):
    Activity.objects.filter(id=id).update(astatus=1)
    return redirect(cr_view_activity)

def activity_delete(request,id):
    Activity.objects.filter(id=id).delete()
    return redirect(cr_view_activity)

def cr_view_med(request):
    try:
        id=request.session['cr_id']
        try:
            pt=User.objects.filter(cr_id=id).get()
            med=Medicine_details.objects.filter(c_id=id).all().order_by('cons_time')
            return render(request,'cr_view_med.html',{'med':med,'pt':pt})
        except:
            return render(request,'cr_view_med.html')
    except:
        messages.add_message(request,messages.SUCCESS,'Please Login Again')
        return redirect(logins)


def cr_depart(request,id):
    Appointment.objects.filter(id=id).update(dept=1)
    return redirect(care_dash)


# Patient View 
@login_required
def ptdash(request):
    try:
        if request.session['pt_id']:
            id=request.session['pt_id']

            us=User.objects.filter(id=id).get()
            if us.cr_id:
                print(us.cr_id)
                pt=User.objects.filter(id=us.cr_id).get
                return render(request,"patient_dash.html",{'pt':pt})
        else:
            return redirect(logins)
    except:
        messages.add_message(request,messages.SUCCESS,'Please Login Again')
        return redirect(logins)


def edit_pt(request):
    try:
        id=request.session['pt_id']
        if request.method=='POST':

            ph=request.POST['phone']
            ad=request.POST['address']
            User.objects.filter(id=id).update(phone=ph,address=ad)
            return redirect(ptdash)
        else:
            user=User.objects.filter(id=id).get()
            return render(request,"pt_edit.html",{"data":user})
    except:
        messages.add_message(request,messages.SUCCESS,'Please Login Again')
        return redirect(logins)
        
def patient_add_activity(request):
    try:
        id=request.session['pt_id']
        us=User.objects.filter(id=id).get()
        if request.method=="POST":
            act=request.POST['act_name']
            dur=request.POST['duration']
            Activity.objects.create(aname=act,duration=dur,p_id=us.id,c_id=us.cr_id)
            return redirect(patient_add_activity)
        else:
            return render(request,"patient_add_activity.html",{'act':activities,"user":us})
    except:
        messages.add_message(request,messages.SUCCESS,'Please Login Again')
        return redirect(logins)
        
def pt_view_activity(request):
    try:
        id=request.session['pt_id']
        act=Activity.objects.filter(p_id=id).all()
        return render(request,"pt_view_act.html",{"act":act})
    except:
        messages.add_message(request,messages.SUCCESS,'Please Login Again')
        return redirect(logins)

def pt_remove_act(request,id):
    Activity.objects.filter(id=id).delete()
    return redirect(pt_view_activity)

def patient_add_appointment(request):
    try:
        id=request.session['pt_id']
        us=User.objects.filter(id=id).get()
        if request.method=="POST":
            ap_type=request.POST["apt_type"]
            dr_name=request.POST["dr_name"]
            hs_name=request.POST["hs_name"]
            time=request.POST['time']
            Appointment.objects.create(apname=ap_type,aptime=time,dr_name=dr_name,h_name=hs_name,p_id=us.id,c_id=us.cr_id)
            return redirect(ptdash)
        else:
            try:
                mp=Appointment.objects.filter(p_id=id).get()
                return render(request,"patient_add_apt.html",{"user":us,"map":mp})
            except:
                return render(request,"patient_add_apt.html",{"user":us})
    except:
        messages.add_message(request,messages.SUCCESS,'Please Login Again')
        return redirect(logins)

    
def patient_add_medicine(request):
    try:
        id=request.session['pt_id']
        us=User.objects.filter(id=id).get()
        ms=Medicine.objects.all()
        if request.method=="POST":
            mname=request.POST["mname"]
            mtype=request.POST['mtype']
            time=request.POST['time']
            Medicine_details.objects.create(m_name=mname,m_cat=mtype,cons_time=time,p_id=us.id,c_id=us.cr_id)
            return redirect(patient_add_medicine)
        else:
            return render(request,"patient_add_med.html",{"user":us,"med":ms})
    except:
        messages.add_message(request,messages.SUCCESS,'Please Login Again')
        return redirect(logins)



#support

def support(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        message = request.POST['message']
        email = request.POST['email']
        Support.objects.create(fname=fname,lname=lname,message=message,email=email)
        messages.success(request, 'Submitted successful!')
        return redirect(index)
    else:
        return render(request,'support.html')
    
# map
def maps(request):
    return render(request,"maps.html")




from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.contrib.auth import login,logout,authenticate
from datetime import date
from django.contrib.auth.decorators import login_required
from .forms import DocumentUploadForm,SignedContractUploadForm
from django.http import HttpResponse
import csv
from django.utils import timezone
from datetime import timedelta
from .utils import send_email
from django.http import HttpResponse, Http404
from datetime import timedelta
import zipfile
import io
from datetime import datetime
from django.http import JsonResponse

from .forms import *
# Create your views here.

def index(request):
    return render(request, 'index.html')



# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import EmployeeDetail, EmployeeExperience, EmployeeEducation
from django.contrib.auth import login, logout, authenticate

def registration(request):
    error = ""
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        ec = request.POST['empcode']
        em = request.POST['email']
        pwd = request.POST['pwd']
        cpwd = request.POST['cpwd']
        ts = request.POST['tehsil']
        ds = request.POST['district']
        addr = request.POST['address']
        bg = request.POST['blood_group']
        dept = request.POST['department']
        desg = request.POST['designation']
        contact = request.POST['contact']
        coverage = request.POST['coverage']
        dob = request.POST['dob']


        if pwd != cpwd:
            error = "yes"
        else:
            try:
                user = User.objects.create_user(first_name=fn, last_name=ln, username=em, email=em, password=pwd)
                EmployeeDetail.objects.create(
                    user=user,
                    empcode=ec,
                    tehsil=ts,
                    district=ds,
                    adress=addr,
                    blood_group=bg,
                    empdept=dept,
                    designation=desg,
                    contact=contact,
                    coverage=coverage,
                    dob=dob
                )
                EmployeeExperience.objects.create(user=user)
                EmployeeEducation.objects.create(user=user)
                error = "no"
                # Send email notification
                subject = 'Registration Successful'
                message = 'You have successfully registered. Please upload all required documents.'
                recipient_list = [em]
                send_email(subject, message, recipient_list)
            except Exception as e:
                print(e)  # This will help to see the actual error in the console
                error = "yes"
    d = {'error': error}
    return render(request, 'registration.html', d)

# Other views remain unchanged

def emp_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['emailid']
        p = request.POST['password']
        user = authenticate(username=u,password=p)
        if user:
            login(request, user)
            error = "no"
        else:
            error = "yes"
    d = {'error': error}
    return render(request, 'emp_login.html',d)

def Logout(request):
    logout(request)
    return redirect('/')

def emp_home(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    return render(request, 'emp_home.html')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    error = ""
    user = request.user
    employee = EmployeeDetail.objects.get(user=user)
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        ec = request.POST['empcode']
        dept = request.POST['department']
        designation = request.POST['designation']
        contact = request.POST['contact']
        jdate = request.POST['jdate']
        gender = request.POST['gender']

        employee.user.first_name = fn
        employee.user.last_name = ln
        employee.empcode = ec
        employee.empdept = dept
        employee.designation = designation
        employee.contact = contact
        employee.gender = gender

        if jdate:
            employee.joiningdate = jdate
        try:
            employee.save()
            employee.user.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'employee': employee}
    return render(request, 'profile.html',d)


def myexperience(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')

    user = request.user
    experience = EmployeeExperience.objects.get(user=user)


    d = {'experience': experience}
    return render(request, 'myexperience.html',d)

def edit_myexperience(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')

    user = request.user
    experience = EmployeeExperience.objects.get(user=user)

    if request.method == "POST":
        cn1 = request.POST['company1name']
        cdes1 = request.POST['company1desig']
        csal1 = request.POST['company1salary']
        cd1 = request.POST['company1duration']

        cn2 = request.POST['company2name']
        cdes2 = request.POST['company2desig']
        csal2 = request.POST['company2salary']
        cd2 = request.POST['company2duration']

        cn3 = request.POST['company3name']
        cdes3 = request.POST['company3desig']
        csal3 = request.POST['company3salary']
        cd3 = request.POST['company3duration']

        experience.company1name = cn1
        experience.company1desig = cdes1
        experience.company1salary = csal1
        experience.company1duration = cd1

        experience.company2name = cn2
        experience.company2desig = cdes2
        experience.company2salary = csal2
        experience.company2duration = cd2

        experience.company3name = cn3
        experience.company3desig = cdes3
        experience.company3salary = csal3
        experience.company3duration = cd3

        try:
            experience.save()
            error = "no"
        except:
            error = "yes"

    return render(request, 'edit_myexperience.html',locals())


def myeducation(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')

    user = request.user
    education = EmployeeEducation.objects.get(user=user)


    d = {'education': education}
    return render(request, 'myeducation.html',d)

def edit_myeducation(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')

    user = request.user
    education = EmployeeEducation.objects.get(user=user)

    if request.method == "POST":
        cpg = request.POST['coursepg']
        scpg = request.POST['schoolclgpg']
        ypg = request.POST['yearpassingpg']
        ppg = request.POST['percentagepg']

        cg = request.POST['coursegra']
        scg = request.POST['schoolclggra']
        yg = request.POST['yearpassinggra']
        pg = request.POST['percentagegra']

        cssc = request.POST['coursessc']
        scssc = request.POST['schoolclgssc']
        ypssc = request.POST['yearpassingssc']
        pssc = request.POST['percentagessc']

        chsc = request.POST['coursehsc']
        schsc = request.POST['schoolclghsc']
        yhsc = request.POST['yearpassinghsc']
        phsc = request.POST['percentagehsc']


        education.coursepg = cpg
        education.schoolclgpg = scpg
        education.yearpassingpg = ypg
        education.percentagepg = ppg

        education.coursegra = cg
        education.schoolclggra = scg
        education.yearpassinggra = yg
        education.percentagegra = pg

        education.coursessc = cssc
        education.schoolclgssc = scssc
        education.yearpassingssc = ypssc
        education.percentagessc = pssc

        education.coursehsc = chsc
        education.schoolclghsc = schsc
        education.yearpassinghsc = yhsc
        education.percentagehsc = phsc

        try:
            education.save()
            error = "no"
        except:
            error = "yes"

    return render(request, 'edit_myeducation.html',locals())


def change_password(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    error = ""
    if request.method=="POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"

    return render(request,'change_password.html',locals())


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'admin_login.html',locals())


@login_required

def admin_home(request):
    employee_counts = {
        'PENDING': EmployeeDetail.objects.filter(status='PENDING').count(),
        'DOC_PENDING': EmployeeDetail.objects.filter(status='DOC_PENDING').count(),
        'DOC_VERIFIED': EmployeeDetail.objects.filter(status='DOC_VERIFIED').count(),
        'CONTRACT_PENDING': EmployeeDetail.objects.filter(status='CONTRACT_PENDING').count(),
        'FINALIZED': EmployeeDetail.objects.filter(status='FINALIZED').count(),
    }

    current_year = datetime.now().year
    expiration_counts = [
        EmployeeDetail.objects.filter(expiry_date__year=current_year, expiry_date__month=month).count()
        for month in range(1, 12+1)
    ]

    context = {
        'employee_counts': employee_counts,
        'expiration_counts': expiration_counts,
        'current_year': current_year,
    }
    return render(request, 'admin_home.html', context)

def get_expiration_counts(request, year):
    expiration_counts = [
        EmployeeDetail.objects.filter(expiry_date__year=year, expiry_date__month=month).count()
        for month in range(1, 12+1)
    ]
    return JsonResponse(expiration_counts, safe=False)
def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method=="POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"

    return render(request,'change_passwordadmin.html',locals())

@login_required
def export_employees_csv(request):
    employees = EmployeeDetail.objects.filter(status='FINALIZED')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Employee Code', 'Custom Employee Code', 'First Name', 'Last Name', 'Email', 
        'Contact', 'Department', 'Designation', 'Joining Date', 'Tehsil', 'District', 'Blood Group'
    ])

    for employee in employees:
        writer.writerow([
            employee.empcode, employee.custom_employee_code(), employee.user.first_name,
            employee.user.last_name, employee.user.email, employee.contact,
            employee.empdept, employee.designation, employee.joiningdate,
            employee.tehsil, employee.district, employee.blood_group
        ])

    return response

def all_employee(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    employees = EmployeeDetail.objects.filter(status='FINALIZED')
    return render(request, 'all_employee.html', {'employees': employees})

def delete_employee(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('all_employee')


def edit_profile(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    employee = EmployeeDetail.objects.get(id=pid)
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        ec = request.POST['empcode']
        dept = request.POST['department']
        designation = request.POST['designation']
        contact = request.POST['contact']
        jdate = request.POST['jdate']
        gender = request.POST['gender']
        tehsil = request.POST['tehsil']
        district = request.POST['district']
        addr = request.POST['address']
        blood_group = request.POST['blood_group']
        coverage= request.POST['coverage']
        dob = request.POST['dob']

        employee.user.first_name = fn
        employee.user.last_name = ln
        employee.empcode = ec
        employee.empdept = dept
        employee.designation = designation
        employee.contact = contact
        employee.tehsil = tehsil
        employee.district = district
        employee.address = addr
        employee.blood_group = blood_group
        employee.gender = gender
        employee.coverage= coverage
        dob=dob

        if jdate:
            employee.joiningdate = jdate
        try:
            employee.save()
            employee.user.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error, 'employee': employee}
    return render(request, 'edit_profile.html', d)


def edit_education(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    user = User.objects.get(id=pid)
    education = EmployeeEducation.objects.get(user=user)

    if request.method == "POST":
        cpg = request.POST['coursepg']
        scpg = request.POST['schoolclgpg']
        ypg = request.POST['yearpassingpg']
        ppg = request.POST['percentagepg']

        cg = request.POST['coursegra']
        scg = request.POST['schoolclggra']
        yg = request.POST['yearpassinggra']
        pg = request.POST['percentagegra']

        cssc = request.POST['coursessc']
        scssc = request.POST['schoolclgssc']
        ypssc = request.POST['yearpassingssc']
        pssc = request.POST['percentagessc']

        chsc = request.POST['coursehsc']
        schsc = request.POST['schoolclghsc']
        yhsc = request.POST['yearpassinghsc']
        phsc = request.POST['percentagehsc']


        education.coursepg = cpg
        education.schoolclgpg = scpg
        education.yearpassingpg = ypg
        education.percentagepg = ppg

        education.coursegra = cg
        education.schoolclggra = scg
        education.yearpassinggra = yg
        education.percentagegra = pg

        education.coursessc = cssc
        education.schoolclgssc = scssc
        education.yearpassingssc = ypssc
        education.percentagessc = pssc

        education.coursehsc = chsc
        education.schoolclghsc = schsc
        education.yearpassinghsc = yhsc
        education.percentagehsc = phsc

        try:
            education.save()
            error = "no"
        except:
            error = "yes"

    return render(request, 'edit_education.html',locals())


def edit_experience(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    user = User.objects.get(id=pid)
    experience = EmployeeExperience.objects.get(user=user)

    if request.method == "POST":
        cn1 = request.POST['company1name']
        cdes1 = request.POST['company1desig']
        csal1 = request.POST['company1salary']
        cd1 = request.POST['company1duration']

        cn2 = request.POST['company2name']
        cdes2 = request.POST['company2desig']
        csal2 = request.POST['company2salary']
        cd2 = request.POST['company2duration']

        cn3 = request.POST['company3name']
        cdes3 = request.POST['company3desig']
        csal3 = request.POST['company3salary']
        cd3 = request.POST['company3duration']

        experience.company1name = cn1
        experience.company1desig = cdes1
        experience.company1salary = csal1
        experience.company1duration = cd1

        experience.company2name = cn2
        experience.company2desig = cdes2
        experience.company2salary = csal2
        experience.company2duration = cd2

        experience.company3name = cn3
        experience.company3desig = cdes3
        experience.company3salary = csal3
        experience.company3duration = cd3

        try:
            experience.save()
            error = "no"
        except:
            error = "yes"

    return render(request, 'edit_experience.html',locals())

# views.py
@login_required
def document_upload_view(request):
    employee_detail = get_object_or_404(EmployeeDetail, user=request.user)
    
    if employee_detail.status not in ['PENDING', 'DOC_PENDING']:
        return render(request, 'document_upload.html', {'error': 'You are not allowed to upload documents at this stage.'})

    existing_document = Document.objects.filter(employee=request.user).first()
    
    if request.method == 'POST':
        if existing_document:
            form = DocumentUploadForm(request.POST, request.FILES, instance=existing_document)
        else:
            form = DocumentUploadForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)
            document.employee = request.user
            document.save()
            employee_detail.status = 'DOC_PENDING'
            employee_detail.save()
            return redirect('emp_home')
    else:
        form = DocumentUploadForm(instance=existing_document if existing_document else None)
    
    return render(request, 'document_upload.html', {'form': form})



@login_required
def admin_verify_documents(request):
    pending_documents = Document.objects.filter(verified=False)
    employees = EmployeeDetail.objects.filter(status='DOC_PENDING')
    return render(request, 'admin_verify_documents.html', {'employees': employees, 'pending_documents': pending_documents})

@login_required
def verify_document(request, employee_id):
    document = get_object_or_404(Document, employee_id=employee_id)
    document.verified = True
    document.save()
    employee_detail = get_object_or_404(EmployeeDetail, user=document.employee)
    employee_detail.status = 'DOC_VERIFIED'
    employee_detail.save()
    # Send email notification
    subject = 'Documents Verified'
    message = 'Your documents have been verified. Please upload the signed contract.'
    recipient_list = [document.employee.email]
    send_email(subject, message, recipient_list)
    return redirect('admin_verify_documents')

@login_required
def reject_document(request, employee_id):
    document = get_object_or_404(Document, employee_id=employee_id)
    employee_detail = get_object_or_404(EmployeeDetail, user=document.employee)
    document.verified = False
    document.save()
    employee_detail.status = 'PENDING'  # Revert to the previous status so they can upload again
    employee_detail.save()
    # Send email notification
    subject = 'Documents Rejected'
    message = 'Your documents have been rejected. Please re-upload the required documents.'
    recipient_list = [document.employee.email]
    send_email(subject, message, recipient_list)
    return redirect('admin_verify_documents')

@login_required
def signed_contract_upload_view(request):
    employee_detail = get_object_or_404(EmployeeDetail, user=request.user)
    
    if employee_detail.status != 'DOC_VERIFIED':
        return render(request, 'signed_contract_upload.html', {'error': 'You are not allowed to upload the signed contract at this stage.'})
    
    existing_contract = SignedContract.objects.filter(employee=request.user).first()
    
    if request.method == 'POST':
        if existing_contract:
            form = SignedContractUploadForm(request.POST, request.FILES, instance=existing_contract)
        else:
            form = SignedContractUploadForm(request.POST, request.FILES)

        if form.is_valid():
            contract = form.save(commit=False)
            contract.employee = request.user
            contract.save()
            employee_detail.status = 'CONTRACT_PENDING'
            employee_detail.save()
            return redirect('emp_home')
    else:
        form = SignedContractUploadForm(instance=existing_contract if existing_contract else None)
    
    return render(request, 'signed_contract_upload.html', {'form': form})


@login_required
def admin_verify_contracts(request):
    pending_contracts = SignedContract.objects.filter(verified=False)
    employees = EmployeeDetail.objects.filter(status='CONTRACT_PENDING')
    return render(request, 'admin_verify_contracts.html', {'employees': employees, 'pending_contracts': pending_contracts})



@login_required
def verify_contract(request, employee_id):
    employee_detail = get_object_or_404(EmployeeDetail, user__id=employee_id)
    contract = get_object_or_404(SignedContract, employee__id=employee_id)
    contract.verified = True
    contract.save()
    employee_detail.status = 'FINALIZED'
    employee_detail.save()
    # Send email notification
    subject = 'Contract Verified'
    message = 'Your contract has been verified. You have completed all steps.'
    recipient_list = [employee_detail.user.email]
    send_email(subject, message, recipient_list)
    return redirect('admin_verify_contracts')

@login_required
def download_aadhaar_card(request, employee_id):
    document = get_object_or_404(Document, employee_id=employee_id)
    response = HttpResponse(document.aadhaar_card, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{document.aadhaar_card.name}"'
    return response

@login_required
def download_pan_card(request, employee_id):
    document = get_object_or_404(Document, employee_id=employee_id)
    response = HttpResponse(document.pan_card, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{document.pan_card.name}"'
    return response

@login_required
def download_light_bill(request, employee_id):
    document = get_object_or_404(Document, employee_id=employee_id)
    response = HttpResponse(document.light_bill, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{document.light_bill.name}"'
    return response

@login_required
def download_photo(request, employee_id):
    document = get_object_or_404(Document, employee_id=employee_id)
    response = HttpResponse(document.photo, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{document.photo.name}"'
    return response

@login_required
def download_contract(request, employee_id):
    contract = get_object_or_404(SignedContract, employee_id=employee_id)
    response = HttpResponse(contract.contract, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{contract.contract.name}"'
    return response

# views.py
@login_required
def reject_contract(request, employee_id):
    employee_detail = get_object_or_404(EmployeeDetail, user__id=employee_id)
    contract = get_object_or_404(SignedContract, employee__id=employee_id)
    contract.verified = False
    contract.save()
    employee_detail.status = 'DOC_VERIFIED'
    employee_detail.save()
    # Send email notification
    subject = 'Contract Rejected'
    message = 'Your contract has been rejected. Please re-upload the signed contract.'
    recipient_list = [employee_detail.user.email]
    send_email(subject, message, recipient_list)
    return redirect('admin_verify_contracts')
@login_required
def renew_expiry_date(request, employee_id):
    employee = get_object_or_404(EmployeeDetail, id=employee_id)
    employee.expiry_date = employee.expiry_date + timedelta(days=365)
    employee.save()
    # Send email notification
    subject = 'ID Renewed'
    message = f'Your ID has been renewed. The new expiry date is {employee.expiry_date}.'
    recipient_list = [employee.user.email]
    send_email(subject, message, recipient_list)
    return redirect('all_employee')

def generate_employee_code(empcode, district):
    if district == "All Gujarat":
        return f"GJ/{empcode}"
    else:
        district_initials = "".join([word[0] for word in district.split()[:2]]).upper()
        return f"GJ/{district_initials}/{empcode}"
    

def view_document(request, document_type, employee_id):
    file_url = None
    is_image = False
    
    if document_type == 'aadhaar_card':
        document = get_object_or_404(Document, employee_id=employee_id)
        file_url = document.aadhaar_card.url
    elif document_type == 'pan_card':
        document = get_object_or_404(Document, employee_id=employee_id)
        file_url = document.pan_card.url
    elif document_type == 'light_bill':
        document = get_object_or_404(Document, employee_id=employee_id)
        file_url = document.light_bill.url
    elif document_type == 'photo':
        document = get_object_or_404(Document, employee_id=employee_id)
        file_url = document.photo.url
        is_image = True
    elif document_type == 'contract':
        contract = get_object_or_404(SignedContract, employee_id=employee_id)
        file_url = contract.contract.url
    else:
        raise ValueError('Invalid document type')

    context = {
        'file_url': file_url,
        'is_image': is_image if document_type == 'photo' else False,
    }

    return render(request, 'file_viewer.html', context)
    
@login_required
def download_zip(request):
    # Create a zip file in memory
    zip_filename = "Gujarat_Employee_Details.zip"
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        employees = EmployeeDetail.objects.filter(status='FINALIZED')
        for employee in employees:
            district_folder = f"{employee.district}"
            tehsil_folder = f"{employee.tehsil}"
            user_folder = f"{employee.user.username}"
            
            # Add documents to the zip file
            try:
                document = Document.objects.get(employee=employee.user)
                if document.aadhaar_card:
                    zip_file.write(document.aadhaar_card.path, f"{district_folder}/{tehsil_folder}/{user_folder}/aadhaar_card.pdf")
                if document.pan_card:
                    zip_file.write(document.pan_card.path, f"{district_folder}/{tehsil_folder}/{user_folder}/pan_card.pdf")
                if document.light_bill:
                    zip_file.write(document.light_bill.path, f"{district_folder}/{tehsil_folder}/{user_folder}/light_bill.pdf")
                if document.photo:
                    zip_file.write(document.photo.path, f"{district_folder}/{tehsil_folder}/{user_folder}/photo.jpg")
            except Document.DoesNotExist:
                pass

            # Add signed contracts to the zip file
            try:
                contract = SignedContract.objects.get(employee=employee.user)
                if contract.contract:
                    zip_file.write(contract.contract.path, f"{district_folder}/{tehsil_folder}/{user_folder}/contract.pdf")
            except SignedContract.DoesNotExist:
                pass

    zip_buffer.seek(0)
    
    # Serve the zip file as a response
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={zip_filename}'
    return response

@login_required
def admin_download_zip(request):
    return render(request, 'admin_download_zip.html')
@login_required
def superuser_verification_list(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    employees = EmployeeDetail.objects.filter(status='SUPERUSER_VERIFICATION_PENDING')
    return render(request, 'superuser_verification_list.html', {'employees': employees})


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from employee.views import *
from django.urls import path
from employee.views import view_document


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('registration/', registration),
    path('emp_login/', emp_login, name='emp_login'),
    path('emp_home/', emp_home, name='emp_home'),
    path('logout/', Logout),
    path('profile/', profile),
    path('myexperience', myexperience, name='myexperience'),
    path('edit_myexperience', edit_myexperience, name='edit_myexperience'),
    path('myeducation', myeducation, name='myeducation'),
    path('edit_myeducation', edit_myeducation, name='edit_myeducation'),
    path('change_password', change_password, name='change_password'),
    path('admin_login', admin_login, name='admin_login'),
    path('admin_home', admin_home, name='admin_home'),
    path('change_passwordadmin', change_passwordadmin, name='change_passwordadmin'),
    path('all_employee', all_employee, name='all_employee'),
    path('delete_employee/<int:pid>', delete_employee, name='delete_employee'),
    path('edit_profile/<int:pid>', edit_profile, name='edit_profile'),
    path('edit_education/<int:pid>', edit_education, name='edit_education'),
    path('edit_experience/<int:pid>', edit_experience, name='edit_experience'),
    
    path('document_upload/', document_upload_view, name='document_upload'),
    path('signed_contract_upload/', signed_contract_upload_view, name='signed_contract_upload'),
    path('admin_verify_documents/', admin_verify_documents, name='admin_verify_documents'),
    path('verify_document/<int:employee_id>/', verify_document, name='verify_document'),
    path('reject_document/<int:employee_id>/', reject_document, name='reject_document'),
    path('admin_verify_contracts/', admin_verify_contracts, name='admin_verify_contracts'),
    path('verify_contract/<int:employee_id>/', verify_contract, name='verify_contract'),\
    path('reject_contract/<int:employee_id>/', reject_contract, name='reject_contract'),  # Add this line
    path('view_document/<str:document_type>/<int:employee_id>/', view_document, name='view_document'),
    path('download_zip/', download_zip, name='download_zip'),  # Add this line
    path('download_aadhaar_card/<int:employee_id>/', download_aadhaar_card, name='download_aadhaar_card'),
    path('download_pan_card/<int:employee_id>/', download_pan_card, name='download_pan_card'),
    path('download_light_bill/<int:employee_id>/', download_light_bill, name='download_light_bill'),
    path('download_photo/<int:employee_id>/', download_photo, name='download_photo'),
    path('download_contract/<int:employee_id>/', download_contract, name='download_contract'),
    path('export_employees_csv/', export_employees_csv, name='export_employees_csv'),
    path('renew_expiry_date/<int:employee_id>/', renew_expiry_date, name='renew_expiry_date'),
    path('admin_download_zip/', admin_download_zip, name='admin_download_zip'),  # Add this line
    path('get_expiration_counts/<int:year>/', get_expiration_counts, name='get_expiration_counts'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

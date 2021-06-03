from django.shortcuts import render, redirect
from .models import *
import datetime
from django.http import JsonResponse
from .text_keywords_processing import chat_bow
from .arabic_text_keywords_processig import chat_bow_arabic
from .forms import InquiryForm, InquiryFormArabic, ManualResponseForm, ManualResponse_arabicForm
global link_flag, text_flag


# Create your views here.
def home(request):
    ans_input = ''
    dat = datetime.datetime.now()
    if request.method == 'POST':
        form = request.POST
        print(form, 'form data .....')
        code = form.get('title')
        if code == 'english':
            ans_input = english_menu()
        elif code == '1':
            ans_input = select_about_us()
        elif code == '2':
            ans_input = "Please enter your Query:"
        elif code == '3':
            ans_input = select_link_by_keyword(code)
        elif code == '4':
            ans_input = u"<a href={0} style=\"color: yellow\">{1}</a>".format('/InquiryForm',
                                                                              'Click here to submit your inquiry!')
        elif ('a' <= code <= 'z') or ('A' <= code <= 'Z'):
            ans_input = select_text_by_keyword(code)
        elif code == '5':
            ans_input = english_exit()
        elif code == 'عربى':
            ans_input = arabic_menu()
        elif code == "١":
            ans_input = select_about_us_arabic()
        elif code == "٢":
            ans_input = "الرجاء إدخال الاستعلام الخاص بك"
        elif code == "٣":
            ans_input = select_link_by_keyword(code)
        elif code == "٤":
            ans_input = u"<a href={0} style=\"color: yellow\">{1}</a>".format('/InquiryForm1',
                                                                              'انقر هنا لتقديم استفسارك')
        elif code == "٥":
            ans_input = arabic_exit()
        elif '\u0080' <= code <= '\u07FF':
            ans_input = select_text_by_keyword_arabic(code)
        else:
            ans_input = "invalid option"
        data_json = {
            'msg': code,
            'ans': ans_input
        }
        return JsonResponse(data_json)
    context = {'dat': dat}
    return render(request, 'accounts/index.html', context)


# English_Option_Functions
def english_menu():
    eng_menu = "\t1. About the Service, \n\t2. Consult Me \n\t3. Gain Knowledge \n\t4. Ask your consultant\n\t5. Exit"
    return eng_menu


def arabic_menu():
    menu = "\t1. حول الخدمة \n\t2. استشرني \n\t3. اكتساب المعرفة \n\t4. اسأل مستشارك\n\t5. مخرج"
    return menu


def select_about_us():
    aboutUs = About_Us.objects.filter(about_us_paragraph__isnull=False)
    aboutUs = aboutUs[0]
    return aboutUs.about_us_paragraph


def select_about_us_arabic():
    aboutUs_arabic = About_Us_arabic.objects.filter(about_us_paragraph_arabic__isnull=False)
    aboutUs_arabic = aboutUs_arabic[0]
    return aboutUs_arabic.about_us_paragraph_arabic


def select_text_by_keyword(queryString):
    response = chat_bow(queryString)
    if response != 'Sorry, I don\'t have an answer for this right now..':
        return response
    else:
        form_link = u"<a href = {0} style =\"color: yellow\">{1}</a>".format('/queryForm',
                                                                             'Click here to submit your query directly to the admin!')
        return response + "\n" + form_link


def select_text_by_keyword_arabic(queryString):
    response = chat_bow_arabic(queryString)
    if response != 'آسف ، ليس لدي إجابة عن هذا الآن ..':
        return response
    else:
        form_link = u"<a href = {0} style =\"color: yellow\">{1}</a>".format('/queryForm1',
                                                                             'انقر هنا لإرسال استفسارك مباشرة إلى المسؤول!')
        return response + "\n" + form_link


def select_link_by_keyword(queryString):
    link_keyword = models.link_keyword.objects.filter(keyword_values__contains=str(queryString))
    link_keyword_arabic = models.link_keyword.objects.filter(keyword_values_arabic__contains=str(queryString))
    if len(link_keyword_arabic) == 0 and link_keyword:
        return link_keyword
    elif len(link_keyword) == 0 and link_keyword_arabic:
        return link_keyword_arabic
    else:
        error_msg = "Sorry, there are no links available regarding this right now.."
        return error_msg


def AskConsultant(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            Inquiry = form.save(commit=False)
            Inquiry.name = request.POST.get('name')
            Inquiry.file_number = request.POST.get('file_number')
            Inquiry.inquiry = request.POST.get('inquiry')
            Inquiry.save()
            return redirect('home')
    else:
        form = InquiryForm
    return render(request, 'accounts/InquiryForm.html', {'form': form})


def AskConsultant_arabic(request):
    if request.method == 'POST':
        form = InquiryFormArabic(request.POST)
        if form.is_valid():
            Inquiry = form.save(commit=False)
            Inquiry.name = request.POST.get('name')
            Inquiry.file_number = request.POST.get('file_number')
            Inquiry.inquiry = request.POST.get('inquiry')
            Inquiry.save()
            return redirect('home')
    else:
        form = InquiryForm
    return render(request, 'accounts/InquiryForm1.html', {'form': form})


def manualResponse(request):
    if request.method == 'POST':
        form = ManualResponseForm(request.POST)
        if form.is_valid():
            Query = form.save(commit=False)
            Query.new_keyword = request.POST.get('new_keyword')
            Query.email_id = request.POST.get('email_id')
            Query.save()
            new_key_mail(Query.new_keyword)
            return redirect('home')
    else:
        form = ManualResponseForm
    return render(request, 'accounts/queryForm.html', {'form': form})


def manualResponse_arabic(request):
    if request.method == 'POST':
        form = ManualResponse_arabicForm(request.POST)
        if form.is_valid():
            Query = form.save(commit=False)
            Query.new_keyword = request.POST.get('new_keyword_arabic')
            Query.email_id = request.POST.get('email_id_arabic')
            Query.save()
            new_key_mail(Query.new_keyword)
            return redirect('home')
    else:
        form = ManualResponseForm
    return render(request, 'accounts/queryForm1.html', {'form': form})


def english_exit():
    english_exit = "Thank You!"
    return english_exit


def arabic_exit():
    arabic_exit = 'اشكرك'
    return arabic_exit


def new_key_mail(question):
    subject = 'A new query is added!'
    message = 'A new query ''%s'' is added to the database. \nRun the server and go to http://127.0.0.1:8000/admin/chatbotApp/manual_response/ to add response.' % (
        question)
    mail = EmailMultiAlternatives(subject, message, 'serverchatbot@gmail.com', ['serverchatbot@gmail.com'])
    mail.send()

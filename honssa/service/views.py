import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from admin.models import *


def service_center(requset):
    return render(requset, 'service/service_main.html', {})

def service_board(request):
    if request.method == 'POST':
        user_id = request.user.id
        id = member_tbl.objects.get(id=user_id)
        category = request.POST['category']
        title = request.POST['title']
        question = request.POST['question']
        img = request.FILES.get('img', '')
        new_data = m2mfaq_tbl(
            member_number = id,
            comment_image = img,
            comment_title = title,
            comment_question = question,
            comment_category = category,
        )
        new_data.save()
        print(request.POST)

        return redirect('/honssa/service/m2m/')
    return render(request, 'service/board.html', {})

def m2m_list(request):
    user = member_tbl.objects.get(id=request.user.id)
    list = m2mfaq_tbl.objects.filter(member_number=user)
    print(list)

    for i in list:
        i.comment_write_date = i.comment_write_date.strftime('%Y-%m-%d')
        if i.comment_status == '0':
            i.comment_status = '미답변'
        else:
            i.comment_status = '답변완료'
    return render(request, 'service/m2m_list.html', {'list': list})

def m2m_detail(request, id):
    question = m2mfaq_tbl.objects.get(id=id)
    content = faq_answer_tbl.objects.filter(comment_number_id=question)
    if question.comment_image:
        photo = question.comment_image
    else:
        photo = None

    if content:
        content = content[0]
    else:
        pass

    return render(request, 'service/m2m_detail.html', {'content': content, 'question': question, 'photo': photo})

def service_faq(request):
    return render(request, 'service/service_faq.html', {})
# Create your views here.

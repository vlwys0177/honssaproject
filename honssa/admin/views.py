import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.conf import settings
from django.utils.timezone import make_aware

from .models import *

def admin_login(request):
    if request.method == 'POST':
        if request.POST["id"] == "" or request.POST["password"] == "":
            return render(request, 'admin/login.html', {})

        id = request.POST["id"]
        password = request.POST["password"]
        if User.objects.get(username=id).is_superuser is True:
            user = auth.authenticate(request, username=id, password=password)
            if user is not None:
                login(request, user)
                return redirect("admin:admin_main")

    return render(request, 'admin/login.html', {})

def admin_logout(request):
    logout(request)
    return redirect("admin:admin_login")

def admin_index(request):
    m2m_list = m2mfaq_tbl.objects.order_by('-id')
    being = []
    m2m = []

    for i in range(5):
        being.append(m2m_list[i])

    for i in being:
        i.comment_write_date = i.comment_write_date.strftime('%Y-%m-%d')
        if i.comment_status == '0':
            i.comment_status = 'No'
        else:
            i.comment_status = 'Yes'
        m2m.append(i)

    pay = 0
    settings.TIME_ZONE  # 'UTC'
    now = datetime.datetime.now()
    now = make_aware(now)
    now.tzinfo  # <UTC>
    nowTuple = now.timetuple()
    month_ago = now + datetime.timedelta(days=-30) # 한달 전 시간
    nowTime = now + datetime.timedelta(days=1)  # 하루 뒤 시간

    month_order = order_tbl.objects.filter(order_date__range=[month_ago, nowTime])  # 30일전부터 오늘까지 (한달)

    to_order = order_tbl.objects.filter(order_date__year=nowTuple.tm_year,
                                        order_date__month=nowTuple.tm_mon,
                                        order_date__day=nowTuple.tm_mday) # 오늘의 총 주문 목록

    # 오늘의 주문 건수 및 가격 합산
    for order in to_order:
        pay += order.order_price # 오늘 주문 가격 합산

    cnt = to_order.count() # 오늘의 주문 갯수

    pay_fin = order_tbl.objects.filter(order_pay_status = '결제완료', order_date__year=nowTuple.tm_year,
                                                                 order_date__month=nowTuple.tm_mon,
                                                                 order_date__day=nowTuple.tm_mday) # 오늘의 결제완료 품목
    # 결제완료 금액 초기회
    fin_pay = 0

    # 오늘의 결제완료 금액 가격 합산
    for i in pay_fin:
        fin_pay += i.order_price

    fin_cnt = pay_fin.count() # 오늘의 결제완료 갯수

    pay_ref = order_tbl.objects.filter(order_status= '환불', order_date__year=nowTuple.tm_year,
                                                            order_date__month=nowTuple.tm_mon,
                                                            order_date__day=nowTuple.tm_mday) # 오늘의 환불 품목
    # 환불 금액 초기화
    ref_pay = 0

    # 오늘의 환불완료 금액 가격 합산
    for i in pay_ref:
        ref_pay += i.order_price

    ref_cnt = pay_ref.count()  # 오늘의 환불 갯수


    month_before_pay = month_order.filter(order_pay_status= '결제전').count()  # 한달내의 결제 전 항목
    month_ready_deli = month_order.filter(order_pay_status= '결제완료', order_status= '배송준비').count() # 한달내의 결제완료 후 배송준비 항목
    month_ing_deli = month_order.filter(order_status= '배송중').count() # 한달내의 배송중 항목
    month_cancel = month_order.filter(order_status= '취소').count() # 한달내의 취소 항목
    month_change = month_order.filter(order_status='교환').count()  # 한달내의 교환 항목
    month_refund = month_order.filter(order_status='환불').count()  # 한달내의 환불 항목


    content = {'cnt': cnt, 'pay': pay, 'fin_cnt': fin_cnt, 'fin_pay': fin_pay, 'ref_cnt': ref_cnt, 'ref_pay': ref_pay, 'm2m_list': m2m,
               'before_pay_mon': month_before_pay, 'ready_deli_mon': month_ready_deli, 'ing_deli_mon': month_ing_deli,
               'cancel_mon': month_cancel, 'change_mon': month_change, 'refund_mon': month_refund}

    return render(request, 'admin/index.html', content)

@login_required
def member_manage(request):

    # member_tbl 테이블의 모든 레코드를 불러온다
    search_list = member_tbl.objects.all()

    # search_option 을 option 에 저장
    option = request.GET.get('search_option')

    # search_key 를 search_key 에 저장
    search_key = request.GET.get('search_key')

    if option == 'rank':
        search_list = search_list.filter(member_rank__icontains=search_key)
    elif option == 'name':
        search_list = search_list.filter(member_name__icontains=search_key)
    elif option == 'userid':
        search_list = search_list.filter(member_id__icontains=search_key)
    elif option == 'email':
        search_list = search_list.filter(member_email__icontains=search_key)
    elif option == 'phone_number':
        search_list = search_list.filter(member_contact_number__icontains=search_key)
    elif option == 'reg_date':
        search_list = search_list.filter(member_join_date__icontains=search_key)
    else:
        search_list

    paginator = Paginator(search_list, 10)  # member_tbl 테이블의 모든 레코드를 페이지네이터에서 10개씩 저장한다.
    page = request.GET.get('page')  # request된 page를 저장한다
    search_list = paginator.get_page(page)  # request된 page의 레코드를 저장한다

    for a in search_list:
        a.member_join_date = a.member_join_date.strftime('%Y-%m-%d')

    return render(request, 'admin/member_manage.html',
                  {'search_list':search_list})

def member_update(request, id):
    # member_tbl 에 있는 데어터를 해당 id 를 통해서 info 에 저장
    info = member_tbl.objects.get(id=id)

    # member_rank 는 비어있으면 안돼기 때문에 'POST' 로 이용한다.
    # 'GET' 은 처음부터 비어있는 상태로 적용을 시키려 하기 때문에 오류가 난다.
    # 반면 'POST' 는 그렇지 않기 때문에 오류가 나지 않는다.
    if request.method == 'POST':
        info.member_rank = request.POST['rank_edit']
        info.save()

    info.member_join_date = info.member_join_date.strftime('%Y/%m/%d')
    return render(request, 'admin/member_update.html', {'info':info})

@login_required
def faq_manage(request):

    # m2mfaq_tbl 테이블의 모든 레코드를 불러온다
    faqs = m2mfaq_tbl.objects.all()

    # 비어있는 리스트를 생성
    names = []

    # 비어있는 리스트에 추가
    for i in faqs:
        names.append(member_tbl.objects.get(id=i.member_number_id).member_name)

    # m2mfaq_tbl 테이블의 모든 레코드를 페이지네이터에서 10개씩 저장한다.
    paginator = Paginator(faqs, 10)
    # request된 page를 저장한다
    page = request.GET.get('page')
    # request된 page의 레코드를 저장한다
    faqlists = paginator.get_page(page)

    # 문의목록에 있는 작성 날짜의 형식을 바꾼다
    for a in faqs:
        a.comment_write_date = a.comment_write_date.strftime('%Y-%m-%d')

    return render(request, 'admin/faq_manage.html',
                  {'faqs':faqs, 'faqlists':faqlists})

@login_required
def answer_window(request, id):

    # m2mfaq_tbl 에 있는 데이터를 id 를 통해서 question 에 저장
    question = m2mfaq_tbl.objects.get(id=id)

    # member_tbl 에 있는 데어터를 question 안에 있는
    #  member_number_id 를 통해서 user 에 저장
    user = member_tbl.objects.get(id=question.member_number_id)

    # request 의 method 가 POST 라면
    if request.method == 'POST':

        # reply_box 를 POST 로 reply 에 저장
        reply = request.POST['reply_box']

        try:
            # faq_answer_tbl 에 있는 question 이 저장된 comment_number 를
            # data 에 저장
            data = faq_answer_tbl.objects.get(comment_number=question)

            # reply 를 data 안에 있는 answer_description 에 저장
            data.answer_description = reply
            data.save() # reply 에 입력한 값을 data 에 저장

        except:
            # faq_answer_tbl 에 있는;
            # reply 를 answer_description 에 저장,
            # '관리자' 라는 이름으로 answer_writer 에 저장
            # question 을 comment_number 에 저장
            new_data = faq_answer_tbl(
                answer_description = reply,
                answer_writer = '관리자',
                comment_number = question
            )
            new_data.save() # 입력한 값을 new_data에 저장

            # 문의에 답변을 했을 경우
            # 답변 상태의 값을 0 에서 1 로 변경
            question.comment_status = 1
            question.save()

    try:
        answer = faq_answer_tbl.objects.get(comment_number=question)
    except:
        return render(request, 'admin/answer_window.html',
                      {'question': question, 'user': user})

    return render(request, 'admin/answer_window.html',
                  {'question': question, 'user': user, 'answer': answer})

def product_register(request):
    if request.method == 'POST':
        product_Price = request.POST['product_Price']
        product_made_date = request.POST['product_made_date']
        product_name = request.POST['product_name']
        product_image = request.FILES['product_image']
        product_description = request.POST['product_description']
        product_volume = request.POST['product_volume']
        product_stock = request.POST['product_stock']
        product_category = request.POST['product_category']
        product_size = request.POST.get('product_size', '')
        product_brand = request.POST['product_brand']
        product_manufacturer = request.POST['product_manufacturer']
        product_meterial = request.POST['product_meterial']
        product_made_country = request.POST['product_made_country']
        new_data = product_tbl(
            product_Price = product_Price,
            product_made_date = product_made_date,
            product_name = product_name,
            product_image = product_image,
            product_description = product_description,
            product_volume = product_volume,
            product_stock = product_stock,
            product_category = product_category,
            product_size = product_size,
            product_brand = product_brand,
            product_manufacturer = product_manufacturer,
            product_meterial = product_meterial,
            product_made_country = product_made_country,
        )

        print(new_data.save())
    return render(request, 'admin/product_register.html', {})

def product(request):
    try:
        category = request.GET['category']
        if category == '전체':
            product_list = product_tbl.objects.all()
        elif category == '주방용품':
            product_list = product_tbl.objects.filter(Q(product_category='냉장고') | Q(product_category='에어프라이어/튀김기'))
        elif category == '튀김':
            product_list = product_tbl.objects.filter(product_category='에어프라이어/튀김기')
        elif category == '냉장고':
            product_list = product_tbl.objects.filter(product_category='냉장고')
        elif category == '생활용품':
            product_list = product_tbl.objects.filter(product_category='에어컨/냉풍기')
        elif category == '에어컨':
            product_list = product_tbl.objects.filter(product_category='에어컨/냉풍기')
        elif category == '청소용품':
            product_list = product_tbl.objects.filter(Q(product_category='세탁기') | Q(product_category='청소기'))
        elif category == '세탁기':
            product_list = product_tbl.objects.filter(product_category='세탁기')
        elif category == '청소기':
            product_list = product_tbl.objects.filter(product_category='청소기')

    except:
        product_list = product_tbl.objects.all()
    context = {'product_list': product_list}
    return render(request, 'admin/product.html', context)

def product_delete(request, id):
    product = product_tbl.objects.get(id=id)
    product.delete()
    return redirect('/admin/product/')

def product_edit(request, id):
    product = product_tbl.objects.get(id=id)
    if request.method == 'POST':
        product.product_Price = request.POST['product_Price']
        product.product_stock = request.POST['product_stock']
        product.product_description = request.POST['product_description']
        product.save()
        return redirect('/admin/product/')
    return render(request, 'admin/product_edit.html', {'product': product})

def order_manage(request):
    now = datetime.datetime.now()
    nowTuple = now.timetuple()

    try:
        search = request.GET['search']
    except:
        search = None

    if search == 'deli':
        order_list = order_tbl.objects.filter(order_status='배송중')
    elif search == 'be_deli':
        order_list = order_tbl.objects.filter(order_status='배송준비')
    elif search == 'fi_deli':
        order_list = order_tbl.objects.filter(order_status='배송완료')
    elif search == 'cancel':
        order_list = order_tbl.objects.filter(order_status='취소')
    elif search == 'change':
        order_list = order_tbl.objects.filter(order_status='교환')
    elif search == 'refund':
        order_list = order_tbl.objects.filter(order_status='환불')
    elif search == '결제완료':
        order_list = order_tbl.objects.filter(order_pay_status='결제완료', order_date__year=nowTuple.tm_year,
                                                                        order_date__month=nowTuple.tm_mon,
                                                                        order_date__day=nowTuple.tm_mday)
    elif search == '환불':
        order_list = order_tbl.objects.filter(order_pay_status='환불', order_date__year=nowTuple.tm_year,
                                                                        order_date__month=nowTuple.tm_mon,
                                                                        order_date__day=nowTuple.tm_mday)
    elif search == 'today':
        order_list = order_tbl.objects.filter(order_date__year=nowTuple.tm_year,
                                              order_date__month=nowTuple.tm_mon,
                                              order_date__day=nowTuple.tm_mday)
    else:
        order_list = order_tbl.objects.all()

    context = {'order_list': order_list}
    return render(request, 'admin/order.html', context)

def order_detail(request, id):
    order = order_tbl.objects.get(id=id)
    if request.method == 'POST':
        order.order_pay_status = request.POST['order_pay_status']
        order.order_delivery_company = request.POST['order_delivery_company']
        order.order_transport_number = request.POST['order_transport_number']
        order.order_status = request.POST['order_status']

        order.save()
        return redirect('/admin/order/')
    return render(request, 'admin/order_detail.html', {'order':order})
# Create your views here.

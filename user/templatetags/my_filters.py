from django import template
import datetime

register = template.Library()

@register.filter(name='times') 
def times(number):
    return [n for n in range(number)]

@register.filter(name='get_age_group') 
def get_age_group(number):
    return (number+1) * 10 if number < 6 else f"{(number+1)*10}~"

@register.filter(name='get_exp_text') 
def get_exp_text(number):
    if number == 0:
        display_text = "초급(0~2년)"
    elif number == 1:
        display_text = "중급(3~7년)"
    else:
        display_text = "고급(7년이상)"
    return display_text

@register.filter(name='get_reason_text')
def get_reason_text(number):
    reasons = ['친목모임', '친환경', '건강관리', '취미활동', '탐험', '사진']
    return reasons[number]

@register.filter(name='intToStr')
def intToStr(id):
    return str(id)

@register.filter(name='get_category_title')
def get_category_title(category_key):
    this_month = datetime.datetime.now().month
    if this_month == 12: this_month = 0
    season = ['겨울', '봄', '여름', '가을']

    category_store = {
        'local_mountain': '주변 산 추천',
        'recommand_mountain': '좋아할 만한 산 추천',
        'season_mountain': f'{season[this_month//3]} 산 추천'
    }
    return category_store[category_key]

@register.filter(name='get_color_by_gender')
def get_color_by_gender(gender):
    return 'bg-primary' if gender == '남' else 'bg-danger'

@register.filter(name='get_my_reason_list')
def get_my_reason_list(reason):
    reason = reason[1:-1].replace('\'', '')
    return reason.split(',')

# 포스트 경과 시간 계산
@register.filter(name='elapsed_time')
def elapsed_time(post_time):
    elapsed_time = datetime.datetime.utcnow() - post_time.replace(tzinfo=None)

    m, s = divmod(elapsed_time.seconds, 60)
    h, m = divmod(m, 60)
    d = elapsed_time.days
    y, d = divmod(d, 365)

    if y > 0:
        elapsed_time = f'{y}년 전'
    elif y == 0 and d > 0:
        elapsed_time = f'{d}일 전'
    elif d == 0 and h > 0:
        elapsed_time = f'{h}시간 전'
    elif h == 0 and m > 0:
        elapsed_time = f'{m}분 전'
    else:
        elapsed_time = f'방금 전'

    return elapsed_time
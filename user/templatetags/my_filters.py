from django import template

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
    category_store = {
        'local_mountain': '내 주변 산 추천',
        'recommand_mountain': '어떤 산을 가볼까?'
    }
    return category_store[category_key]

@register.filter(name='get_color_by_gender')
def get_color_by_gender(gender):
    return 'bg-primary' if gender == '남' else 'bg-danger'

@register.filter(name='get_my_reason_list')
def get_my_reason_list(reason):
    reason = reason[1:-1].replace('\'', '')
    return reason.split(',')
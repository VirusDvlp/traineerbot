from jinja2 import Template


def get_coach_descr(coach: dict) -> str:
    temp = Template(
        '''{{coach["full_name"]}}\nСтаж работы - {{coach["exp"]}} лет\n
Специализация:
{% for spec in coach["specialization"].split(",") -%}
    {{spec}}
{% endfor -%}
''')
    return temp.render(coach=coach)
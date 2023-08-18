#coding=utf-8

from django.template import Library
import markdown

register = Library()

@register.filter
def md(value):

    return markdown.markdown(value, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',  # 语法高亮拓展
        'markdown.extensions.toc'  # 自动生成目录
    ])
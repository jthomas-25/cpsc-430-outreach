

from django import template

register = template.Library()

#@student.inclusion_tag("home_view.html") # need to add in an html file to pass in
def student(iterator):
    return {"iterator": iterator}
register.inclusion_tag('home_view.html')(student)

#@employer.inclusion_tag("home_view.html") # need to add in an html file to pass in
def employer(iterator):
    return {"iterator": iterator}
register.inclusion_tag('home_view.html')(employer)

#@admin.inclusion_tag("home_view.html") #need to add in an html file to pass in
def admin(iterator):
    return {"iterator": iterator}
register.inclusion_tag('home_view.html')(admin)
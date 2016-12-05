from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
	print(type(value))
	
	final = 0
	for i in arg:
		final = float(value)*float(i)

	return final
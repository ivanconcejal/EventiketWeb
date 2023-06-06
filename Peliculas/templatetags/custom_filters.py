from django import template

register = template.Library()

@register.filter
def get_by_fila_columna(butacas_info, fila_columna):
    fila, columna = fila_columna.split('_')
    for butaca_info in butacas_info:
        if butaca_info.fila == int(fila) and butaca_info.columna == int(columna):
            return butaca_info
    return None
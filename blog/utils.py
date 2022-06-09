import sys
import builtins
from pprint import pprint

from django.db.models.query import QuerySet
from django.db.models.manager import BaseManager

cyrillic_letters = {
    u'а': u'a',
    u'б': u'b',
    u'в': u'v',
    u'г': u'g',
    u'д': u'd',
    u'е': u'e',
    u'ё': u'e',
    u'ж': u'zh',
    u'з': u'z',
    u'и': u'i',
    u'й': u'i',
    u'к': u'k',
    u'л': u'l',
    u'м': u'm',
    u'н': u'n',
    u'о': u'o',
    u'п': u'p',
    u'р': u'r',
    u'с': u's',
    u'т': u't',
    u'у': u'u',
    u'ф': u'f',
    u'х': u'h',
    u'ц': u'ts',
    u'ч': u'ch',
    u'ш': u'sh',
    u'щ': u'sch',
    u'ь': u'',
    u'ы': u'y',
    u'ъ': u'',
    u'э': u'e',
    u'ю': u'u',
    u'я': u'ya',

}


def from_cyrilic_to_eng(text: str):
    text = text.replace(' ', '-').lower()
    result = ''
    for char in text:
        result += cyrillic_letters.get(char, char)
    return result


def get_object_or_null(model, **kwargs):
    if isinstance(model, QuerySet) or isinstance(model, BaseManager):
        return model.filter(**kwargs).first()
    return model.objects.filter(**kwargs).first()


# # for import
# from analizetools.analize import (
#     p_dir, p_mro, p_glob, p_loc, p_type,
#     delimetr, p_content, show_builtins, show_doc,
# )

# p_dir, p_mro, p_glob, p_loc, p_content, show_builtins, show_doc, delimiter


def p_dir(obj):
    return pprint(dir(obj))


def p_mro(obj):
    if isinstance(obj, type):
        return pprint(obj.mro())
    return pprint(type(obj).mro())


def p_glob():
    return pprint(globals())


def p_loc():
    return pprint(locals())


def p_content(obj):
    if hasattr(obj, '__iter__'):
        return pprint(obj)
    return pprint("Can't show elements of obj")


def show_builtins():
    # import builtins
    # pp(dir(builtins) == dir(globals()['__builtins__'])) # True
    # pp(builtins == globals()['__builtins__']) # True
    # pp(type(builtins)) # <class 'module'>
    # pp(type(builtins).mro()) # [<class 'module'>, <class 'object'>]
    key_builtins = globals().get('__builtins__')
    if key_builtins:
        if isinstance(key_builtins, dict):
            return pprint(key_builtins)
        return pprint(dir(key_builtins))
    else:
        return pprint("Can't show builtins")


def show_doc(obj):
    return print(obj.__doc__)


def delimiter(sym='-+', quant=50):
    return print('\n', sym * quant, end='\n')


# потом можно улучшить чтобы передавался также **kwargs, и тогда выводился
# также имя переменной и её значенте
# поможет setattr
def console(*args, delimetr='- ', length=50):
    print('\n', '=' * 100)
    for elem in args:
        print(elem)
        print(delimetr * length)
    print('=' * 100, '\n')


def p_type(obj):
    return print(type(obj))

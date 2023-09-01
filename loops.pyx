import re 
def contain_check(list l, str q)->bool:
    cdef str i
    for i in l:
        if i in q:
            return True
    return False
def refine(str ans)->str:
    return re.sub('a-zA-Z]+','',ans).replace(" ","").lower()

def escape_check(escape,support)->bool:
    for items in escape:
        if items in support:
            return False 
    return True
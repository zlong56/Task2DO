# for select input, before the query set, add extra value
# to show in the select option
a = [('10', 'Ali')]
context['obj_list'] = a + list(obj_list.values_list('pk','Name'))

# 


some_string = str(input('Input the string of a comma separated positive integers: '))
some_string = list(some_string.split(', '))
res_str = ''
for digit in some_string:
    res_str = res_str + str(digit)
res_int = int(res_str)
print(res_int)

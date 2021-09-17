a = int(input('Enter the start number of a column: '))
b = int(input('Enter the end number of a column: '))
c = int(input('Enter the start number of a string: '))
d = int(input('Enter the end number of a string: '))

numbers_list = [a for a in range(c, d + 1)]
list_column = [' ']
list_column.extend([a for a in range(a, b + 1)])
list_column.reverse()
for value_1 in range(a, b + 1):
    for value_2 in range(c, d + 1):
        numbers_list.append(value_1*value_2)
values_in_string = d - c + 1
print('Multiplication table:')
for k, value in enumerate(numbers_list):
    if k % values_in_string == 0:
        print('{:10}'.format(list_column.pop()), end='')
    print('{:10}'.format(value), end='\n' if (k + 1) % values_in_string == 0 else '')


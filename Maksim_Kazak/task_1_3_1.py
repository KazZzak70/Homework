from math import sqrt


def get_divisors(number):
    if number != 0:
        divisors_list = [1]
        for divisor in range(2, int(sqrt(number)) + 1):
            if number % divisor == 0:
                divisors_list.extend([divisor, int(number/divisor)])
        divisors_list.append(number)
        divisors_list.sort()
        return divisors_list


value = int(input('Input the number to find divisors: '))
print(get_divisors(value))

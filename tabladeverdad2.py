print('tabla de verdad con or')
booleanos = [True, False]
for x in booleanos:
    for y in booleanos:
        print('{}\t{}\t{}'.format(x, y, x or y))

print(' ')
print('tabla de verdad con and')

booleanos = [True, False]
for x in booleanos:
    for y in booleanos:
        print('{}\t{}\t{}'.format(x, y, x and y))

print(' ')
print('tabla de verdad con not')

booleanos = [True, False]
for x in booleanos:
    print('{}\t{}'.format(x, not x))


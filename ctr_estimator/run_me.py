__author__ = 'Jiahao Dong'

import console

print 'please one engine by input 1, 2 or 3:'
print '1.perform on ipinyou single set'
print '2.perform on ipinyou multi sets'
print '3.perform on MG set'

while True:
    flag = raw_input("Please enter 1, 2, or 3: ")
    try:
        {
            '1': console.perform_single_set,
            '2': console.perform_multi_set,
            '3': console.perform_mg,
        }[flag]()
        break
    except KeyError:
        print "Incorrect input"
#!/usr/bin/python
from random import randint

print 'Welcome to Math.  Press q to quit.'
score = 0
while True:
    a = randint(1, 100)
    b = randint(1, 100)
    yourAnswer = raw_input('What is ' + str(a) + ' x ' + str(b) + '?\n--> ')
    if yourAnswer == 'q':
        break
    elif yourAnswer == str(a * b):
        score += 20
        print 'You rock!  Total score: ' + str(score) + '\n'
    else:
        score -= 10
        print 'The correct answer was ' + str(a * b) + '\n'

print 'Good job!  Your score is ' + str(score)

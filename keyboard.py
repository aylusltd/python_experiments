import random
MIN = 1
MAX = 10
n = random.randrange(MIN,MAX,1)
n = int(n)
i=0
count=0

def set_i(n):
    try:
        i=int(n)
        return i
    except:
        print "Invalid input"
        return None

s = raw_input("I'm thinking of a random integer between " + str(MIN) + " and " + str(MAX) + ". Guess what it is. \n")
i = set_i(s)
count+=1
while i != n:
    if(i < n):
        # print str(i) + "<" + str(n)
        s=raw_input("My number is higher. Guess again. \n")
    if(i>n):
        # print str(i) + ">" + str(n)
        s=raw_input("My number is lower. Guess again. \n")
    i=set_i(s)
    count+=1

print "Congratulations, I was thinking of " + str(i) + "."
if count > 1:
    print "You guessed it in " + str(count)+ " guesses."
else:
    print "You got it in 1. You must be psychic."

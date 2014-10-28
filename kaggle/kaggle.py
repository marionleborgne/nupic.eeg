__author__ = 'marion'

"""quick answer to the stupid kaggle spam question..."""

NB = 966
MULTIPLES = [3,5]

multiples = set()
for m in MULTIPLES:
    for n in range(0, NB):
        if n % m == 0:
            multiples.add(n)

sum = sum(multiples)
print "spam answer : %s" % sum

import random

def ant(latest=0, _cur_steps=0):
   if latest == 0:
       latest = 1
       _cur_steps += 1
       return ant(latest, _cur_steps)
   elif latest == 1:
       latest = random.choice([0, 1, 1, 2])
       _cur_steps += 1
       return ant(latest, _cur_steps)
   else:
       return _cur_steps

n = 10000
total = 0
for i in range(n):
   total += ant()

print(total/n)
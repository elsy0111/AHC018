f = open('seeds.txt', 'w')

k = 0
for i in range(100):
    f.write(str(i) + " 0 0 " + str(k) + "\n")

f.close()
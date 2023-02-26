import subprocess

f = open('score.txt', 'w')
f.close()

f = open('score_C.txt', 'w')
f.close()

for k in range(0,100,10):
    cmd = "cargo run --release --bin tester python3 main.py < in/" + str(k).zfill(4) + ".txt"  + " > out.txt"
    runcmd = subprocess.call(cmd.split(),shell = True)

#!----------------------------------------------------------
    cmd = "cargo run --release --bin tester python3 past.py < in/" + str(k).zfill(4) + ".txt"  + " > out.txt"
    runcmd = subprocess.call(cmd.split(),shell = True)

f = open("score.txt","r")
r = list(map(int,f.read().split("\n")[:-1]))
f.close()
f = open("score.txt","a")
if sum(r) > 0:
    f.write("diff : +" + str(sum(r)))
else:
    f.write("diff : " + str(sum(r)))
f.close()
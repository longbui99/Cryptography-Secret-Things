import sys
mb = 100


t = 2**20
MB = mb*t
a = int(MB/2915)
b = 1000
with open("./file.txt", "a") as file:
    t = ""
    for x in range(0,a):
        stri =""
        for x in range(0,b):
            stri += str(x)
        file.write(stri)
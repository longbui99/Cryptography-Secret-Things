
T = "TTATAGATCTCGTATTCTTTTATAGATCTCCTATTCTT"
S = "TCCTATTCTT"
length = len(S)
q = 3
CompareL = [("A",1),("C",2),("T",3),("G",4)]
listT  = []
listS = []
for x in T:
    
    for t in CompareL:
        if x == t[0]:
            listT.append(t[1])
            break
    
for x in S:
    for t in CompareL:
        if x == t[0]:
            listS.append(t[1])
            break

print("T = ")
for x in listT:
    print(x, end="")
print("\n S = ")
for x in listS:
    print(x, end="")
print("\n")
i = 0
while i < len(listT)-length:

    j = 0
    check = True
    if listT[i] == listS[j]:
        while j < len(listS):
            if listT[i+j] != listS[j]:
                check = False
            j = j+1
    if check:
        print(i, end=":\t")
    i = i +1
# coding: utf8
def multi(n):
    result=0
    print (("Tables de multiplication de 1 à "+str(n)).center(50,"-")+"\n")
    for i in range(1,n+1):
        for j in range(1,n+1):
            result=i*j
            print result,
        print "\n"
n=14
multi(n)

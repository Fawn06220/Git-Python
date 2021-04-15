def get_sum(a,b):
    liste_nb=[]

    if a<b:
        for i in range(a,b+1):
            liste_nb.append(i)
    else:
        for i in range(b,a+1):
            liste_nb.append(i)

    print(liste_nb)
    

    if a==b:
        return a
    else:
        somme=sum(liste_nb)

    return somme

get_sum(0,-1)

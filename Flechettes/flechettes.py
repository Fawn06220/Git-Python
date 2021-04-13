# coding: utf8

#Pour calculer les float lors de la division sous Python 2.x
#sous Python 3.x supprimer cet import
from __future__ import division
#nombre aléatoire 
import random
 
 
nb_lances=0
nb_touches=0
nb_draw=0
nb_mille=0
nb_out=0
X=0
Y=0
limite=int(input("nombre de tirs ?"))
 
while (nb_lances!=limite):
    #Precision des tirs et nombre de chiffres apres la virgule (e.g 1)
    X=round(random.uniform(0, 1.0), 1)
    Y=round(random.uniform(0, 1.0), 1)
 
    D=((X*X)+(Y*Y))

    if D==0: #Lances qui touchent le centre de la cible
        nb_mille+=1
        
    if D<=1: #Lances qui touchent la cible
        nb_touches+=1
        print (u"impact au point X : "+str(X)+" Y : "+str(Y))
 
    if D==1: #Lances qui touchent la limite
        nb_draw+=1
 
    if D>=1: #Lances qui ne touchent pas la cible
        nb_out+=1
 
    nb_lances+=1

#En pourcentage
frequence=float(nb_touches/nb_lances)*100 
 
print (u"\nLa fréquence du nombre d'impacts dans la cible est : "+str(frequence)+"%")
 
#Petit bonus d'affichage histoire de...
print  (u"\nlances : "+str(nb_lances),u"touche : "+str(nb_touches), u"draw : "+str(nb_draw),u"out : "+str(nb_out),u"dans le mille : "+str(nb_mille))

def split_the_bill(x):
    somme=0
    dict_final={}
    diff=[]
    
    for k,v in x.items():
        somme+=v #Somme
    keys_list=list(x.keys())#Liste keys dict
    values_list=list(x.values())#Liste values dict
    den=len(keys_list)#Denominateur
    part=somme/den#Part a payer pour chacun

    for i in values_list:
        diff.append(round(i-part,2))#On arrondit a 2 chiffres après la virgule

    dict_final=dict(zip(keys_list, diff))#Crée le dict de resultat
    return dict_final
        
split_the_bill({'A': 232.6, 'B': 141.6, 'C': -19.400000000000006, 'D': -131.4, 'E': -223.4})

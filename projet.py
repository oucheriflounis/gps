import csv
import tkinter as tk
from tkinter import *


def nom_sommet(dataframe):
    #renvoie la liste de tous les nom des sommets

    liste_nom = []
    for i in range(len(dataframe)):
        if 'nom_sommet' in dataframe[i]:
            liste_nom.append(dataframe[i]['nom_sommet'])
        liste_nom = list(set(liste_nom))
    return liste_nom


def num_sommet(dataframe):
    #renvoie la liste de tous les numeros des sommets

    liste_num = []
    for i in range(len(dataframe)):
        if 'num_sommet' in dataframe[i]:
            liste_num.append(dataframe[i]['num_sommet'])
    return liste_num



def num_stat(dataframe, nom_som):
    #d'apres le nom de la station il sort tous les numero de la station 
    liste_num_stat = []
    for i in range(len(dataframe)):
        if 'nom_sommet' in dataframe[i]:
            if dataframe[i]['nom_sommet'] == nom_som:
                liste_num_stat.append(dataframe[i]['num_sommet'])
    return liste_num_stat


def nom_stat(dataframe, num_som):
    #d'apres le numero de la station il sort le nom de la station 
    if 'nom_sommet' in dataframe[num_som]:
            nom_station = dataframe[num_som]['nom_sommet']
    return nom_station


def ligne(dataframe, num_som1,num_som2):
    #renvoie la ligne a suivre pour arriver au sommet 2 a partir du sommet 1

    l = ""
    for i in range(len(dataframe)):
        if dataframe[i]['num_sommet1'] == num_som1 and dataframe[i]['num_sommet2'] == num_som2 :
            l = dataframe[num_som1]['ligne']
    if l == "":
        for i in range(len(dataframe)):
            if dataframe[i]['num_sommet1'] == num_som2 and dataframe[i]['num_sommet2'] == num_som1:
                l = dataframe[num_som2]['ligne']
    
    return l
    

def alentoure(dataframe, num_sommet):
    #renvoie une liste de liste contenant le numero du sommet ,num_sommet1 , num_sommet2 et temps_en_s  (les detaile de l'arrete associer au sommet)

    liste_al = []
    for i in range(len(dataframe)):
        if dataframe[i]['num_sommet1'] == num_sommet or dataframe[i]['num_sommet2'] == num_sommet :
            liste_al.append([num_sommet ,dataframe[i]['num_sommet1'] ,dataframe[i]['num_sommet2'] ,dataframe[i]['temps_en_s']])
    return liste_al


def alentoure_graph(dataframe, num_sommet):
    #renvoie une liste de liste contenant le numero du sommet ,num_sommet1 , num_sommet2 et temps_en_s  (les detaile de l'arrete associer au sommet)

    liste_al = []
    for i in range(len(dataframe)):
        if dataframe[i]['num_sommet1'] == num_sommet or dataframe[i]['num_sommet2'] == num_sommet :
            liste_al.append([num_sommet ,dataframe[i]['num_sommet1'] ,dataframe[i]['num_sommet2']])
    return liste_al


def connexite(dico,s) :
    couleur=dict()
    for station in dico :couleur[station]='blanc'
    pere=dict()
    pere[s]=None
    couleur[s]='gris'
    pile=[s]
    while pile :
        u=pile[-1]
        R=[y for y in dico[u] if couleur[y]=='blanc']
        if R :
            station=R[0]
            couleur[station]='gris'
            pere[station]=u
            pile.append(station)
        else :
            pile.pop()
            couleur[u]='noir'
    if len(pere) == len(dico) :
        print (True)


def graphe_conex(dataframe):
    #renvoie un dictionaire de clé (numero de sommet) et comme valeur (un dictionaire de clé (le numero des sommets ateniable) et comme valeur( le temps entre les 2 en s))

    liste_num1 = []
    liste_stat = []
    dic = {}
    
    liste_nom = nom_sommet(dataframe)
    liste_nom = list(set(liste_nom))
    for nom in liste_nom:
        liste_num = num_stat(dataframe, nom)
        for num in liste_num :
            liste_num1.append(num)
    for num in liste_num1:
        liste = alentoure_graph(dataframe, num) 
        for stat in liste :
            liste_stat.append(stat)
    for i in range(len(liste_stat)):
        Valeur_base = []
        key = liste_stat[i][0]
        
        if liste_stat[i][1] == key:
            Valeur = liste_stat[i][2]
        elif liste_stat[i][2] == key:
            Valeur = liste_stat[i][1]
        
        Valeur_base.append(Valeur)
        nouveau = {key:Valeur_base}
        
        if key in dic.keys():
            dic[key].append(Valeur)
        else:
            dic.update(nouveau)


    connexite(dic,1)
    


def graphe(dataframe):
    #renvoie un dictionaire de clé (numero de sommet) et comme valeur (un dictionaire de clé (le numero des sommets ateniable) et comme valeur( le temps entre les 2 en s))

    liste_num1 = []
    liste_stat = []
    dic = {}
    
    liste_nom = nom_sommet(dataframe)
    liste_nom = list(set(liste_nom))
    for nom in liste_nom:
        liste_num = num_stat(dataframe, nom)
        for num in liste_num :
            liste_num1.append(num)
    for num in liste_num1:
        liste = alentoure(dataframe, num) 
        for stat in liste :
            liste_stat.append(stat)
    for i in range(len(liste_stat)):
        Valeur_base = {}
        key = liste_stat[i][0]
        
        if liste_stat[i][1] == key:
            Valeur = {liste_stat[i][2] : liste_stat[i][3]}
        elif liste_stat[i][2] == key:
            Valeur = {liste_stat[i][1] : liste_stat[i][3]}
        
        Valeur_base.update(Valeur)
        nouveau = {key:Valeur_base}
        
        if key in dic.keys():
            dic[key].update(Valeur)
        else:
            dic.update(nouveau)

        
    return dic


def dijsktra(dataframe ,dictio , s, fin):

    # trouve le plus court chemin entre 2 sommets 
    # s:sommet de debut , fin:le sommet de arriver 
    # et renvoie dic: un dictionaire de clé (la longueur du plus court chemin) et de valeur (une liste dans la quelle y a le sommet de depart et le sommet d'arriver) 
    # s_connu : la liste des sommet traverser 
    # u : le sommet d'arriver


    # initialisation 
    dic = {}
    infini = 10000000000000
    s_connu = {s :[0 , [s]]}
    s_inconnu = {k : [infini , ''] for k in dictio if k != s}
    for suivant in dictio[s]:
        s_inconnu[suivant] = [dictio[s][suivant],s]
    
    # recherche 

    while s_inconnu and any(s_inconnu[k][0] < infini for k in s_inconnu):
        u = min(s_inconnu,key = s_inconnu.get)
        longueur_u, precedent_u = s_inconnu[u]
        for v in dictio[u]:
            if v in s_inconnu:
                d = longueur_u + dictio[u][v]
                if d < s_inconnu[v][0]:
                    s_inconnu[v] = [d, u]
        s_connu[u] = [longueur_u, s_connu[precedent_u][1] + [u]]
        del s_inconnu[u]
        
        if u == fin :  
            dic = {longueur_u : [s_connu[u][1][0],u]}
            break
            
    return dic , s_connu, u 


process_list = []
_path = "./metro1.csv"
with open(_path, newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    for row in reader:
        num_somm = lambda a : int(a) if (a != '') else None 
        av ={
            'sommet': row[0],
            'num_sommet': num_somm(row[1]),
            'nom_sommet': row[2],
            'ligne': row[3],
            'arete': row[4],
            'num_sommet1': int(row[5]),
            'num_sommet2': int(row[6]),
            'temps_en_s' : int(row[7]),
        }
        ap = {'arete': row[4],'num_sommet1': int(row[5]),'num_sommet2': int(row[6]),'temps_en_s' : int(row[7])}
        if row[0] != '' :
            process_list.append(av)
        else:
            process_list.append(ap)



graphe_conex(process_list)


### interface

TXT_DEPART = None
TXT_ARRIVE = None


root = tk.Tk()
root.title(" metro itineraire ")
canvas = tk.Canvas(root, bg="white", width=1000, height=800)


label_depars = tk.Label(root, text="Gare de départ :", fg="Black", font=("Helvetica", 20))
label_arrive = tk.Label(root, text="Gare d'arrivé :", fg="Black", font=("Helvetica", 20))




def getEntry_dep(depart):
    global TXT_DEPART
    depart = v_1.get()
    TXT_DEPART = depart


def getEntry_arr(arriver):
    global TXT_ARRIVE
    arriver = v_2.get()
    TXT_ARRIVE = arriver


def fonc(dataframe ):
    global TXT_DEPART , TXT_ARRIVE
    
    dep = TXT_DEPART
    arr =TXT_ARRIVE
    if dep == arr :
        pass
    else:
        dic = {}
        debut = num_stat(process_list, dep)
        arriver = num_stat(process_list, arr)
        dico = graphe(process_list)
        for i in debut:
            for j in arriver:
                dic_temp, sans_interer_1, sans_interer_2 = dijsktra(process_list,dico , i, j)
                liste_dic_temp = list(dic_temp.keys())
                cle_dic_temp = liste_dic_temp[0]
                if cle_dic_temp in list(dic.keys()):
                    dic[cle_dic_temp].append(dic_temp.get(cle_dic_temp))
                    
                else:
                    dic.update(dic_temp)
                
        liste_18 = list(dic.keys())

        temps_min = min(liste_18)
        dysc ,dic_min ,u = dijsktra(process_list,dico , dic[temps_min][0], dic[temps_min][1])
    return affichage(process_list ,dic_min , u ,temps_min)


def affichage(dataframe ,dyco, u, longueur):
    # elle affiche le trajet pour l'utilisateur
    # en entrer :
    # dyco : un dictionaire de clé (la longueur du plus court chemin) et de valeur (une liste dans la quelle y a le sommet de depart et le sommet d'arriver)
    # u : sommet de fin
    # longueur : la longueur du plus cour chemin 

    TXT =""
    TXT += "le temps de trajet est de : {} min \n \n ".format(round(longueur/60, 2)) 
    for w in range(len(dyco[u][1])-1):
        lign = ligne(dataframe, dyco[u][1][w],dyco[u][1][w+1])
        if nom_stat(dataframe,dyco[u][1][w]) == nom_stat(dataframe,dyco[u][1][w+1]):
            TXT +="\n corespendance de la ligne {0}  avec la ligne {1} \n \n".format(lign,dataframe[dyco[u][1][w+1]]['ligne'])
        else:
            TXT +="vous partez de {0} jusqu'a {1} avec la ligne {2} \n".format(nom_stat(dataframe, dyco[u][1][w]), nom_stat(dataframe,dyco[u][1][w+1]), lign)
    TXT += "\n vous etes ariver a {} \n".format(nom_stat(dataframe,u))
    label_resultat.config(text = TXT)


def get_entry():
    global TXT_DEPART, TXT_ARRIVE
    TXT_DEPART = v_1.get()
    TXT_ARRIVE = v_2.get()
    fonc(process_list)



liste_2 = nom_sommet(process_list)
liste_2.sort(key=lambda x: x[0])

boutton_recherche = tk.Button(root, height=1, width=10, text="Chercher", command=get_entry)
boutton_recherche.grid(row=7, column=60)
label_resultat = tk.Label(root, height=10, width=10, text= 'itinéraire')


#
v_1 = StringVar()
v_1.set("Gare de depart")
deroule_dep = OptionMenu(root, v_1, *liste_2, command=getEntry_dep)
#
v_2 = StringVar()
v_2.set("Gare d'arrivée")
deroule_arr = OptionMenu(root, v_2, *liste_2, command=getEntry_arr)
#


##################### PLACEMENT ###########################
label_resultat.grid(row= 15, rowspan=100, column=0, columnspan=200)
label_resultat.place(x=100, y=200, width=800, height=750)
deroule_dep.grid(row = 5, column = 20)
deroule_arr.grid(row = 7, column = 20)

label_depars.grid(row=5, column=2)
label_arrive.grid(row=7, column=2)
boutton_recherche.grid(row=6, column=60)

canvas.grid(row=0, rowspan=200, column=0, columnspan=200)

root.mainloop()
# coding: utf8
import wx
from wx.lib.intctrl import IntCtrl
import time
from time import gmtime, strftime
import os
from os import getcwd
import wx.media
from os.path import *


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, None, id, u"Ranking Emul V0.1a par Fawn Le Sombre", wx.DefaultPosition, wx.Size(300, 200),style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX|wx.STAY_ON_TOP)

        #Panel pour affichage
        self.panel = wx.Panel(self, -1, size=wx.Size(300, 200))

        #On capture l'event de fermeture de l'app
        self.Bind(wx.EVT_CLOSE,self.on_close,self)       

        #Crée la barre d'état (en bas).
        self.CreerBarreEtat()

        self.affichage = Affichage(None, -1, None)
        
        #Score
        self.txtScoreBox = IntCtrl(self.panel,-1,size=(100,20),style=wx.TE_PROCESS_ENTER)
        self.txtScoreBox.SetHint(u"SCORE")
        self.Bind(wx.EVT_TEXT_ENTER,self.SendScore,self.txtScoreBox)

        #Nom
        self.txtNomBox = wx.TextCtrl(self.panel,-1,size=(100,20),style=wx.TE_PROCESS_ENTER)
        self.txtNomBox.SetHint(u"NOM")
        self.Bind(wx.EVT_TEXT_ENTER,self.SendScore,self.txtNomBox)
        
        #Bouton Init
        self.BtnInit = wx.Button(self.panel,-1,u"Réinitialiser ?")
        self.Bind(wx.EVT_BUTTON, self.InitScore, self.BtnInit)

        #Boutons Affichage
        self.BtnAffichage = wx.Button(self.panel,-1,u"Afficher Scores")
        self.Bind(wx.EVT_BUTTON, self.Affichage, self.BtnAffichage)
        
        #Sizer install
        gbox0 = wx.GridBagSizer(10,10)
        gbox0.SetEmptyCellSize((10,10))
        gbox0.Add(self.txtScoreBox,(1,0))
        gbox0.Add(self.txtNomBox,(0,0))
        gbox0.Add(self.BtnInit,(2,0))
        gbox0.Add(self.BtnAffichage,(2,1))
        
        #PIP
        box0 = wx.StaticBox(self.panel, -1, u"Rankemulator :")
        bsizer0 = wx.StaticBoxSizer(box0, wx.HORIZONTAL)
        sizerH0 = wx.BoxSizer(wx.VERTICAL)
        sizerH0.Add(gbox0, 0, wx.ALL|wx.CENTER, 10)
        bsizer0.Add(sizerH0, 1, wx.EXPAND, 0)

        #--------Ajustement du sizer----------
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(bsizer0, 0,wx.ALL|wx.EXPAND, 10)
        self.SetSizer(mainSizer)

    def Affichage(self,evt):
        self.affichage.Show(True)
        
    def Chrono(self):#Chronometre (date )
        stemps = time.strftime(u"%A %d/%m/%Y") #Definit le format voulu
        self.SetStatusText(stemps,1) #Affiche a droite.

    def CreerBarreEtat(self):#Creation de la barre d'etat du bas avec l'affichage de la date
        self.CreateStatusBar(2) #Cree une barre de statut (en bas) de deux parties.
        self.SetStatusWidths([-1,150]) #Definit la taille.
        self.Chrono()#Affiche.

    def InitScore(self,evt):
        i=0
        if exists(u"score.txt"):
            os.remove(u"score.txt")
            with open(u"score.txt",u"a") as texte:
                while i<5: #Definit le nombre de joueurs a classer ici 5
                    texte.write("joueur 0\n")
                    i+=1
        else:
            with open(u"score.txt",u"w") as texte:
                while i<5: #Definit le nombre de joueurs a classer ici 5
                    texte.write("joueur 0\n")
                    i+=1
                texte.close()
        evt.Skip()
        
    def SendScore(self,evt):
        score_entry=self.txtScoreBox.GetValue()
        nom_entry=self.txtNomBox.GetValue()
        compteur=0
        memo=[]
        dico = {} #On crée un dico pour stocker les entrées
        une_occurence=0 #Toujours la var pour catch juste la premiere occurence
        if score_entry and nom_entry !='': #On vérifie que l'on a bien reçu un score et un nom (à toi d'adapter d'ou tu les reçois)
            dico[nom_entry]=score_entry #On associe le score à la clé "nom"
            for cle,valeur in dico.items(): #On fait une boucle pour recuperer sous forme cle+u" "+str(valeur) (soit ex: pierre 123)
                scorenom=cle+u" "+str(valeur)
            #A partir de là on reprend le truc classique pour ecrire la premiere ocurence et remplacer la ligne dans "score.txt"
            with open(u"score.txt",u"r") as texte,open(u'nouveau_score.txt', u'w') as nouveau_texte:
                lignes = texte.readlines()
                for data in lignes:
                    if une_occurence==0:
                        score_propre=data.split(u' ')[-1].rstrip(u'\n')
                        if int(valeur)>int(score_propre):
                            del lignes[-1]#On efface la derniere ligne du fichier
                            i=0
                            nouveau_texte.write(scorenom+u'\n')
                            while i<len(lignes)-compteur:
                                    memo.append(lignes[compteur+i])
                                    i+=1
                            for values in memo:
                                    memo_propre=values.rstrip(u'\n')
                                    nouveau_texte.write(memo_propre+u'\n')
                            une_occurence=1
                        else:
                            compteur+=1#Marqueur du numero de ligne remplacée
                            nouveau_texte.write(data)
                            
            os.remove(u'score.txt')
            os.rename(u'nouveau_score.txt', u'score.txt')         
        evt.Skip()

    def on_close(self,evt):#On detruit tout :)
        self.Destroy()
        self.affichage.Destroy()

class Affichage(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, None, id, u"Affichage Ranking", wx.DefaultPosition, wx.Size(500, 450),style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX|wx.STAY_ON_TOP)

        #Panel pour affichage
        self.panel = wx.Panel(self, -1, size=wx.Size(500, 450))

        #On capture l'event de fermeture de l'app
        self.Bind(wx.EVT_CLOSE,self.on_close,self)

        #Musique Player
        self.player = wx.media.MediaCtrl(self.panel, szBackend=wx.media.MEDIABACKEND_WMP10)
        self.player.Load("zik.mp3")
        self.Bind(wx.media.EVT_MEDIA_LOADED,self.button_play,self.player)

        #Boutons musique
        self.buttonZik = wx.Button(self.panel,-1,u"Play/Pause")
        self.Bind(wx.EVT_BUTTON, self.button_play, self.buttonZik)

        self.buttonZikStop = wx.Button(self.panel
                                       ,-1,u"Stop")
        self.Bind(wx.EVT_BUTTON, self.button_stop, self.buttonZikStop)

        #Bouton affichage
        self.BtnAffich = wx.Button(self.panel,-1,u"Rafraichir Scores")
        self.Bind(wx.EVT_BUTTON, self.Affich, self.BtnAffich)

        #Widget affichage
        self.AffichTxt=wx.TextCtrl(self.panel,-1,size=(450,200),style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.AffichTxt.SetBackgroundColour(u'BLACK')
        self.AffichTxt.SetFont(wx.Font(12, wx.DEFAULT , wx.NORMAL, wx.NORMAL,False ))
        self.AffichTxt.SetForegroundColour(u"FOREST GREEN")

        #Sizer install
        gbox0 = wx.GridBagSizer(10,10)
        gbox0.SetEmptyCellSize((10,10))
        gbox0.Add(self.AffichTxt,(0,0))
        gbox0.Add(self.BtnAffich,(1,0))

        #Sizer zik
        gbox1 = wx.GridBagSizer(10,10)
        gbox1.SetEmptyCellSize((2,2))
        gbox1.Add(self.buttonZik,(0,0))
        gbox1.Add(self.buttonZikStop,(0,1))

        #Ranking
        box0 = wx.StaticBox(self.panel, -1, u"Top 5 Ranking :")
        bsizer0 = wx.StaticBoxSizer(box0, wx.HORIZONTAL)
        sizerH0 = wx.BoxSizer(wx.VERTICAL)
        sizerH0.Add(gbox0, 0, wx.ALL|wx.CENTER, 10)
        bsizer0.Add(sizerH0, 1, wx.EXPAND, 0)

        #Musique
        box1 = wx.StaticBox(self.panel, -1, u"Musique :")
        bsizer1 = wx.StaticBoxSizer(box1, wx.HORIZONTAL)
        sizerH1 = wx.BoxSizer(wx.VERTICAL)
        sizerH1.Add(gbox1, 0, wx.ALL|wx.CENTER, 10)
        bsizer1.Add(sizerH1, 1, wx.EXPAND, 0)

        #--------Ajustement du sizer----------
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(bsizer0, 0,wx.ALL|wx.EXPAND, 10)
        mainSizer.Add(bsizer1, 0,wx.ALL|wx.EXPAND, 10)
        self.SetSizer(mainSizer)

        #couleur bouton zik
        self.buttonZik.SetBackgroundColour(wx.GREEN)
        
    def button_play(self,evt):
        colorpause=self.buttonZik.GetBackgroundColour()
        if colorpause==(wx.GREEN):
            self.player.Pause()
            self.buttonZik.SetBackgroundColour("")
        else:#sinon on play
            self.player.Play()
            self.buttonZikStop.SetBackgroundColour("")
            self.buttonZik.SetBackgroundColour(wx.GREEN)
        evt.Skip()

    def button_stop(self,evt):
        self.buttonZikStop.SetBackgroundColour(wx.RED)
        self.buttonZik.SetBackgroundColour("")
        self.player.Stop()
        evt.Skip()
        
    def Affich(self,evt):
        self.AffichTxt.Clear()
        with open(u"score.txt",u"r") as texte:
            lignes=texte.readlines()
            for data in lignes:
                self.AffichTxt.WriteText(data)
        self.panel.Refresh()
    
    def on_close(self,evt):#On cache la fenetre
        try:
            self.player.Stop()
        except:
            pass
        finally:
            self.Hide()
        
class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, None)
        frame.Show(True)
        frame.Centre()
        return True
 
if __name__=='__main__':    
 
    app = MyApp(0)
    app.MainLoop()
        

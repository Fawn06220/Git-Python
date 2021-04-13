# coding: utf8
import wx
import time
from time import gmtime, strftime
import os
from os.path import *
from os import getcwd
import subprocess
import shlex
import wx.lib.agw.hyperlink as hl
import wx.media

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, None, id, "PYTHON Modules Installer V0.1b par Fawn Le Sombre", wx.DefaultPosition, wx.Size(500, 800),style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX|wx.STAY_ON_TOP)

        #Panel pour affichage
        self.panel = wx.Panel(self, -1, size=(500, 800))

        #On capture l'event de fermeture de l'app
        self.Bind(wx.EVT_CLOSE,self.on_close,self)
        
        #Deco
##        ImgDir = (getcwd()+"\\Fond_setup.jpg")
##        fond = wx.Image(ImgDir, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
##        self.panel = wx.StaticBitmap(self.panel, -1, fond)

        #Crée la barre d'état (en bas).
        self.CreerBarreEtat()

        #Musique Player
        self.player = wx.media.MediaCtrl(self.panel, szBackend=wx.media.MEDIABACKEND_WMP10)
        self.player.Load("zik.mp3")
        self.Bind(wx.media.EVT_MEDIA_LOADED,self.button_play,self.player)
        
        #Boutons
        self.PIP_install_verif = wx.Button(self.panel,-1,"Vérification Installation PIP")
        self.Bind(wx.EVT_BUTTON, self.PIPinstall_verif, self.PIP_install_verif)

        self.PIP_install = wx.Button(self.panel,-1,"Installer PIP")
        self.Bind(wx.EVT_BUTTON, self.PIPinstall, self.PIP_install)
        #On disable le bouton au cas ou il serait déjà installé
        self.PIP_install.Disable()

        self.MOD_uninstall = wx.Button(self.panel,-1,"Désinstaller ?")
        self.Bind(wx.EVT_BUTTON, self.MODuninstall, self.MOD_uninstall)
        self.MOD_uninstall.Disable()

        #Boutons musique
        self.buttonZik = wx.Button(self.panel,-1,"Play/Pause")
        self.Bind(wx.EVT_BUTTON, self.button_play, self.buttonZik)

        self.buttonZikStop = wx.Button(self.panel
                                       ,-1,"Stop")
        self.Bind(wx.EVT_BUTTON, self.button_stop, self.buttonZikStop)

        #widgets vides
        self.txtVideMemo = wx.StaticText(self.panel,-1,"")
        self.txtVideMemo.SetFont(wx.Font(18, wx.DEFAULT , wx.NORMAL, wx.NORMAL,False, "Impact" ))
        self.txtVideMemo.SetForegroundColour("RED")
        
        self.txtVidePIP = wx.StaticText(self.panel,-1,"")
        self.txtVidePIP.SetFont(wx.Font(10, wx.DEFAULT , wx.NORMAL, wx.NORMAL,False, "Impact" ))
        
        #widgets
        self.txtMod = wx.StaticText(self.panel,-1,"Module à installer :")
        
        self.txtBox = wx.TextCtrl(self.panel,-1,size=(300,20),style=wx.TE_PROCESS_ENTER)
        self.txtBox.SetHint("Entrez le nom du MODULE ici...")
        self.txtBox.Disable()
        self.Bind(wx.EVT_TEXT_ENTER,self.Get_Mod,self.txtBox)
        
        self.AffichTxt=wx.TextCtrl(self.panel,-1,size=(450,300),style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.AffichTxt.SetBackgroundColour('BLACK')
        self.AffichTxt.SetFont(wx.Font(10, wx.DEFAULT , wx.NORMAL, wx.NORMAL,False ))
        self.AffichTxt.SetForegroundColour("FOREST GREEN")

        self.txtMajPip = wx.StaticText(self.panel,-1,'Lien MaJ fichier "get-pip.py" :')

        self.LienPip = hl.HyperLinkCtrl(self.panel, wx.ID_ANY, 'Download "get-pip.py" ',URL="https://bootstrap.pypa.io/get-pip.py")
        self.LienPip.SetLinkCursor(wx.CURSOR_HAND)
        self.LienPip.SetUnderlines(False, False, True)
        self.LienPip.EnableRollover(True)
        self.LienPip.SetColours("BLUE", "ORANGE", "BLUE")
        self.LienPip.SetBold(True)
        self.LienPip.SetToolTip(wx.ToolTip('Lien pour télécharger ou mettre à jour "get-pip.py"'))
        self.LienPip.UpdateLink()
        
        #Sizer install
        gbox0 = wx.GridBagSizer(10,10)
        gbox0.SetEmptyCellSize((10,10))
        gbox0.Add(self.PIP_install_verif,(0,0))
        gbox0.Add(self.txtVidePIP,(0,1))
        gbox0.Add(self.PIP_install,(0,2))
        gbox0.Add(self.txtMajPip,(1,0))
        gbox0.Add(self.LienPip,(1,1))
        
        #Sizer gestion
        gbox1 = wx.GridBagSizer(10,10)
        gbox1.SetEmptyCellSize((2,2))
        gbox1.Add(self.txtMod,(0,0))
        gbox1.Add(self.txtBox,(0,1))
        gbox1.Add(self.txtVideMemo,(1,1))
        gbox1.Add(self.MOD_uninstall,(2,1))

        #Sizer affichage
        gbox2 = wx.GridBagSizer(10,10)
        gbox2.SetEmptyCellSize((10,10))
        gbox2.Add(self.AffichTxt,(0,0))

        #Sizer zik
        gbox3 = wx.GridBagSizer(10,10)
        gbox3.SetEmptyCellSize((10,10))
        gbox3.Add(self.buttonZik,(0,0))
        gbox3.Add(self.buttonZikStop,(0,1))
        
        #PIP
        box0 = wx.StaticBox(self.panel, -1, "Installation PIP :")
        bsizer0 = wx.StaticBoxSizer(box0, wx.HORIZONTAL)
        sizerH0 = wx.BoxSizer(wx.VERTICAL)
        sizerH0.Add(gbox0, 0, wx.ALL|wx.CENTER, 10)
        bsizer0.Add(sizerH0, 1, wx.EXPAND, 0)
        
        #Modules
        box1 = wx.StaticBox(self.panel, -1, "Gestion des modules :")
        bsizer1 = wx.StaticBoxSizer(box1, wx.HORIZONTAL)
        sizerH1 = wx.BoxSizer(wx.VERTICAL)
        sizerH1.Add(gbox1, 0, wx.ALL|wx.CENTER, 10)
        bsizer1.Add(sizerH1, 1, wx.EXPAND, 0)

        #Affichage
        box2 = wx.StaticBox(self.panel, -1, "Affichage :")
        bsizer2 = wx.StaticBoxSizer(box2, wx.HORIZONTAL)
        sizerH2 = wx.BoxSizer(wx.VERTICAL)
        sizerH2.Add(gbox2, 0, wx.ALL|wx.CENTER, 10)
        bsizer2.Add(sizerH2, 1, wx.EXPAND, 0)

        #Zik
        box3 = wx.StaticBox(self.panel, -1, "Musique :")
        bsizer3 = wx.StaticBoxSizer(box3, wx.HORIZONTAL)
        sizerH3 = wx.BoxSizer(wx.VERTICAL)
        sizerH3.Add(gbox3, 0, wx.ALL|wx.CENTER, 10)
        bsizer3.Add(sizerH3, 1, wx.EXPAND, 0)

        #--------Ajustement du sizer----------
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(bsizer0, 0,wx.ALL|wx.EXPAND, 10)
        mainSizer.Add(bsizer1, 0,wx.ALL|wx.EXPAND, 10)
        mainSizer.Add(bsizer2, 0,wx.ALL|wx.EXPAND, 10)
        mainSizer.Add(bsizer3, 0,wx.ALL|wx.EXPAND, 10)
        self.SetSizer(mainSizer)

        #Préparation des dossiers et fichiers de configuration
        self.Check_up()

        #On check si PIP a été installé
        self.Check_pip()

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
    
    def Check_pip(self):
        global DirPip
        with open(DirPip,"r") as check:
            data=check.read()
            if data=="0":
                pass
            else:
                with open(DirPip,"w") as pip_ok:
                    pip_ok.write("1")
                self.PIP_install.Disable()
                self.PIP_install_verif.Disable()
                self.txtVidePIP.SetLabel('PIP est installé !')
                self.txtVidePIP.SetForegroundColour("FOREST GREEN")
                self.txtBox.Enable()

    def Check_up(self):
        global RepConf
        RepConf=getcwd()+"\\config"
        #Vérification des répertoires 
        if exists(RepConf): #Verifie que le répertoire "config" existe.
            self.Check_files() 
        else : #Sinon
            os.mkdir(RepConf) #Crée le repertoire "batch" s'il n'existe pas.
            self.Check_files()

    def Check_files(self):
        global RepConf,DirPip,DirMemo
        DirMemo=RepConf+"\\memo.txt"
        DirPip=RepConf+"\\pip.txt"
        if exists(DirMemo):
            pass
        else:
            with open(DirMemo,"w") as create_memo:
                create_memo.close()
        if exists(DirPip):
            pass
        else:
            with open(DirPip,"w") as create_pip:
                create_pip.write("0")
                
        
    def PIPinstall(self,evt):
        out=0
        err=0
        self.AffichTxt.Clear()
        process = subprocess.Popen(shlex.split('python get-pip.py'), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            error= process.stderr.readline()
            if (output=='' and error=='') and process.poll() is not None:
                if out==1:
                    self.PIP_install_out()
                if err==1:
                    self.PIP_install_err()
                break
            if output:
                out_propre= output.strip()
                out_propre=out_propre.decode('cp850','ignore')#On decode l'entrée envoyée par cmd.exe
                self.AffichTxt.SetForegroundColour("FOREST GREEN")
                self.AffichTxt.AppendText(out_propre + "\n")
                out=1
                #print out_propre
            elif error:
                error_propre= error.strip()
                error_propre=error_propre.decode('cp850','ignore')#On decode l'entrée envoyée par cmd.exe
                self.AffichTxt.SetForegroundColour("RED")
                self.AffichTxt.AppendText(error_propre + "\n")
                err=1
        process.poll()
                #print error_propre
        evt.Skip()
        
    def PIP_install_out(self):
        global DirPip
        with open(DirPip,"w") as pip_ok:
            pip_ok.write("1")
        self.txtVidePIP.SetLabel('PIP est installé !')
        self.txtVidePIP.SetForegroundColour("FOREST GREEN")
        self.PIP_install.Disable()
        self.txtBox.Enable()
        
    def PIP_install_err(self):
        self.txtVidePIP.SetLabel('Erreur PIP install !')
        self.txtVidePIP.SetForegroundColour("RED")
        
    def PIPinstall_verif(self,evt):
        out=0
        err=0
        self.AffichTxt.Clear()
        process = subprocess.Popen(shlex.split('python -m pip -V'), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            error= process.stderr.readline()
            if (output=='' and error=='') and process.poll() is not None:
                if out==1:
                    self.PIP_verif_out()
                if err==1:
                    self.PIP_verif_err()
                break
            if output:
                out_propre= output.strip()
                out_propre=out_propre.decode('cp850','ignore')#On decode l'entrée envoyée par cmd.exe
                self.AffichTxt.SetForegroundColour("FOREST GREEN")
                self.AffichTxt.AppendText(out_propre + "\n")
                out=1
                #print out_propre
            elif error:
                error_propre= error.strip()
                error_propre=error_propre.decode('cp850','ignore')#On decode l'entrée envoyée par cmd.exe
                self.AffichTxt.SetForegroundColour("RED")
                self.AffichTxt.AppendText(error_propre + "\n")
                err=1
                #print error_propre
        process.poll()
        evt.Skip()
        
    def PIP_verif_err(self):
        self.txtVidePIP.SetLabel('PIP non installé !')
        self.txtVidePIP.SetForegroundColour("RED")
        self.PIP_install.Enable()
        self.PIP_install_verif.Disable()
        
    def PIP_verif_out(self):
        global RepConf,DirPip
        with open(DirPip,"w") as pip_ok:
            pip_ok.write("1")
        self.txtVidePIP.SetLabel('PIP est installé !')
        self.txtVidePIP.SetForegroundColour("FOREST GREEN")
        self.PIP_install_verif.Disable()
        self.txtBox.Enable()
                
    def Get_Mod(self,evt):
        global mod_to_install,exception
        out=0
        err=0
        exception=0
        self.AffichTxt.Clear()
        mod_to_install=self.txtBox.GetValue()
        process = subprocess.Popen(shlex.split('python -m pip install '+mod_to_install), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            error= process.stderr.readline()
            if (output=='' and error=='') and process.poll() is not None:
                if out==1:
                    self.MOD_out()
                if err==1:
                    self.MOD_err()
                break
            if output:
                out_propre= output.strip()
                out_propre=out_propre.decode('cp850','ignore')#On decode l'entrée envoyée par cmd.exe
                self.AffichTxt.SetForegroundColour("FOREST GREEN")
                self.AffichTxt.AppendText(out_propre + "\n")
                txt_except="Requirement already satisfied: "+mod_to_install
                if txt_except in out_propre:
                    exception=1    
                out=1
            elif error:
                error_propre= error.strip()
                error_propre=error_propre.decode('cp850','ignore')#On decode l'entrée envoyée par cmd.exe
                self.AffichTxt.SetForegroundColour("RED")
                self.AffichTxt.AppendText(error_propre + "\n")
                err=1
        process.poll()
        evt.Skip()
        
    def MOD_out(self):
        global DirMemo,mod_to_install,exception
        present=0
        self.txtVideMemo.SetLabel("")
        with open(DirMemo,"r") as memo:
            lignes = memo.readlines()
            for ligne in lignes:
                elem=ligne.rstrip('\n')
                if mod_to_install in elem:
                    present=1
        if present==1 or exception==1:
            self.txtVideMemo.SetForegroundColour("RED")
            self.txtVideMemo.SetLabel("Module déjà installé !")
            self.MOD_uninstall.Enable()
            if present==0 and exception==1:
                with open(DirMemo,"a") as memo:
                    memo.write(mod_to_install+"\n")
        else:
            with open(DirMemo,"a") as memo:
                memo.write(mod_to_install+"\n")
            self.txtVideMemo.SetLabel("Le module a bien été installé !")
            self.txtVideMemo.SetForegroundColour("FOREST GREEN")
                
    def MOD_err(self):
        global DirMemo
        self.txtVideMemo.SetLabel("")
        self.AffichTxt.SetForegroundColour("RED")
        self.AffichTxt.SetLabel("Le module n'existe pas ! >o<")
        ###Hack pour mauvais nom de module#####
        with open(DirMemo,"r") as memo:
            lines=memo.readlines()
            if len(lines) > 0:
                del lines[-1]
                file(DirMemo, 'w').writelines(lines)

    def MODuninstall(self,evt):
        global mod_to_uninstall
        out=0
        err=0
        self.AffichTxt.Clear()
        mod_to_uninstall=self.txtBox.GetValue()
        process = subprocess.Popen(shlex.split('python -m pip uninstall -y '+mod_to_uninstall), stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if output=='' and process.poll() is not None:
                if out==1:
                    self.MOD_uninstall_out()
                break
            if output:
                out_propre= output.strip()
                out_propre=out_propre.decode('cp850','ignore')#On decode l'entrée envoyée par cmd.exe
                self.AffichTxt.SetForegroundColour("FOREST GREEN")
                self.AffichTxt.AppendText(out_propre + "\n")
                out=1
        process.poll()
        evt.Skip()

    def MOD_uninstall_out(self):
        global DirMemo,mod_to_uninstall
        self.txtVideMemo.SetLabel("")
        with open(DirMemo, 'r') as texte, open('nouveau_texte.txt', 'w') as nouveau_texte:
            for line in texte:
                if mod_to_uninstall in line:
                    nouveau_texte.write('')
                else:
                    nouveau_texte.write(line)
        os.remove(DirMemo)
        os.rename('nouveau_texte.txt', DirMemo)
        self.txtVideMemo.SetLabel("Le module a bien été désinstallé !")
        self.txtVideMemo.SetForegroundColour("FOREST GREEN")
        self.MOD_uninstall.Disable()
    
    def Chrono(self):#Chronometre (date )
        stemps = time.strftime("%A %d/%m/%Y") #Definit le format voulu
        self.SetStatusText(stemps,1) #Affiche a droite.
    
    def CreerBarreEtat(self):#Creation de la barre d'etat du bas avec l'affichage de la date
        self.CreateStatusBar(2) #Cree une barre de statut (en bas) de deux parties.
        self.SetStatusWidths([-1,150]) #Definit la taille.
        self.Chrono()#Affiche.

    def on_close(self,evt):#On detruit tout :)
        try:
            self.player.Stop()
        except:
            pass
        finally:
            self.Destroy()
        
        

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, None)
        frame.Show(True)
        frame.Centre()
        return True
 
if __name__=='__main__':    
 
    app = MyApp(0)
    app.MainLoop()

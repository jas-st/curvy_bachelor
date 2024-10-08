# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 01:56:33 2019

@author: Home
"""

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import numpy as np
import sympy as sp
import tkinter.ttk as ttk
from random import choice, randint 


class P(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self,master)
        self.createGraph()
        self.Eingabe()
        self.k=0
    
    def Achsen(self,fig):
        ax = fig.gca()
        ax.spines["right"].set_color("none")
        ax.spines["top"].set_color("none")
        ax.spines["left"].set_position(("data",0))
        ax.spines["bottom"].set_position(("data",0))
        ax.xaxis.set_ticks_position("bottom")
        ax.yaxis.set_ticks_position("left")    
        
    
    def createGraph(self):               
        fig = Figure(figsize = (9, 6), facecolor = "white")
        axis = fig.add_subplot(111)
        
        canvas = FigureCanvasTkAgg(fig, master = root)
        canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = 1)
        
        axis.grid()
        
        style = ttk.Style()
        style.configure("spiel.TButton", font = ("Calibri Light", 12), foreground = "gray30")
        style.configure("normal.TButton", font = ("Calibri Light", 12), foreground = "gray30")
        
        self.plotbutton1 = ttk.Button(master = root, text="Zeichnen", style = "normal.TButton", command = lambda: self.Plotter(canvas,axis,fig))
        self.plotbutton2 = ttk.Button(master = root, text="Nullstelle", style = "normal.TButton", command = lambda: self.Nullstellen(canvas,axis,fig))
        self.plotbutton3 = ttk.Button(master = root, text="Extremstellen", style = "normal.TButton", command = lambda: self.Extremstellen(canvas,axis,fig))
        self.plotbutton4 = ttk.Button(master = root, text="Ableitung", style = "normal.TButton", command = lambda: self.Ableitung(canvas,axis,fig))
        self.plotbutton5 = ttk.Button(master = root, text="Spiel", style = "spiel.TButton", command = lambda: self.Spiel(root))
        self.plotbutton1.pack(padx = 10, pady = 10, side = tk.RIGHT)
        self.plotbutton5.pack(padx = 5, pady = 10, side = tk.LEFT)
        self.plotbutton2.pack(padx = 5, pady = 10, side = tk.LEFT)
        self.plotbutton3.pack(padx = 5, pady = 10, side = tk.LEFT)
        self.plotbutton4.pack(padx = 5, pady = 10, side = tk.LEFT)
        
    
    def Eingabe(self):
        self.E1 = tk.Entry(root)
        self.E1.pack(padx = 80, pady = 16)
        return self.E1
    
    
    def Spiel(self,root):
        spiel = tk.Toplevel(root, width=90)  
        
               
        def Funktion_Generator():
            
            fig = Figure(figsize = (9, 6))
            axs = fig.subplots(2,3, gridspec_kw = {"hspace": 1})
            
            axs[0,0].remove()
            axs[0,2].remove()
            
            xx = np.linspace(-5,5,1000)
            x = sp.symbols("x")
            funktionen_liste = [sp.sin(x), sp.cos(x),
                                choice([-1,1])*randint(1,8)*x**2+randint(-8,8)*x+randint(-8,8),
                                choice([-1,1])*randint(1,8)*x**3+randint(-8,8)*x**2+randint(-8,8)*x+randint(-8,8), 
                                choice([-1,1])*randint(1,8)*x**4+randint(-8,8)*x**2+randint(-8,8)*x+randint(-8,8),
                                choice([-1,1])*randint(1,8)*x**4+randint(-8,8)*x**3+randint(-8,8)*x+randint(-8,8),
                                sp.exp(x), choice([-1,1])*randint(1,8)*sp.sqrt(x)
                                ]
            
            #die erste random-gewählte funktion
            y_1 = choice(funktionen_liste)
            #ihre ableitung
            y1_ablt_richtig = y_1.diff(x)
            
            #die zweite funktion
            y_2 = choice(funktionen_liste)
            #sicherstellen dass die zweite und die erste verschieden sind            
            while str(y_2) == str(y_1):
                y_2 = choice(funktionen_liste)
            #ihre ableitung
            y2_ablt = y_2.diff(x)
            
            #die dritte funktion
            y_3 = choice(funktionen_liste)            
            while str(y_3) == str(y_2) or str(y_3) == str(y_1):
                y_3 = choice(funktionen_liste)   
            #ihre ableitung                     
            y3_ablt = y_3.diff(x)
            
            #numerisch speichern
            #die funktion, deren ableitung wir suchen
            y1 = sp.lambdify(x, y_1)(xx)
            #die drei mögliche choices
            y2 = sp.lambdify(x, y2_ablt)(xx)
            y3 = sp.lambdify(x, y3_ablt)(xx)
            richtig = sp.lambdify(x, y1_ablt_richtig)(xx)
            
            a = [y2,y3,richtig]
            uno = choice(a)
            due = choice(a)            
            while str(due) == str(uno):
                due = choice(a)                
            tre = choice(a)            
            while str(tre) == str(uno) or str(tre) == str(due):
                tre = choice(a) 
            
            #die hauptfunktion plotten                        
            axs[0,1].plot(xx, np.transpose(y1))
            axs[0,1].set_title(y_1)
            
            #die erste choice
            axs[1,0].plot(xx, np.transpose(uno))
            #der richtige name setzen
            if str(uno) == str(y2):
                axs[1,0].set_title(y2_ablt)
            elif str(uno) == str(y3):
                axs[1,0].set_title(y3_ablt)
            else:
                axs[1,0].set_title(y1_ablt_richtig)
             
            #die zweite choice
            axs[1,1].plot(xx,np.transpose(due))           
            if str(due) == str(y2):
                axs[1,1].set_title(y2_ablt)
            elif str(due) == str(y3):
                axs[1,1].set_title(y3_ablt)
            else:
                axs[1,1].set_title(y1_ablt_richtig)
             
            #die dritte choice   
            axs[1,2].plot(xx, np.transpose(tre))           
            if str(tre) == str(y2):
                axs[1,2].set_title(y2_ablt)
            elif str(tre) == str(y3):
                axs[1,2].set_title(y3_ablt)
            else:
                axs[1,2].set_title(y1_ablt_richtig)
                
                
            canvas = FigureCanvasTkAgg(fig, spiel)
            canvas._tkcanvas.grid(row=1, columnspan=3)
                                   
            def selected():               
                if v.get()==str(y1_ablt_richtig):                        
                    ab=tk.Text(spiel, height=1, width=20,background="DarkOliveGreen3")                   
                    ab.grid(row=3,column=1)
                    ab.insert(tk.END,"Richtig".center(20))
                                       
                else: 
                    ab=tk.Text(spiel, height=1, width=20,background="red")                   
                    ab.grid(row=3,column=1)
                    ab.insert(tk.END,"Bäääh! Falsch!!".center(20))
                        
            def counter():               
                if v.get()==str(y1_ablt_richtig): 
                   self.k+=1
                   textbox=tk.Text(spiel, height=1,width=10)
                   textbox.grid(row=0,column=2)                  
                   textbox.insert(tk.END, str(self.k) + " richtig")
                else:
                   textbox=tk.Text(spiel, height=1,width=10)
                   textbox.grid(row=0,column=2)                  
                   textbox.insert(tk.END, str(self.k)+ " richtig")
                                                            
            def counter_selected():
                selected()
                counter()
            
            namen = [y1_ablt_richtig,y2_ablt,y3_ablt]
            one = choice(namen)
            
            two = choice(namen)            
            while str(two) == str(one):
                two = choice(namen)
                           
            three = choice(namen)            
            while str(three) == str(one) or str(three) == str(two):
                three = choice(namen)   
                                      
            v = tk.StringVar()
                        
            c1=tk.Radiobutton(spiel, text = str(one).ljust(50), variable = v, value = one, command = counter_selected)            
            c2=tk.Radiobutton(spiel, text = str(two).ljust(50), variable = v, value = two, command = counter_selected)            
            c3=tk.Radiobutton(spiel, text = str(three).ljust(50), variable = v, value = three, command = counter_selected )

            c1.grid(row = 2,column = 0, sticky=tk.W)
            c2.grid(row = 2,column = 1, sticky=tk.W)
            c3.grid(row = 2,column = 2, sticky=tk.W)
                           
                              
        def btnchange():
            btn_t.set("weiter")
            
        def btnchange_FGenerator():
            btnchange()
            Funktion_Generator()
            
        btn_t = tk.StringVar()    
        B1 = tk.Button(spiel, textvariable = btn_t, command = btnchange_FGenerator)
        btn_t.set("Los!".center(40))
        B1.grid(row=0,column=1)
             
    
    def Plotter(self,canvas,axis,fig):
        x = sp.symbols("x")
        funktion = sp.sympify(self.E1.get())
    
        axis.clear()
        self.Achsen(fig)
           
        xx = np.linspace(-10,10,1000)
        yy = sp.lambdify(x,[funktion])(xx)
        
        axis.plot(xx,np.transpose(yy))
        axis.grid()
        
        canvas.draw()
        
    
    def Nullstellen(self,canvas,axis,fig):
        x = sp.symbols("x")
        funktion = sp.sympify(self.E1.get())    
        
        axis.clear()
        self.Achsen(fig)
        
        xx = np.linspace(-10,10,1000)
        yy = sp.lambdify(x,[funktion])(xx)
        axis.plot(xx,np.transpose(yy))
        axis.grid()
        
        if "sin" or "cos" in self.E1.get():            
            zeroPoints = list(sp.solve(funktion,x))           
        else:
            zeroPoints= list(sp.solveset(funktion,x))
            
            
        zeroPointsY=[funktion.subs(x,a)for a in zeroPoints]
        ###liste mit nullpunkten
        zeroPointsF=[]
        for el in zeroPoints:
            x=float(el)
            zeroPointsF.append(round(x,2))
        zeroPointsYF=[]
        for el in zeroPointsY:
            x=float(el)
            zeroPointsYF.append(round(x,2))
            
        a=list(zip(zeroPointsF, zeroPointsYF))
        
       
        ###nullpunkte zeichnen
        axis.plot(zeroPointsF,zeroPointsYF,"bo")
        ###textfeld mit nullstellen               
        if "sin" in self.E1.get():            
            textstr="Diese Funktion hat unendlich viele Nullstellen. \n Zwei davon liegen bei:"   
        elif "cos" in self.E1.get() :
            textstr="Diese Funktion hat unendlich viele Nullstellen. \n Zwei davon liegen bei:"
        else:
            textstr="Die Nullstellen von dieser Funktion liegen bei "   
            
        for el in a:
            textstr+=str(el)+" "
            
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        axis.text(0.05, 0.95, textstr, transform=axis.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        
        with open ("daten.txt","a+") as d:            
             d.write(str(self.E1.get())+": " + textstr + "\n")
        
    
        canvas.draw()   
        
        
    def Extremstellen(self,canvas,axis,fig):
        x = sp.symbols("x")
        funktion = sp.sympify(self.E1.get())

        axis.clear()
        self.Achsen(fig)

        xx = np.linspace(-10,10,1000)
        yy = sp.lambdify(x,[funktion])(xx)
        axis.plot(xx,np.transpose(yy))
        axis.grid()

        ersteAbl = funktion.diff(x)
        
        
        
        
        if "sin" or "cos"  in self.E1.get():            
            extremStellen = list(sp.solve(ersteAbl,x))
        else:
            extremStellen=list(sp.solveset(ersteAbl,x))
            
        extremstellenY = [funktion.subs(x, a) for a in extremStellen]
        
        
        
        ###liste mit extremstellen
        extremstellenF=[]
        for el in extremStellen:
            x=float(el)
            extremstellenF.append(round(x,2))
        extremstellenYF=[]
        for el in extremstellenY:
            x=float(el)
            extremstellenYF.append(round(x,2))
        a=list(zip(extremstellenF, extremstellenYF))
        ###extremstellen zeichnen
        axis.plot(extremStellen,extremstellenY,"k*")
        ###textfeld mit extremstellen
        if "sin" in self.E1.get():            
            textstr="Diese Funktion hat unendlich viele Extremstellen. \n Zwei davon liegen bei:"   
        elif "cos" in self.E1.get() :
            textstr="Diese Funktion hat unendlich viele Extremstellen. \n Zwei davon liegen bei:"
        else:
            textstr="Die Extremstellen von dieser Funktion liegen bei "
        for el in a:
            textstr+=str(el)+" "
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        axis.text(0.05, 0.95, textstr, transform=axis.transAxes, fontsize=14, verticalalignment='top', bbox=props)

        with open ("daten.txt","a+") as d:            
             d.write(str(self.E1.get())+": " + textstr + "\n")

        canvas.draw()

    def Ableitung(self,canvas,axis,fig):
        x = sp.symbols("x")
        funktion = sp.sympify(self.E1.get())

        axis.clear()
        self.Achsen(fig)
        
        ersteAbl = funktion.diff(x)
            
        xx = np.linspace(-10,10,1000)
        yy = sp.lambdify(x,[funktion, ersteAbl])(xx)
        axis.plot(xx,np.transpose(yy))
        axis.grid()
            
        textstr="Die erste Ableitung dieser Funktion ist "+str(ersteAbl)
        props = dict(boxstyle="square", facecolor='wheat', alpha=0.5)
        axis.text(0.05, 0.95, textstr, transform=axis.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        
        with open ("daten.txt","a+") as d:            
             d.write(str(self.E1.get())+": " + textstr + "\n")
        
        canvas.draw()

root = tk.Tk()
app = P(master = root)


app.mainloop()
    

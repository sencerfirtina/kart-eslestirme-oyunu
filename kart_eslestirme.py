import tkinter as tk
import random
from tkinter import PhotoImage as Pi
from PIL import Image,ImageTk,ImageSequence
import glob
import os

class Oyun():

    def __init__(self):
        self.pencere = tk.Tk()
        self.sayilar = list(range(1,9)) * 2
        random.shuffle(self.sayilar)
        self.kartlar = []
        self.yazilar = []
        self.acik_kartlar = []
        self.eslesmis_kartlar = []
        self.onceki_sureler = []
        self.x1 = 85
        self.y1 = 240
        self.x2 = 185
        self.y2 = 340
        self.ilk_kart = True  #sayacı ilk karta tıklanınca başlatmak için ilk kart kontrolü
        self.kart_kilidi = False  #kart kontrolü yapılırken kart açma işlemini durdurur
        self.sayac_aktif = False  #sayacin aktiflik durumunu belirler
        self.sure_metni = None  #ekranda süreyi göstermeye yarar
        self.saniye = 0  #saniye değerini int olarak tutar
        self.counter = 0  #kartalara yazıları karışık atayabilmek için gerekli bir değişken
        self.butonlar = []
        self.normal_genislik = 600
        self.acik_genislik = 800

    def pencereyi_sekillendir(self):
        self.pencere.title("Kart Eslestirme")
        self.pencere.geometry("600x800")
        self.pencere.resizable(False,False)
    
    def frame_ve_canvas_olustur(self):
        self.menu_frame = tk.Frame(self.pencere,width=600,height=800,bg="white")
        self.oyun_frame = tk.Frame(self.pencere,width=600,height=800,bg="white")

        self.menu_canvas = tk.Canvas(self.menu_frame,width=600,height=800,bg="white")
        self.menu_canvas.place(x=0,y=0,relwidth=1,relheight=1)

        self.oyun_canvas = tk.Canvas(self.oyun_frame,width=600,height=800,bg="white")
        self.oyun_canvas.place(x=0,y=0)

        self.menu_frame.pack()

    def gorselleri_yukle(self):
        IMG_PATH = "Resimler"

        self.game_bg = Pi(file=os.path.join(IMG_PATH,"game_bg.png"))
        self.skor_bg = Pi(file=os.path.join(IMG_PATH,"game_bg.png"))
        self.menu_bg = Pi(file=os.path.join(IMG_PATH,"menu_bg.png"))
        self.plant_icon = Pi(file=os.path.join(IMG_PATH,"plant.png"))
        self.panda_icon = Pi(file=os.path.join(IMG_PATH,"panda.png"))
        self.catsy_icon = Pi(file=os.path.join(IMG_PATH,"cute_catsy_thing.png"))
        self.frame_left = [ImageTk.PhotoImage(Image.open(img)) for img in glob.glob(os.path.join(IMG_PATH,"frame_left_*.png"))]
        self.frame_right = [ImageTk.PhotoImage(Image.open(img)) for img in glob.glob(os.path.join(IMG_PATH,"frame_right_*.png"))]

    def iconlari_yerlestir(self):
        self.menu_canvas.create_image(170,545,image = self.plant_icon)
        self.menu_canvas.create_image(660,-20,anchor = "ne",image=self.catsy_icon)
        self.menu_canvas.create_image(90,700,image= self.panda_icon)

    def arka_planlari_yerlestir(self):
        self.oyun_canvas.create_image(0,0,anchor="nw", image = self.game_bg)
        self.oyun_canvas.create_image(900,380,image = self.skor_bg)
        self.menu_canvas.create_image(0,0,anchor="nw",image = self.menu_bg)
    
    def tilki_animasyon(self):
        yon = "sol"
        tilki_x = 350
        tilki_y = 520
        frame_idx = 0
        tilki_adim = 0

        def animate():
            nonlocal yon,tilki_x,tilki_y,frame_idx,tilki_adim

            self.menu_canvas.delete("tilki")

            if yon == "sol":
               frame = self.frame_left[frame_idx]
               tilki_x -= 5
            else:
                frame = self.frame_right[frame_idx]
                tilki_x += 5
            
            self.menu_canvas.create_image(tilki_x,tilki_y,image=frame,tags="tilki")
            tilki_adim += 1

            frame_idx = (frame_idx + 1) % 5

            if tilki_adim >= 22:
                yon = "sag" if yon == "sol" else "sol"
                tilki_adim = 0
            
            self.menu_canvas.after(250,animate)

        animate()
    
    def sayaci_guncelle(self):
        if self.sayac_aktif:
            dakika = self.saniye // 60
            saniyelik = self.saniye % 60
            self.zaman = f"{dakika:02}:{saniyelik:02}"
            self.oyun_canvas.itemconfig(self.sure_metni,text=self.zaman)
            self.saniye += 1
            self.oyun_canvas.after(1000,self.sayaci_guncelle)
    
    def oyun_bitis_kontrol(self):
        self.hepsi_acik = all(self.oyun_canvas.itemcget(yazi,"state") == "normal"for yazi in self.yazilar)
        if self.hepsi_acik:
            self.sayac_aktif = False
            self.oyun_canvas.create_text(305,200,text="🎉TEBRİKLEER🎉",font=("Arial",35,"bold"), fill="#28FC5A")
            self.onceki_sureler.append(self.zaman)

    def kartlari_gizle(self):
        self.kart_kapama_anim(self.acik_kartlar[0],self.yazilar[self.index1])
        self.kart_kapama_anim(self.acik_kartlar[1],self.yazilar[self.index2])
        self.acik_kartlar.clear()
        self.kart_kilidi = False
    
    def eslesmis_kartlari_ekle(self):
        self.eslesmis_kartlar.extend([self.acik_kartlar[0],self.acik_kartlar[1]])
        self.acik_kartlar.clear()
        self.kart_kilidi = False
        self.oyun_bitis_kontrol()
    
    def eslesme_kontrol(self):
        self.kart_kilidi = True

        self.index1 = self.kartlar.index(self.acik_kartlar[0])
        self.index2 = self.kartlar.index(self.acik_kartlar[1])

        if self.oyun_canvas.itemcget(self.yazilar[self.index1],"text") != self.oyun_canvas.itemcget(self.yazilar[self.index2],"text"):
            self.oyun_canvas.after(800,self.kartlari_gizle)
        else:
            self.oyun_canvas.after(300,self.eslesmis_kartlari_ekle)
    
    def kart_cevirme(self,event=None):
        if self.ilk_kart:
            self.saniye = 0
            self.sayac_aktif = True
            self.sayaci_guncelle()
        if self.kart_kilidi:
            return

        self.tiklanan = self.oyun_canvas.find_withtag("current")[0]
        self.index = self.kartlar.index(self.tiklanan)

        if self.tiklanan in self.eslesmis_kartlar:
            return
        if self.tiklanan in self.acik_kartlar:
            return
        if len(self.acik_kartlar) < 2:
            self.kart_acma_anim(self.tiklanan,self.yazilar[self.index])
            self.acik_kartlar.append(self.tiklanan)
        if len(self.acik_kartlar) == 2:
            self.eslesme_kontrol()
        self.ilk_kart = False

    def yeniden_basla(self):
        self.oyun_canvas.delete("all")

        random.shuffle(self.sayilar)

        self.kartlar.clear()
        self.yazilar.clear()
        self.acik_kartlar.clear()
        self.eslesmis_kartlar.clear()
        self.sure_metni = None
        self.saniye = 0
        self.sayac_aktif=False
        self.counter = 0
        self.x1= 85
        self.x2= 185
        self.y1 = 240
        self.y2 = 340
        self.kart_kilidi = False
        self.ilk_kart = True

        self.oyun_canvas.create_image(0,0,anchor="nw",image = self.game_bg)
        self.oyun_canvas.create_image(900,380,image = self.skor_bg)

        self.kart_dagitma()
    
    def kart_dagitma(self):
        for i in range(4):
            for j in range(4):
                self.kart = self.oyun_canvas.create_rectangle(self.x1,self.y1,self.x2,self.y2,fill="pink")
                self.yazi = self.oyun_canvas.create_text(self.x1+50,self.y1+50,text=self.sayilar[self.counter],font=("Arial",24), fill="black",state="hidden")

                self.yazilar.append(self.yazi)
                self.kartlar.append(self.kart)
                
                self.oyun_canvas.tag_bind(self.kart,"<Button-1>",self.kart_cevirme)
                self.counter += 1
                self.y1 = self.y2 + 10
                self.y2 = self.y1 + 100
            self.y1 = 240
            self.y2 = 340
            self.x1 = self.x2 + 10
            self.x2 = self.x1 + 100
        self.sure_metni = self.oyun_canvas.create_text(300,130,text="00:00",font=("Arial",40,"bold"),fill="white")
    
    def oyuna_basla(self):
        self.menu_frame.pack_forget()
        self.oyun_frame.pack(fill="both",expand=True)

    def menuye_don(self):
        self.oyun_frame.pack_forget()
        self.yeniden_basla()
        self.menu_frame.pack(fill="both",expand=True)
    
    def cikis_yap(self):
        self.pencere.destroy()

    def butonlari_olustur(self):
        self.yeniden_oyna_buton = tk.Button(self.oyun_frame,text="Yeniden Oyna",
                                            command=self.yeniden_basla,bg="#FCD4F7", 
                                            fg="#393939", font=("Helvetica", 12, "bold"),
                                            activebackground="#FCBDF7",
                                            bd=4, relief="ridge", width=20)
        self.yeniden_oyna_buton.place(x=85,y=710)

        self.menuye_don_buton = tk.Button(self.oyun_frame,text="Menuye Don",
                                          command=self.menuye_don,bg="#FCD4F7", 
                                          fg="#393939", font=("Helvetica", 12, "bold"),
                                          activebackground="#FCBDF7",
                                          bd=4, relief="ridge", width=20)
        self.menuye_don_buton.place(x=305,y=710)

        self.oyuna_basla_buton = tk.Button(self.menu_frame,text="Oyuna Basla",
                                           command=self.oyuna_basla,bg="#FCD4F7", 
                                           fg="#393939", font=("Helvetica", 12, "bold"),
                                           activebackground="#FCBDF7",
                                           bd=4, relief="ridge", width=30)
        self.oyuna_basla_buton.place(x=150,y=570)

        self.cikis_yap_buton = tk.Button(self.menu_frame,text="Cikis Yap",
                                         command=self.cikis_yap,bg="#FCD4F7", 
                                         fg="#393939", font=("Helvetica", 12, "bold"),
                                         activebackground="#FCBDF7",
                                         bd=4, relief="ridge", width=30)
        self.cikis_yap_buton.place(x=150,y=630)

        self.butonlar.extend([self.yeniden_oyna_buton,self.menuye_don_buton,self.oyuna_basla_buton,self.cikis_yap_buton])
    
    def hover_efektlerini_ekle(self):
        def koyulastir(e):
            e.widget.config(bg="#FAC0F5")
        def renk_ac(e):
            e.widget.config(bg="#FCD4F7")
        for buton in self.butonlar:
            buton.bind("<Enter>",koyulastir)
            buton.bind("<Leave>",renk_ac)
    
    def skor_tablosunu_olustur(self):
        skor_tablo = tk.Frame(self.oyun_frame,width=30,height=800,bg="#B0F2FF")
        skor_tablo.place(x=570,y=0)

        skor_tablo.bind("<Enter>",self.skor_panelini_ac)
        skor_tablo.bind("<Leave>",self.skor_panelini_kapat)

    def skor_panelini_ac(self,event=None):
        self.pencereyi_genislet(self.normal_genislik)
        self.canvasi_genislet(self.normal_genislik)

    def pencereyi_genislet(self, genislik):
        if genislik<=800:
            self.pencere.geometry(f"{genislik}x800")
            self.pencere.after(10,lambda:self.pencereyi_genislet(genislik + 10))
        self.normal_genislik = 600

    def canvasi_genislet(self, genislik):
        if genislik <= 800:
            self.oyun_canvas.config(width=genislik)
            self.pencere.after(10,lambda:self.canvasi_genislet(genislik + 10))
        self.normal_genislik = 600

        if self.onceki_sureler:
            for i in range(len(self.onceki_sureler)):
                self.oyun_canvas.create_text(700,40+i*50,text=self.onceki_sureler[i],font=("Arial",30,"bold"),fill="white")
    
    def skor_panelini_kapat(self,event=None):
        self.pencereyi_daralt(self.acik_genislik)
        self.canvasi_daralt(self.acik_genislik)
    
    def pencereyi_daralt(self,genislik):
        if genislik >= 600:
            self.pencere.geometry(f"{genislik}x800")
            self.pencere.after(10,lambda:self.pencereyi_daralt(genislik - 10))
        self.acik_genislik = 800
    
    def canvasi_daralt(self,genislik):
        if genislik >= 600:
            self.oyun_canvas.config(width=genislik)
            self.pencere.after(10,lambda:self.canvasi_daralt(genislik - 10))
        self.acik_genislik = 800
    
    def kart_acma_anim(self,kart_id,yazi_id, adim = 0, max_adim = 5):
        x1,y1,x2,y2 = self.oyun_canvas.coords(kart_id)

        if adim < max_adim:
            yeni_x1 = x1 + 5
            yeni_x2 = x2 - 5
            self.oyun_canvas.coords(kart_id,yeni_x1,y1,yeni_x2,y2)
            self.oyun_canvas.after(30,lambda:self.kart_acma_anim(kart_id,yazi_id,adim+1,max_adim))
        elif adim == max_adim:
            self.oyun_canvas.itemconfig(yazi_id, state="normal")
            self.oyun_canvas.itemconfig(kart_id,fill="#7CFCFA")
            self.oyun_canvas.after(30,lambda:self.kart_acma_anim(kart_id,yazi_id,adim+1,max_adim))
        elif adim < max_adim*2 + 1:
            yeni_x1 = x1 - 5
            yeni_x2 = x2 + 5
            self.oyun_canvas.coords(kart_id,yeni_x1,y1,yeni_x2,y2)
            self.oyun_canvas.after(30,lambda:self.kart_acma_anim(kart_id,yazi_id,adim+1,max_adim))
    
    def kart_kapama_anim(self,kart_id,yazi_id,adim = 0,max_adim = 5):
        x1,y1,x2,y2 = self.oyun_canvas.coords(kart_id)

        if adim < max_adim:
            yeni_x1 = x1 + 5
            yeni_x2 = x2 - 5
            self.oyun_canvas.coords(kart_id,yeni_x1,y1,yeni_x2,y2)
            self.oyun_canvas.after(30,lambda:self.kart_kapama_anim(kart_id,yazi_id,adim+1,max_adim))
        elif adim == max_adim:
            self.oyun_canvas.itemconfig(yazi_id, state = "hidden")
            self.oyun_canvas.itemconfig(kart_id,fill="pink")
            self.oyun_canvas.after(30,lambda:self.kart_kapama_anim(kart_id,yazi_id,adim+1,max_adim))
        elif adim < max_adim*2 + 1:
            yeni_x1 = x1 - 5
            yeni_x2 = x2 + 5
            self.oyun_canvas.coords(kart_id,yeni_x1,y1,yeni_x2,y2)
            self.oyun_canvas.after(30,lambda:self.kart_kapama_anim(kart_id,yazi_id,adim+1,max_adim))
    
o = Oyun()

o.pencereyi_sekillendir()
o.frame_ve_canvas_olustur()
o.gorselleri_yukle()
o.arka_planlari_yerlestir()
o.iconlari_yerlestir()
o.tilki_animasyon()
o.butonlari_olustur()
o.hover_efektlerini_ekle()
o.skor_tablosunu_olustur()
o.kart_dagitma()

o.pencere.mainloop()
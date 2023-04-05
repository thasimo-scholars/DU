import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import os

# proměné
save = 0
i = 0
g = 1
dic = 0
file_path1 = "DU/úkol/budget.csv"

#proměné grafu %
es1 = 0
es2 = 0
es3 = 0
esostatni = 0
k = 0
dohromadyvsech = 0

#listy

cat=[]
am=[]
sp=[]
st=[]

#for saving dictionaries
budg=[]
maxim=[]
minim=[]
průmě=[]
sumy=[]

#dictionaries
dictionary_event = {}

#otevřít soubor, smazat první řádek a seřadit
f = open(file_path1, "r")
rozdeleni_na_radky = f.read().splitlines()

rozdeleni_na_radky.pop(0)
rozdeleni_na_radky.sort()


#rozdělení řádků do listů (cat-categorie, am-amount, sp-spent, st-status)
for radek in rozdeleni_na_radky:
    r = radek.split(";")
    cat.append(r[0])
    am.append(r[1])
    sp.append(r[2].replace(",","."))
    st.append(r[3])
    am[i] = float(am[i])
    sp[i] = float(sp[i])
    i += 1

#amount a spent do slovníků
amount_dict = {category: [] for category in set(cat)}
spent_dict = {category: [] for category in set(cat)}

cat = list(set(cat)) #odstranění duplicit
#přidání hodnot do slovníků, ke každé kategorii přidá hodnoty
for category in cat:
    for radek in rozdeleni_na_radky:
        r = radek.split(";")
        current_category = r[0]
        amount = float(r[1])
        spent = float(r[2].replace(",", "."))

        if current_category == category:
            amount_dict[current_category].append(amount)
            spent_dict[current_category].append(spent)
                
                
                

st = list(set(st)) #odstranění duplicit

#spočítání, kolik je dohromady closed, planing, open a pokud existuje, tak i ostatní
for radek in rozdeleni_na_radky:
    r = radek.split(";")
    if k+1 < len(st):
        if st[k] == r[3]:
            es1 += 1
            k = 0
            dohromadyvsech += 1
        else:
            k += 1
            if st[k] == r[3]:
                es2 += 1
                k = 0
                dohromadyvsech += 1
            else:
                k += 1
                if st[k] == r[3]:
                    es3 += 1
                    k = 0
                    dohromadyvsech += 1
                else:
                    esostatni += 1
                    k = 0
                    dohromadyvsech += 1
                
    else:
        k = 0    
        
#výpočet procent
procentaprvni = es1/dohromadyvsech*100
procentadruhy = es2/dohromadyvsech*100 
procentatreti = es3/dohromadyvsech*100
procenataostatni = esostatni/dohromadyvsech*100


 
#ke kategorii přidat procenta
while dic < len(cat):
    while dic == 0:
        dictionary_event[st[dic]] = float(procentaprvni)
        dic += 1
        break
    while dic == 1:   
        dictionary_event[st[dic]] = float(procentadruhy)
        dic += 1
        break
    while dic == 2:
        dictionary_event[st[dic]] = float(procentatreti)
        dic += 1
        break
    while dic == 3:
        dictionary_event["ostatní"] = float(procenataostatni)
        dic += 0
        break
    break


#graf v matlibu
def sloupecgraf():
    global save
    catnnum = {key: (sum(amount_dict[key]), sum(spent_dict[key])) for key in amount_dict}
    keys = list(catnnum.keys())
    values1 = [value[0] for value in catnnum.values()]
    values2 = [value[1] for value in catnnum.values()]


    #filter out empty values 
    keys, values1, values2 = zip(*[(k, v1, v2) for k, v1, v2 in zip(keys, values1, values2) if v1 and v2])
    #zda je float a int. 
    if all(isinstance(val, (int, float)) for val in values1) and all(isinstance(val, (int, float)) for val in values2):
        bar_width = 0.35
        index = np.arange(len(keys))

        fig, ax = plt.subplots()
        ax.bar(index, values1, bar_width, color='#7B136F', label='amount')
        ax.bar(index + bar_width, values2, bar_width, color='#E28413', label='spent')

        ax.set_xlabel('Kategorie')
        ax.set_ylabel('Hodnoty')
        ax.set_title('sloupcový graf', pad=20)
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(keys)
        ax.legend()

        background_color = "#255957"
        font_color = "#FFFFFF"
        
        fig.patch.set_facecolor(background_color)
        ax.set_facecolor(background_color)

        for label in [ax.xaxis.label, ax.yaxis.label, ax.title] + ax.get_xticklabels() + ax.get_yticklabels():
            label.set_color(font_color)
        
        plt.tight_layout()
        if save == 1:
            plt.savefig('úkol\column_char.png', dpi=300, bbox_inches='tight')
            save = 0
        
        else:
            plt.show()
    else:
        print("Error: values1 and values2 should contain only numbers.")

#už mě to nebaví popisovat. Kdyby něco nebylo jasné, tak se @me   


def kolackobedu():
    global save
    keys = list(dictionary_event.keys())
    values = list(dictionary_event.values())

    colors = ['#B80C09', '#7B136F', '#E28413', '#C2E812']
   
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(values, labels=keys, autopct='%1.1f%%', startangle=90, colors=colors)

   
    ax.axis('equal')

  
    title_text = ax.set_title('Podíl hodnot podle kategorií', pad=20)

    
    background_color = "#255957"
    font_color = "#FFFFFF"
    
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)
    title_text.set_color(font_color)
    
    for text in texts + autotexts:
        text.set_color(font_color)
    
    if save == 1:
        plt.savefig('úkol\pie_chart.png', dpi=300, bbox_inches='tight')
        save = 0
        
    else:
        plt.show()




def seber_lines(soubor):
    with open(soubor, 'r') as soubory:
        for radek in soubory:
            radek = radek.replace(",",".")
            yield radek


def bud(textbox):
    textbox.configure(state='normal')
    textbox.delete("1.0", "end")
    textbox.configure(state='disabled')
    sber = seber_lines(file_path1)

    next(sber)
    for radek in rozdeleni_na_radky:
        textbox.configure(state='normal')
        try:
            line = next(sber)
        except StopIteration:
            break

        data = line.split(";")
        budget = float(data[1])
        spent = float(data[2])
        if spent > budget:
            moc = round((spent - budget)*10)/10
            textbox.insert("end", f"{data[0]} prekrocil/a/o budget o {moc}. \n")
            textbox.configure(state='disabled')
            budg.append(f"{data[0]} prekrocil/a/o budget o {moc}. \n")
            
        else:
            continue
    textbox.configure(state='disabled')



def průměr(textbox, amount_dict, spent_dict):
    textbox.configure(state='normal')
    textbox.delete("1.0", "end")  
    průmě.append("Prumer pro Amount:\n")
    textbox.insert("end", "Prumer pro Amount:\n")
    for category, data in amount_dict.items():
        average = sum(data) / len(data)
        textbox.insert("end", f"Prumer {category}: {average:.2f}\n")
        průmě.append(f"Prumer {category}: {average:.2f}\n")
    textbox.insert("end", "Prumer pro spent:\n")
    průmě.append("Prumer pro spent:\n")
    for category, data in spent_dict.items():
        average = sum(data) / len(data)
        textbox.insert("end", f"Prumer {category}: {average:.2f}\n")
        průmě.append(f"Prumer {category}: {average:.2f}\n")
    textbox.configure(state='disabled')


def minimum(textbox, amount_dict, spent_dict):
    textbox.configure(state='normal')
    textbox.delete("1.0", "end")

    for category in amount_dict.keys():
        min_amount = min(amount_dict[category])
        min_spent = min(spent_dict[category])
        textbox.insert("end", f"Minimum amount {category}: {min_amount:.2f}\n")
        textbox.insert("end", f"Minimum spent {category}: {min_spent:.2f}\n")
        minim.append(f"Minimum amount {category}: {min_amount:.2f}\n")
        minim.append(f"Minimum spent {category}: {min_spent:.2f}\n")
    textbox.configure(state='disabled')

def maximum(textbox, amount_dict, spent_dict):
    textbox.configure(state='normal')
    textbox.delete("1.0", "end")

    for category in amount_dict.keys():
        max_amount = max(amount_dict[category])
        max_spent = max(spent_dict[category])
        textbox.insert("end", f"Maximum amount {category}: {max_amount:.2f}\n")
        textbox.insert("end", f"Maximum spent {category}: {max_spent:.2f}\n")
        maxim.append(f"Maximum amount {category}: {max_amount:.2f}\n")
        maxim.append(f"Maximum spent {category}: {max_spent:.2f}\n")

    textbox.configure(state='disabled')

def suma(textbox, amount_dict, spent_dict):
    textbox.configure(state='normal')
    textbox.delete("1.0", "end")

    for category in amount_dict.keys():
        total_amount = sum(amount_dict[category])
        total_spent = sum(spent_dict[category])
        textbox.insert("end", f"Total amount {category}: {total_amount:.2f}\n")
        textbox.insert("end", f"Total spent {category}: {total_spent:.2f}\n")
        sumy.append(f"Total amount {category}: {total_amount:.2f}\n")
        sumy.append(f"Total spent {category}: {total_spent:.2f}\n")

    textbox.configure(state='disabled')
        
def save_info(textbox, amount_dict, spent_dict):
    bud(textbox)
    suma(textbox, amount_dict, spent_dict)
    maximum(textbox, amount_dict, spent_dict)
    minimum(textbox, amount_dict, spent_dict)
    průměr(textbox, amount_dict, spent_dict)
    #ne nedám ti to do .csv. jsem rád, že se mi povedlo vůbec to .txt :D
    
    folder_path = 'DU/úkol' # replace with the actual folder path
    file_path = os.path.join(folder_path, 'results.txt')

    if os.path.exists(file_path):
        os.remove(file_path)
    
    with open(file_path, 'w') as f:
        f.write('Kde prekrocili limit:\n')
        f.write('\n'.join(budg))
        f.write('\n\n')
        
        f.write('Info o prumeru:\n')
        f.write('\n'.join(průmě))
        f.write('\n\n')
        
        f.write('Info o minimu:\n')
        f.write('\n'.join(minim))
        f.write('\n\n')
        
        f.write('Info o maximu:\n')
        f.write('\n'.join(maxim))
        f.write('\n\n')
        
        f.write('Info o total:\n')
        f.write('\n'.join(sumy))
        
    budg.clear()
    průmě.clear()
    minim.clear()
    maxim.clear()
    sumy.clear()
    
    textbox.configure(state='normal')
    textbox.delete('1.0', 'end')
    textbox.configure(state='disabled')
    
    

    

class App(tk.Tk):
    def __init__(self):  
        super().__init__()

 
        self.title("Úkolíček")
        self.geometry("1100x850+100+100")
        self.configure(bg="#255957")
        
        label_frame = tk.Frame(self, bg="#255957")
        label_frame.pack(pady=10, fill=tk.X, expand=True) 

        label1 = tk.Label(label_frame, text="ÚKOL NA PROGRÁMKO", font=("Georgia", 20), fg="#FFFFFF", bg="#255957")
        label1.pack(side="top", pady=0, expand=True)

        
        label2 = tk.Label(label_frame, text="koník :)", font=("Georgia", 10), bg="#255957", fg="#F4C2C2")
        label2.pack(side="left", anchor="w", pady=0, padx=(0, 0))  


        button_frame = tk.Frame(self, bg="#255957")
        button_frame.pack(pady=10)
        
        button_bg_color = "#8E3B46" 
        button_text_color = "#FFFFFF"
        
        avg_button = tk.Button(button_frame, text="Vypočítat průměry", font=("Georgia", 15), bg=button_bg_color, fg=button_text_color, command=lambda: průměr(self.textbox, amount_dict, spent_dict))
        avg_button.pack(side="left", padx=10)

        min_button = tk.Button(button_frame, text="Vypočítat minima", font=("Georgia", 15), bg=button_bg_color, fg=button_text_color, command=lambda: minimum(self.textbox, amount_dict, spent_dict))
        min_button.pack(side="left", padx=10)

        max_button = tk.Button(button_frame, text="Vypočítat maxima", font=("Georgia", 15), bg=button_bg_color, fg=button_text_color,command=lambda: maximum(self.textbox, amount_dict, spent_dict))
        max_button.pack(side="left", padx=10)

        sum_button = tk.Button(button_frame, text="Calculate sumy", font=("Georgia", 15), bg=button_bg_color, fg=button_text_color, command=lambda: suma(self.textbox, amount_dict, spent_dict))
        sum_button.pack(side="left", padx=10)

        bud_button = tk.Button(button_frame, text="Překročili budget", font=("Georgia", 15), bg=button_bg_color, fg=button_text_color, command=lambda: bud(self.textbox))
        bud_button.pack(side="left", padx=10)




        

      
        self.textbox = tk.Text(self, height=13, width=50, bg="#43E1DB", font=("Georgia", 20), wrap=tk.WORD, state='disabled', padx=5, pady=5)
        self.textbox.pack(pady=10)

    
        button_frame1 = tk.Frame(self, bg="#255957")
        button_frame1.pack(pady=10)

        open_window_button1 = tk.Button(button_frame1, text='Easteregg', font=("Georgia", 15), bg=button_bg_color, fg=button_text_color, command=self.open_window1)
        open_window_button1.pack(side="left", padx=10)

        grafsloupec = tk.Button(button_frame1, text='Sloupcový graf', font=("Georgia", 15), bg=button_bg_color, fg=button_text_color, command=lambda:(sloupecgraf()))
        grafsloupec.pack(side="left", padx=10)

        grafkolac = tk.Button(button_frame1, text='Koláčový graf', font=("Georgia", 15), bg=button_bg_color, fg=button_text_color, command=lambda:(kolackobedu()))
        grafkolac.pack(side="left", padx=10)

        open_window_button4 = tk.Button(button_frame1, text='IHATEPIL', font=("Georgia", 15), bg=button_bg_color, fg=button_text_color, command=self.open_window4)
        open_window_button4.pack(side="left", padx=10)
        
        
        button_frame2 = tk.Frame(self, bg="#255957")
        button_frame2.pack(pady=10)
        
        save_graphs_button = tk.Button(button_frame2, text='Save Graphs', font=("Georgia", 15), bg=button_bg_color, fg=button_text_color, command=lambda: (globals().update(save=save+1), sloupecgraf(), globals().update(save=save+1), kolackobedu()))
        save_graphs_button.pack(side="left", padx=10)
        
        save_info_button = tk.Button(button_frame2, text='Save Info', font=("Georgia", 15), bg=button_bg_color, fg=button_text_color, command=lambda:(save_info(self.textbox, amount_dict, spent_dict)))
        save_info_button.pack(side="left", padx=10)

    def open_window1(self):  
        window = Window1(self)
        window.grab_set()


    def open_window2(self): 
        window = Window2(self)
        window.grab_set()

    
    def open_window3(self): 
        window = Window3(self)
        window.grab_set()

    def open_window4(self):  # Remove the 'window' argument
        window = Window4(self)
        window.grab_set()

class Window1(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.video_source = "DU/úkol/easteregg.mp4"
        self.cap = cv2.VideoCapture(self.video_source)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.geometry('1280x720')

        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.update()

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            self.canvas.image = photo
            self.after(33, self.update)
        else:
            self.cap.release()


class Window2(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('300x100')
        self.title('Toplevel Window')

        ttk.Button(self,
                   text='Close',
                   command=self.destroy).pack(expand=True)
        
class Window3(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('300x100')
        self.title('Toplevel Window')

        ttk.Button(self,
                   text='Close',
                   command=self.destroy).pack(expand=True)
        
class Window4(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('1920x1080')
        self.title('Toplevel Window')

        
        image = Image.open('DU/úkol/ha.jpg')
        image = image.resize((1920, 1080), Image.ANTIALIAS)
        
        self.photo = ImageTk.PhotoImage(image)

        
        label = tk.Label(self, image=self.photo)
        label.pack(fill=tk.BOTH, expand=True)

        
        ttk.Button(self, text='Close', command=self.destroy).pack(expand=True)



if __name__ == "__main__":
    app = App()
    app.mainloop()


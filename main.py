from tkinter import *

from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime

# okno Tk
window = Tk()
window.title("Převod měn")
window.minsize(300, 200)  # velikost okna
window.resizable(False, False)
window.config(bg="#222")
window.iconbitmap("icon_many.ico")


# funkce web_scraping - kurz měny z ČNB
def kurz_euro():
    response = requests.get("https://www.cnb.cz/cs/")
    soup = bs(response.text, "html.parser")

    euro = soup.find(id="rate_eur")
    euro = euro.getText()
    euro_float = float(euro.replace(",", "."))
    return round(euro_float, 2)


# funkce 1 czk = CNB
def count_currency_czk():
    try:
        amount_czk = float(amount_input.get()) * kurz_euro()
        result_label_czk["text"] = round(amount_czk, 2)
    except (ValueError, ZeroDivisionError, NameError):
        result_label_czk["text"] = "Zadávej pouze celá čísla!"


# funkce 1 euro = CNB
def count_currency_euro():
    try:
        amount_eur = float(amount_input.get()) / kurz_euro()
        result_label_euro["text"] = round(amount_eur, 2)
    except (ValueError, ZeroDivisionError, NameError):
        result_label_euro["text"] = "Zadávej pouze celá čísla!"


def ulozit_soubor():
    zapis_euro = str(result_label_euro["text"])
    zapis_czk = str(result_label_czk["text"])
    datum = datum_cas()
    castka = amount_input.get()

    # zápis převodu měny do txt souboru, poslední převod měny je vždy na začátku souboru
    text_prevod_meny = f"\n{datum}\n1 euro = {str(kurz_euro())} czk\nČástka: {castka}\n{zapis_euro} euro\n{zapis_czk} czk\n{'-'*18} "

    with open(
        "prevod_meny.txt", "r+", encoding="utf-8"
    ) as f:
        cist_obsah = f.read()
        f.seek(0, 0)
        f.write(text_prevod_meny)
        f.write(cist_obsah)


def datum_cas():
    datum_cas = datetime.now()
    datum_cas = datum_cas.strftime("%d.%m.%Y  %H:%M")
    return datum_cas


# vstup uživatele
amount_input = Entry(width=15, font=("Helvetica", 15))
amount_input.grid(row=0, column=0, padx=10, pady=10)


# label částka
czk_label = Label(text="Částka", font=("Helvetica", 15), bg="#222", fg="white")
czk_label.grid(row=0, column=1)

# euro
result_label_euro = Label(text="0", font=("Helvetica", 15), bg="#222", fg="white")
result_label_euro.grid(row=1, column=0)

# czk
result_label_czk = Label(text="0", font=("Helvetica", 15), bg="#222", fg="white")
result_label_czk.grid(row=2, column=0)

# kurz CNB
euro_CNB = Label(
    text=("euro", "=", kurz_euro(), "ckz", "-", "kurz", "ČNB"),
    font=("Helvetica", 11),
    bg="#222",
    fg="white",
)
euro_CNB.grid(row=3, column=0)

# čas + datum
cas_datum = Label(text=(datum_cas()), font=("Helvetica", 11), bg="#222", fg="white")
cas_datum.grid(row=4, column=0)


# Tlačítka
count_button = Button(text=" EUR ", font=("Helvetica", 15), command=count_currency_euro)
count_button.grid(row=1, column=1, padx=10, pady=10)

count_button = Button(text=" CZK ", font=("Helvetica", 15), command=count_currency_czk)
count_button.grid(row=2, column=1, padx=10, pady=10)

count_button = Button(text="Uložit", font=("Helvetica", 15), command=ulozit_soubor)
count_button.grid(row=3, column=1, padx=10, pady=10)


# hlavní cyklus
window.mainloop()

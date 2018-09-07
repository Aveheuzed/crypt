from seth import encode, decode

from sys import argv
if len(argv)>1 :
    from getpass import getpass
    del argv[0]
    if argv[0] in ("help","--help","-h","/?"):
        print("""\
Seth - algorithme de chiffrement : page d'aide
(pour utiliser le mode graphique, ne pas passer d'argument)
raccourcis en mode graphique :
    ^-o : Ouvrir un fichier et le déchiffrer
    ^-s : Crypter le texte affiché dans un fichier
    ^-l : Charger un texte (non chiffré)

mode console :
usage : seth [help, --help, -h, /?] [--standard-io] -s|-l <source> <destination>

    help, --help, -h, /? : affiche l'aide

    -s <source> <destination> : Ouvre un fchier texte (lisible) pour le crypter

    -l <source> <destination> : Ouvre un fichier crypté pour le déchiffrer

    --standard-io : utilisé avec -s, <source> n'est pas le chemin d'un fichier, mais le texte à chiffrer ;
    si <source> est absent, l'entrée standard sera utilisée
                    utilisé avec -l, affiche le texte décrypté sur la sortie standard au lieu de l'écrire dans un fichier (dans ce cas, ne pas spécifier de <destination>)
""")
        exit(0)
    if argv[0] == "--standard-io" :
        if argv[1] == "-s":
            if len(argv) < 3 :
                print("Syntaxe inconnue. Utilisez -h pour obtenir de l'aide.") ; exit(0)
            elif len(argv) == 3 :#read to stdin
                source = input("Texte à chifrer : ").encode()
            else :#read to argv
                source = " ".join(argv[2:-1]).encode()
            key = getpass("Clé de chiffrement : ").encode()
            open(argv[-1],"wb").write(encode(source,key))
        elif argv[1] == "-l":
            if len(argv) != 3 :
                print("Syntaxe inconnue. Utilisez -h pour obtenir de l'aide.") ; exit(0)
            else :
                source = open(argv[2],"rb").read()
                key = getpass("Clé de déchiffrement : ").encode()
                print(decode(source,key).decode(errors="replace"))
    elif argv[0] == "-s":
        source = open(argv[1],"rt").read().encode()
        key = getpass("Clé de chiffrement : ").encode()
        open(argv[2],"wb").write(encode(source,key))
    elif argv[0] == "-l":
        source = open(argv[1],"rb").read()
        key = getpass("Clé de déchiffrement : ").encode()
        open(argv[2],"wt").write(decode(source,key).decode(errors="replace"))
    else :
        print("Syntaxe inconnue. Utilisez -h pour obtenir de l'aide.") ; exit(0)
    exit(0)

## /\mode console ; \/ mode graphique
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import asksaveasfile, askopenfile
from tkinter.messagebox import showerror

main = Tk()
main.title("Crypteur Seth")

plain = ScrolledText(main)

def crypt(*args):
    text = plain.get("1.0","end")[:-1].encode()
    K = key.get().encode()
    file = asksaveasfile(mode="wb")
    if file is not None :
        file.write(encode(text,K))
        file.close()
        plain.delete("1.0","end")

def decrypt(*args):
    text = askopenfile(mode="rb")
    if text is not None :
        text = text.read()
        K = key.get().encode()
        if not len(K) :
            showerror("Pas de clé","Veuillez entrer votre clé en premier (en bas à droite)")
        else :
            plain.delete("1.0","end")
            plain.insert("1.0",decode(text,K).decode(errors="replace"))

def open_(*args):
    text = askopenfile(mode="rt")
    if text is not None :
        text = text.read()
        plain.delete("1.0","end")
        plain.insert("1.0",text)

key = Entry(main,show="*")

plain.pack(side="top",fill="both", expand=True)
key.pack(side="right")
Label(main,text="Clé de [dé]cryptage :").pack(side="left")

main.bind("<Control-o>",decrypt)
main.bind("<Control-s>",crypt)
main.bind("<Control-l>",open_)
key.focus()

main.mainloop()

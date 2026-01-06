import random
import string
import qrcode
import chess
import jarvis
import iplocator
import instagram_bot
import crypto
import trad
import pdfplumber
header = """
                          _             
                         (_)            
 ___  ___ ___  _ __ _ __  _  ___  _ __  
/ __|/ __/ _ \| '__| '_ \| |/ _ \| '_ \ 
\__ \ (_| (_) | |  | |_) | | (_) | | | |
|___/\___\___/|_|  | .__/|_|\___/|_| |_|
                   | |                  
                   |_|  
    ----------------------
        LISTE DES COMMANDES DISPONIBLES
        ----------------------
        password : génère un mot de passe aléatoire et sécurisé.
        qr code : génère un QR code à partir d'un texte ou d'un lien.
        jarvis : active l'assistant vocal Jarvis pour des recherches.
        chess : démarre un jeu d'échecs.
        ip : lance iplocator permettant de faire des recherches sur les ip/port ... 
        instagram_info :permet de recuperer des informations sur le compte instagram
        crypto : lance  crypto permettant de recuperer des informations sur les marcher
        quitter : quitte le terminal.
        help : affiche cette liste de commandes.
        trad : traduction
        pdf_extract : extraire texte depuis pdf
    """
print(header)
#exctracteur de texte a partir dun fichier pdf renvoyer dan sn fichier txt
def pdf_extract():
    pdf_path = input("Entrez le chemin vers votre PDF : ")

    with pdfplumber.open(pdf_path) as pdf:
        with open("extracted-text.txt", "w", encoding="utf-8") as f:
            for page in pdf.pages:
                f.write(page.extract_text() or "")


#createur de mot de passe securisee
def password(length):
    total = string.ascii_letters + string.digits + string.punctuation

    password = "".join(random.sample(total, int(length)))
    return password
#generateur de qr code
def qr_code(texte,):
    qr = qrcode.QRCode(
        version=10,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=15,
        border=4,
    )

    qr.add_data(texte)
    qr.make(fit=True)
    img = qr.make_image(fill_color="red", back_color="white")
    img.save()

#aide et doccumentation de tout les programmes disponibles
def display_help():
    print("""
        ----------------------
        LISTE DES COMMANDES DISPONIBLES
        ----------------------
        password : génère un mot de passe aléatoire et sécurisé.
        qr code : génère un QR code à partir d'un texte ou d'un lien.
        jarvis : active l'assistant vocal Jarvis pour des recherches.
        chess : démarre un jeu d'échecs.
        ip : lance iplocator permettant de faire des recherches sur les ip/port ... 
        instagram_info : lance instagram_bot qui permet de recuperer des informations sur le compte instagram de votre choix
        crypto : lance  crypto permettant de recuperer des informations sur les marcher de son choix 
        quitter : quitte le terminal.
        help : affiche cette liste de commandes.
    """)


terminal_activer = True
user_command = ""

#lancement du terminal qui tourne en continu
while terminal_activer :
    user_command = input(">>>>")
    #generateur de mot de passe
    if user_command == "password":
        lenght = int(input("combien de caractere >>>>"))
        if lenght >= 64 :
            print("erreur nombre de caracteres maximum depasser (64)")
        print(password(lenght))

    #generateur de qr code
    elif user_command == "qr code" :
        texte = input(" entrer le texte / lien que vous voulez mettre dans le qr code >>>>")
        if texte != "" :
            version = int(input("quelle version de qr code voulez vous (taille)>>>>"))
            if version >=1 and version <=40 :
                chemin = input("veuillez entrez le chemin vers le dossier denregistrement>>>>")
                qr_code(texte)

    #permet a lutilisateur de quitter le terminal
    elif user_command == "quitter" :
        terminal_activer = False

    #active jarvis
    elif user_command == "jarvis":
        jarvis.run()

    # active le traducteur
    elif user_command == "trad":
        trad.trad()


    #permet a l'utilisateur de rechercher la liste des commandes disponibles
    elif user_command == "help" :
        display_help()

    #permet a l'utilisateur de lancer un jeu d'echec
    elif user_command == "chess" :
        screen = chess.main()

    #permet a lutilisateur dutiliser le iplocator
    elif user_command == "ip":
        iplocator.Start_Program()

    #permet a lutilisateur dutiliser le instagram bot permettant de recuperer des informations sur un comptes instagram
    elif user_command == "instagram_info" :
        instagram_bot.main()

    # permet a lutilisateur dutiliser le instagram bot permettant de recuperer des informations sur un comptes instagram
    elif user_command == "crypto":
        crypto.home()

    elif user_command == "pdf_extract":
        pdf_extract()

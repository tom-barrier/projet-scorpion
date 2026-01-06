import nltk
nltk.download('punkt_tab')
from deep_translator import GoogleTranslator
from nltk.tokenize import sent_tokenize
from tqdm import tqdm
import re
from autocorrect import Speller
spell = Speller(lang='en')
def corriger_texte(texte):
    corriger_final = ""
    textes = decouper_en_blocs(texte)
    for texte in tqdm(textes, desc="correction"):
        corriger = spell(texte)
        corriger_final += corriger
    sauvegarder_texte(corriger_final, "correction.txt")
    return corriger_final
def lire_fichier(chemin):
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("Fichier introuvable.")
        return None

def nettoyer_texte(texte):
    return re.sub(r'\s+', ' ', texte.strip())

def decouper_en_blocs(texte, max_chars=4000):
    phrases = sent_tokenize(texte)
    blocs = []
    bloc = ""

    for phrase in phrases:
        if len(bloc) + len(phrase) + 1 <= max_chars:
            bloc += " " + phrase
        else:
            blocs.append(bloc.strip())
            bloc = phrase
    if bloc:
        blocs.append(bloc.strip())
    return blocs

def traduire_blocs(blocs, source="auto", target="fr"):
    traduction = ""
    traducteur = GoogleTranslator(source=source, target=target)
    for bloc in tqdm(blocs, desc="Traduction..."):
        try:
            traduction += traducteur.translate(bloc) + "\n"
        except Exception as e:
            print("Erreur pendant la traduction d’un bloc :", e)
    return traduction

def sauvegarder_texte(texte, nom="traduction.txt"):
    with open(nom, "w", encoding="utf-8") as f:
        textes = decouper_en_blocs(texte,200)
        for texte in textes :
            f.write(texte)
            f.write("\n")

def trad():
    correction_demander = input("[0] sans correction d'ortographes/synatxes \n"
                                "[1] avec correction d'ortographes/syntaxes\n"
                                "entrez votre choix :  ")
    chemin = input("Entrez le chemin du fichier .txt à traduire : ")
    texte = lire_fichier(chemin)
    if not texte:
        return
    texte = nettoyer_texte(texte)
    if correction_demander == 1 :
        texte = corriger_texte(texte)
    blocs = decouper_en_blocs(texte)
    resultat = traduire_blocs(blocs)
    sauvegarder_texte(resultat)
    print("✅ Traduction terminée et enregistrée dans 'traduction.txt'.")

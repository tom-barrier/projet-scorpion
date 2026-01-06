import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install speechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser
import noisereduce as nr
import numpy as np

# Initializing speech synthesis engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate+20)

# Initialisation du recognizer
recognizer = sr.Recognizer()
def speak(audio):
    # Function to speak the given text
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    # Function to greet the user based on the time of day)
    speak("bonjour jarviss a votre service ")


def search_youtube(query):
    # Formuler l'URL de recherche sur YouTube
    youtube_search_url = f"https://www.youtube.com/results?search_query={query}"

    # Ouvrir l'URL dans le navigateur par défaut
    webbrowser.open(youtube_search_url)
def search_google(query):
    # Formuler l'URL de recherche sur google
    google_search_url = f"https://www.google.com/search?q={query}"

    # Ouvrir l'URL dans le navigateur par défaut
    webbrowser.open(google_search_url)


def calculate_energy(audio_data):
    # Calculer l'énergie de l'audio en utilisant les échantillons audio
    raw_data = audio_data.get_raw_data()  # Récupérer les données brutes
    samples = np.frombuffer(raw_data, dtype=np.int16)  # Convertir les données brutes en un tableau numpy
    energy = np.sum(np.square(samples))  # Calculer l'énergie en sommant les carrés des échantillons
    return energy

def takeCommand():
    #ce bloc recupere la voix de lutilisateur puis renvoie le texte compris
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("écoute...")
        r.pause_threshold=2
        r.energy_threshold = 450
        audio=r.listen(source)
    try:
        print("Reconnaissance...")
        query=r.recognize_google(audio,language="fr")
        print(f"l'utilisateur a dit:{query}")

    except Exception as e:
        return "None"
    return query

def run():
    wishMe()
    while True:
        query = takeCommand()  # Prendre la commande de l'utilisateur

        if query:  # Si une commande valide est reçue
            query = query.lower()  # Mettre la commande en minuscules
            print(f"User said: {query}")  # Afficher ce que l'utilisateur a dit

            # quite le programme si lun de ces mots est reconnues
            if query == "quitter" or query == "fermer":
                break

            # logique pour executer les demande de l'utilisateur
            if "wikipédia" in query:
                # recherche et lis les informations de wikipedia
                speak("recherche Wikipedia...")
                query = query.replace("wikipédia", "")
                speak("que voulez vous recherchez")
                query = takeCommand()
                results = wikipedia.summary(query, sentences=2)
                speak("daprès Wikipedia")
                print(results)
                speak(results)
                #logique pour effectuer une recherche youtube
            elif "recherche youtube" in query:
                speak("que voulez vous recherchez ")
                query = takeCommand()
                search_youtube(query)

            elif "recherche google" in query:
                speak("que voulez vous recherchez ")
                query = takeCommand()
                search_google(query)

            elif "heure" in query:
                # recupere puis lis l'heure
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"monsieur il est  {strTime}")

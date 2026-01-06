import ccxt
import mplfinance as mpf
import pandas as pd
from datetime import datetime
import bot_trading
import time


def Display_Menu():
    header = """
                                                                   
                      | |                                     
  ___ _ __ _   _ _ __ | |_ ___   
 / __| '__| | | | '_ \| __/ _ \ 
| (__| |  | |_| | |_) | || (_) |
 \___|_|   \__, | .__/ \__\___/ 
            __/ | |              
           |___/|_|             
    ### Tools:
        [1] trouver le prix d'une devise
        [2] trouver l'evolution sune devise sur les 24 dernieres heures
        [3] investir sur binance
        [4]regarder le graphique dune devise
        [5] demander son avis a un bot de trading
        [6] exit 
    """
    print(header)

# Créer une instance de l'échange (ici, Binance)
exchange = ccxt.binance()

def home():
    Display_Menu()
    users = input("selectionner une option")
    if users == "1":
        print(getprice(input("quelle devise")))
    elif users == "2":
        print(evolution((input("quelle devise"))))
    elif users == "3":
        symbol = input("quelle devise")
        amount = input("quelle quantiter ")
        price = input("a quelle prix ")
        api_key = input("entree votre clee api")
        api_secret = input("entree votre cle api secrete")
        print(investir(symbol, amount, price, api_key, api_secret))
    elif users == "4" :
        symbol = input("quelle devise")
        heures = input("depuis combien de temps")
        graphique(symbol,heures)
    elif users == "5":
        bot_trading.run()


#permet de connaitre la valeur actuel du symbole entree par lutilisateur
def getprice(symbol):
    symbol = symbol.upper()
    symbol_1 = symbol.split("/")

    try:
        v_price = exchange.fetch_ticker(symbol)
        r_price = v_price["info"]["lastPrice"]
        if symbol_1[1] == "USD" or symbol_1[1] == "USDT":
            v_return = "{:.2f} {}".format(float(r_price), symbol_1[1])
            return v_return
        else:
            v_return = "{:.8f} {}".format(float(r_price), symbol_1[1])
            return v_return
    except (ccxt.ExchangeError, ccxt.NetworkError) as error:
        # add necessary handling or rethrow the exception
        return "Got an error", type(error).__name__, error.args
    raise

#permet de connaitre l'évoloution sur les dernieres 24 heures du symbole entree par lutilisateur
def evolution(symbol):
    # Définir la paire de trading
    symbol = symbol.upper()

    # Paramètre '1h' pour des bougies d'une heure
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=24)  # Récupérer les 2 dernières bougies

    # Afficher les données
    print("Données OHLCV :", ohlcv)

    # Calculer la variation de prix entre les deux dernières bougies (dernière et avant-dernière)
    # On récupère les prix de clôture (Close) des deux bougies

    close_last = ohlcv[-1][4]  # Clôture de la dernière bougie
    close_previous = ohlcv[-2][4]  # Clôture de l'avant-dernière bougie

    # Calculer la variation en pourcentage
    price_change_percentage = ((close_last - close_previous) / close_previous) * 100
    print(f"Variation de prix de {symbol} sur les 24 dernieres heures : {price_change_percentage:.2f}%")

#fonction peremttant dinvestir directement sur binance en renseignant plusieurs informations
def investir(symbol,amount,price,api_key,api_secret):
    # Remplacez par vos propres clés API

    # Créez une instance de Binance avec vos clés API
    binance = ccxt.binance({
        'apiKey': api_key,
        'secret': api_secret,
        'enableRateLimit': True,  # Pour limiter les appels API afin d'éviter le ban
    })
    balance = binance.fetch_balance()
    print("Solde disponible:", balance)
    # Exemple de passer un ordre d'achat
    # Passer un ordre d'achat
    order = binance.create_limit_buy_order(symbol, amount, price)
    print("Ordre passé :", order)

    # Attendre un moment pour que l'ordre soit traité
    time.sleep(10)

    balance = binance.fetch_balance()
    print("Solde disponible:", balance)

def graphique(symbol,temps):
    symbol = symbol.upper()
    # Créer une instance de l'échange (ici, Binance)
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=int(temps))  # Récupérer les 2 dernières bougies
    # Données OHLCV
    ohlcv_data = [
        [entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]]  # [timestamp, open, high, low, close, volume]
        for entry in ohlcv
    ]

    # Conversion des timestamps en datetime
    timestamps = [datetime.utcfromtimestamp(item[0] / 1000) for item in ohlcv_data]
    data1 = [
        [entry[3], entry[4]]
        for entry in ohlcv
    ]

    data2 = []
    for i in data1:
        moyenne = i[0] + i[1]
        data2.append(moyenne)

    data = []
    for i in data2:
        moyenne = i / 2
        data.append(moyenne)
    taille = len(data) - 1
    taux = ((data[taille] - data[0]) / data[0]) * 100

    # Création d'un DataFrame pandas pour organiser les données
    df = pd.DataFrame(ohlcv_data, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    # Ajouter la colonne 'moyenne' dans le DataFrame
    df['moyenne'] = data

    # Préparation des données pour mplfinance
    df.set_index('timestamp', inplace=True)
    # Affichage du graphique en bougies avec la courbe de moyenne
    mpf.plot(df, type='candle', style='charles', title='Graphique OHLCV (Bougies)', ylabel='Prix')
    print("le taux d'évolution de la période est de ", taux, "%")

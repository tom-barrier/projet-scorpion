import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np

def calculate_indicators(ticker: str, period: str = '1y') -> dict:
    stock = yf.Ticker(ticker)

    # Essai progressif de périodes pour éviter les erreurs de données manquantes
    periods_to_try = ['1y', '6mo', '3mo']
    data = pd.DataFrame()

    for p in periods_to_try:
        data = stock.history(period=p)
        if not data.empty and len(data) >= 50:  # Minimum pour SMA_50
            print(f"  → Données récupérées avec period={p} ({len(data)} jours)")
            break
        else:
            print(f"  → Pas assez de données avec {p}, essai suivant...")

    if data.empty or len(data) < 50:
        raise ValueError(f"Données insuffisantes pour {ticker} même en 3mo")

    # Calcul des indicateurs de base
    data['SMA_50'] = ta.sma(data['Close'], length=50)
    data['SMA_200'] = ta.sma(data['Close'], length=200) if len(data) >= 200 else np.nan
    data['EMA_20'] = ta.ema(data['Close'], length=20)
    data['RSI'] = ta.rsi(data['Close'], length=14)

    macd = ta.macd(data['Close'])
    data['MACD'] = macd['MACD_12_26_9']
    data['MACD_Signal'] = macd['MACDs_12_26_9']

    # Bollinger Bands avec gestion robuste des noms de colonnes
    bbands = ta.bbands(data['Close'], length=20, std=2)
    if bbands is not None and not bbands.empty:
        # Les noms peuvent être BBL_20_2.0 ou BBL_20_2 selon la version
        lower_col = [col for col in bbands.columns if 'BBL' in col or 'lower' in col.lower()]
        upper_col = [col for col in bbands.columns if 'BBU' in col or 'upper' in col.lower()]

        if lower_col and upper_col:
            data['BB_Lower'] = bbands[lower_col[0]]
            data['BB_Upper'] = bbands[upper_col[0]]
        else:
            data['BB_Lower'] = data['BB_Upper'] = np.nan
    else:
        data['BB_Lower'] = data['BB_Upper'] = np.nan

    data['ATR'] = ta.atr(data['High'], data['Low'], data['Close'], length=14)
    data['Volume_SMA_20'] = ta.sma(data['Volume'], length=20)

    latest = data.iloc[-1]

    # Liste des clés attendues avec fallback à NaN si indisponible
    return {
        'Close': latest['Close'],
        'SMA_50': latest.get('SMA_50', np.nan),
        'SMA_200': latest.get('SMA_200', np.nan),
        'EMA_20': latest.get('EMA_20', np.nan),
        'RSI': latest.get('RSI', np.nan),
        'MACD': latest.get('MACD', np.nan),
        'MACD_Signal': latest.get('MACD_Signal', np.nan),
        'BB_Lower': latest.get('BB_Lower', np.nan),
        'BB_Upper': latest.get('BB_Upper', np.nan),
        'ATR': latest.get('ATR', np.nan),
        'Volume': latest['Volume'],
        'Volume_SMA_20': latest.get('Volume_SMA_20', np.nan)
    }

# Fonction  pour prendre la décision
def make_decision(indicators: dict, sentiment: int) -> tuple[str, int]:
    buy_signals = 0
    sell_signals = 0

    # Fonction helper pour vérifier si valeur valide
    def valid(val):
        return not (val is None or np.isnan(val) or np.isinf(val))

    # Tendance long-terme (seulement si SMA_200 disponible)
    if valid(indicators['SMA_50']) and valid(indicators['SMA_200']):
        if indicators['SMA_50'] > indicators['SMA_200']:
            buy_signals += 2
        elif indicators['SMA_50'] < indicators['SMA_200']:
            sell_signals += 2

    # Prix vs EMA_20
    if valid(indicators['Close']) and valid(indicators['EMA_20']):
        if indicators['Close'] > indicators['EMA_20']:
            buy_signals += 1
        else:
            sell_signals += 1

    # RSI
    if valid(indicators['RSI']):
        if indicators['RSI'] < 30:
            buy_signals += 2
        elif 30 <= indicators['RSI'] < 40:
            buy_signals += 1
        elif indicators['RSI'] > 70:
            sell_signals += 2
        elif 60 < indicators['RSI'] <= 70:
            sell_signals += 1

    # MACD
    if valid(indicators['MACD']) and valid(indicators['MACD_Signal']):
        if indicators['MACD'] > indicators['MACD_Signal'] and indicators['MACD'] > 0:
            buy_signals += 2
        elif indicators['MACD'] > indicators['MACD_Signal']:
            buy_signals += 1
        elif indicators['MACD'] < indicators['MACD_Signal'] and indicators['MACD'] < 0:
            sell_signals += 2
        elif indicators['MACD'] < indicators['MACD_Signal']:
            sell_signals += 1

    # Bollinger Bands
    if valid(indicators['Close']) and valid(indicators['BB_Lower']) and valid(indicators['BB_Upper']):
        if indicators['Close'] <= indicators['BB_Lower']:
            buy_signals += 1
        elif indicators['Close'] >= indicators['BB_Upper']:
            sell_signals += 1

    # Volume confirmation
    if valid(indicators['Volume']) and valid(indicators['Volume_SMA_20']):
        if indicators['Volume'] > indicators['Volume_SMA_20'] * 1.5:
            if buy_signals > sell_signals:
                buy_signals += 1
            elif sell_signals > buy_signals:
                sell_signals += 1

    # Volatilité ATR
    if valid(indicators['ATR']) and valid(indicators['Close']):
        avg_atr = indicators['ATR'] / indicators['Close']
        if avg_atr > 0.05:
            buy_signals = int(buy_signals * 0.8)
            sell_signals = int(sell_signals * 0.8)

    net_score = buy_signals - sell_signals + sentiment

    if net_score >= 4:
        return 'Acheter Fort', net_score
    elif net_score > 1:
        return 'Acheter', net_score
    elif net_score <= -4:
        return 'Vendre Fort', net_score
    elif net_score < -1:
        return 'Vendre', net_score
    else:
        return 'Conserver', net_score


# Fonction principale pour analyser plusieurs actions
def run_bot(tickers: list[str], sentiments: list[int]):
    results = {
        'Acheter Fort': [],
        'Acheter': [],
        'Conserver': [],
        'Vendre': [],
        'Vendre Fort': []
    }
    scores = {}  # Pour stocker les scores et trier

    for i, ticker in enumerate(tickers):
        try:
            print(f"\nAnalyse de {ticker}...")

            # Indicateurs techniques
            indicators = calculate_indicators(ticker)
            print("\nIndicateurs techniques :")
            for key, value in indicators.items():
                print(f"{key}: {value:.2f}")

            # Sentiment
            sentiment = sentiments[i]
            print(f"Sentiment : {sentiment}")

            # Décision et score
            decision, net_score = make_decision(indicators, sentiment)
            print(f"\nDécision pour {ticker} : {decision} (score net : {net_score})")

            results[decision].append(ticker)
            scores[ticker] = net_score

        except Exception as e:
            print(f"Erreur pour {ticker} : {e}")

    # Affichage des listes, triées par score descendant pour achats, ascendant pour ventes
    print("\n" + "=" * 60)
    print("Récapitulatif :")

    # Trier achats par score descendant
    results['Acheter Fort'] = sorted(results['Acheter Fort'], key=lambda t: scores.get(t, 0), reverse=True)
    results['Acheter'] = sorted(results['Acheter'], key=lambda t: scores.get(t, 0), reverse=True)
    # Trier ventes par score ascendant (plus négatif en premier)
    results['Vendre'] = sorted(results['Vendre'], key=lambda t: scores.get(t, 0))
    results['Vendre Fort'] = sorted(results['Vendre Fort'], key=lambda t: scores.get(t, 0))

    for key, value in results.items():
        if value:  # N'afficher que si non vide
            print(f"{key} : {value}")

    # Déduire la plus intéressante (celle avec le plus haut score net parmi les achats)
    all_buys = results['Acheter Fort'] + results['Acheter']
    if all_buys:
        best_ticker = max(all_buys, key=lambda t: scores.get(t, 0))
        print(f"\nLa plus intéressante à acheter : {best_ticker} (score : {scores[best_ticker]})")
    else:
        print("\nAucune action intéressante à acheter dans cette liste.")


# Lancement
def run():
    # Liste par défaut d'actions populaires
    default_tickers = [
        'NVDA', 'PLTR', 'SMCI', 'IONQ', 'CRDO', 'MU', 'AVGO', 'AMD', 'ASML', 'TSM', 'ARM', 'QBTS', 'RGTI',
        'CRWD', 'SNOW', 'DDOG', 'ZS', 'NET', 'MSFT', 'GOOGL', 'AMZN', 'META', 'AAPL', 'ORCL', 'ADBE', 'CRM',
        'DELL', 'HPQ', 'PATH', 'GTLB', 'HUBS', 'TEAM', 'TWLO', 'RBLX', 'U', 'S', 'QCOM', 'INTC', 'CSCO', 'TSLA',
        'VRTX', 'REGN', 'CRSP', 'NTLA', 'BEAM', 'MRNA', 'BNTX', 'ILMN', 'RXRX', 'SDGR', 'EXAI', 'PACB', 'TWST',
        'LVMUY', 'HESAY', 'RMS.PA', 'CFRUY', 'BURBY', 'TPR', 'EL', 'ASTS'
    ]
    # Demande à Grok les sentiments pour la liste complète
    print("\nDemande à Grok :")
    print(f"A partir de ces devises : {', '.join(default_tickers)}")
    print(
        "Analyse chacun des sentiments de ces devises à l'aide des derniers tweets postés, des tweets des personnes influentes ainsi que de l'actualité, puis renvoie-moi une liste dans l'ordre avec un score : 5 pour les plus optimistes où tu es sûr que ça va monter, et -5 si tu es sûr que ça va descendre. Tu peux aussi choisir une valeur intermédiaire. Ne renvoie que des chiffres separes par uniquement des espaces, rien d'autre, je ne veux voir aucune devise !")
    sentiment_input = input("Réponse de Grok : ").strip()

    # Conversion en liste d'entiers avec gestion d'erreurs
    try:
        sentiments = [int(s) for s in sentiment_input.split() if s.strip()]
        if len(sentiments) != len(default_tickers):
            raise ValueError("Le nombre de sentiments ne correspond pas au nombre de tickers.")
    except ValueError as e:
        print(f"Erreur dans les sentiments : {e}")
        print("Utilise des sentiments par défaut à 0.")
        sentiments = [0] * len(default_tickers)

    # Exécution
    run_bot(default_tickers, sentiments)

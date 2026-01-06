import instaloader
def main() :
    # creer une instance instaloader
    bot = instaloader.Instaloader()
    name = input("quelle est le compte ?")
    # charge le profil puis le renvoie a l'utilisateur
    profile = instaloader.Profile.from_username(bot.context, name)
    print("nom d'utilisateur: ", profile.username)
    print("User ID: ", profile.userid)
    print("nombre de poste: ", profile.mediacount)
    print("abonner: ", profile.followers)
    print("abonnement: ", profile.followees)
    print("Biographie: ", profile.biography,profile.external_url)

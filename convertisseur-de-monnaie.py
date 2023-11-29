from forex_python.converter import CurrencyRates

def convertir(montant, devise_origine, devise_cible, taux_de_change):
    taux_origine, taux_cible = taux_de_change.get(devise_origine), taux_de_change.get(devise_cible)
    return montant * (taux_cible / taux_origine) if taux_origine is not None and taux_cible is not None else None

def sauvegarder_conversion(historique):
    with open('historique_conversion.txt', 'a') as fichier:
        fichier.writelines(f"{entree['montant']} {entree['devise_origine']} => {entree['prix_converti']:.2f} {entree['devise_cible']}\n" for entree in historique)

def sauvegarder_favoris(devise, taux_conversion):
    with open('favoris.txt', 'a') as fichier:  # j'ai ajouté un fichier favoris.txt en plus pour mettre tout ce que je met en favoris à l'intérieur !
        fichier.write(f"{devise} {taux_conversion}\n")

def charger_fichier(nom_fichier, conversion_func=None):
    try:
        with open(nom_fichier, 'r') as fichier:
            lignes = fichier.readlines()
            return [conversion_func(ligne) if conversion_func else ligne.strip() for ligne in lignes]
    except FileNotFoundError:
        return []

def ajouter_devise_preferee(devise, taux_conversion, taux_de_change_personnalise):
    taux_de_change_personnalise[devise] = taux_conversion
    sauvegarder_favoris(devise, taux_conversion)
    print(f"La devise {devise} avec un taux de conversion de {taux_conversion} a été ajoutée en favori.")

def programme_principal():
    convertisseur = CurrencyRates()
    devises_disponibles = ['USD', 'EUR', 'JPY', 'GBP', 'CAD', 'CHF', 'AUD', 'NZD', 'CNY', 'INR', 'BRL', 'ZAR', 'MXN', 'SGD', 'THB']
    print("Devises disponibles:", devises_disponibles)
    devise_origine = input("Choisissez la devise de départ : ").upper()
    devise_cible = input("Choisissez la devise d'arrivée : ").upper()

    if devise_origine not in devises_disponibles or devise_cible not in devises_disponibles:
        print("Devises invalides. Veuillez choisir parmi les devises disponibles.")
        return
    taux_de_change_origine = convertisseur.get_rates(devise_origine)
    taux_de_change_cible = convertisseur.get_rates(devise_cible)
    taux_de_change = {**taux_de_change_origine, **taux_de_change_cible}
    taux_de_change_personnalise = {}
    montant = float(input("Entrez le montant à convertir : "))
    prix_converti = convertir(montant, devise_origine, devise_cible, taux_de_change)

    if prix_converti and prix_converti != 0:
        print(f"{montant} {devise_origine} équivaut à {prix_converti:.2f} {devise_cible}")
        historique_conversion = [{'montant': montant, 'devise_origine': devise_origine, 'devise_cible': devise_cible, 'prix_converti': prix_converti}]
        ajout_devise = input("Voulez-vous ajouter cette devise en favori ? Oui ou Non ? : ").lower()
        
        if ajout_devise == 'oui':
            taux_conversion = float(input(f"Entrez le taux de conversion pour {devise_origine} : "))
            ajouter_devise_preferee(devise_origine, taux_conversion, taux_de_change_personnalise)
    else:
        print("Conversion impossible. Vérifiez les devises saisies.")

    if historique_conversion:
        sauvegarder_conversion(historique_conversion)

    print("\nHistorique des conversions :")
    print(*charger_fichier('historique_conversion.txt'), sep='\n')

programme_principal()
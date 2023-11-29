from forex_python.converter import CurrencyRates

def conversion(montant, devise_origine, devise_cible, taux_de_change):
    taux_origine = taux_de_change.get(devise_origine)
    taux_cible = taux_de_change.get(devise_cible)
    if taux_origine is not None and taux_cible is not None:
        taux = taux_cible / taux_origine
        return montant * taux
    else:
        return None

def sauvegarder_historique_conversion(historique):
    with open('historique_conversion.txt', 'a') as fichier:
        for entree in historique:
            fichier.write(f"{entree['montant']} {entree['devise_origine']} => {entree['prix_converti']:.2f} {entree['devise_cible']}\n")

def sauvegarder_favoris(devise, taux_conversion):
    with open('favoris.txt', 'a') as fichier:
        fichier.write(f"{devise} {taux_conversion}\n")

def charger_historique_conversion():
    try:
        with open('historique_conversion.txt', 'r') as fichier:
            return fichier.readlines()
    except FileNotFoundError:
        return []

def charger_favoris():
    try:
        with open('favoris.txt', 'r') as fichier:
            lignes = fichier.readlines()
            return {ligne.split()[0]: float(ligne.split()[1]) for ligne in lignes}
    except FileNotFoundError:
        return {}

def ajouter_devise_preferee(devise_preferee, taux_conversion, taux_de_change_personnalise):
    taux_de_change_personnalise[devise_preferee] = taux_conversion
    sauvegarder_favoris(devise_preferee, taux_conversion)
    print(f"La devise {devise_preferee} avec un taux de conversion de {taux_conversion} a été ajoutée en favori.")

def main():
    c = CurrencyRates()
    taux_de_change = c.get_rates('USD')
    taux_de_change_personnalise = {}
    historique_conversion = []
    montant = float(input("Entrez le montant à convertir : "))
    devise_origine = input("Entrez la devise d'origine (par exemple, JPY) : ").upper()
    devise_cible = input("Entrez la devise cible (par exemple, EUR) : ").upper()
    prix_converti = conversion(montant, devise_origine, devise_cible, taux_de_change)

    if prix_converti is not None and prix_converti != 0:
        print(f"{montant} {devise_origine} équivaut à {prix_converti:.2f} {devise_cible}")
        historique_conversion.append({
            'montant': montant,
            'devise_origine': devise_origine,
            'devise_cible': devise_cible,
            'prix_converti': prix_converti
        })
        ajout_devise = input("Voulez-vous ajouter cette devise en favori ? (Oui/Non) : ").lower()
        if ajout_devise == 'oui':
            taux_conversion = float(input(f"Entrez le taux de conversion pour la devise préférée {devise_origine} : "))
            ajouter_devise_preferee(devise_origine, taux_conversion, taux_de_change_personnalise)
    else:
        print("Conversion impossible. Vérifiez les devises saisies.")
    if historique_conversion:
        sauvegarder_historique_conversion(historique_conversion)
    print("\nHistorique des conversions :")
    for entree in charger_historique_conversion():
        print(entree.strip())

if __name__ == "__main__":
    main()
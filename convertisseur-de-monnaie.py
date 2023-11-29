from forex_python.converter import CurrencyRates

def conversion(montant, devise_origine, devise_cible, taux_de_change):
    taux_origine, taux_cible = taux_de_change.get(devise_origine), taux_de_change.get(devise_cible)
    return montant * (taux_cible / taux_origine) if taux_origine is not None and taux_cible is not None else None

def sauvegarder_historique_conversion(historique):
    with open('historique_conversion.txt', 'a') as fichier:
        fichier.writelines(f"{entree['montant']} {entree['devise_origine']} => {entree['prix_converti']:.2f} {entree['devise_cible']}\n" for entree in historique)

def sauvegarder_favoris(devise, taux_conversion):
    with open('favoris.txt', 'a') as fichier:
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

def main():
    c = CurrencyRates()
    taux_de_change = c.get_rates('USD')
    taux_de_change_personnalise = {}
    historique_conversion = []
    montant = float(input("Entrez le montant à convertir : "))
    devise_origine, devise_cible = input("Entrez la devise d'origine : ").upper(), input("Entrez la devise cible : ").upper()
    prix_converti = conversion(montant, devise_origine, devise_cible, taux_de_change)

    if prix_converti and prix_converti != 0:
        print(f"{montant} {devise_origine} équivaut à {prix_converti:.2f} {devise_cible}")
        historique_conversion.append({'montant': montant, 'devise_origine': devise_origine, 'devise_cible': devise_cible, 'prix_converti': prix_converti})
        ajout_devise = input("Voulez-vous ajouter cette devise en favori ? (Oui/Non) : ").lower()
        if ajout_devise == 'oui':
            taux_conversion = float(input(f"Entrez le taux de conversion pour {devise_origine} : "))
            ajouter_devise_preferee(devise_origine, taux_conversion, taux_de_change_personnalise)
    else:
        print("Conversion impossible. Vérifiez les devises saisies.")

    if historique_conversion:
        sauvegarder_historique_conversion(historique_conversion)
    print("\nHistorique des conversions :")
    print(*charger_fichier('historique_conversion.txt'), sep='\n')

if __name__ == "__main__":
    main()
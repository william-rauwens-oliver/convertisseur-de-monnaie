from forex_python.converter import CurrencyRates

def conversion(montant, devise_origine, devise_cible, taux_de_change):
    taux = taux_de_change.get(devise_cible) / taux_de_change.get(devise_origine)
    return montant * taux if taux else None

def sauvegarder_historique_conversion(historique):
    with open('historique_conversion.txt', 'a') as fichier:
        for entree in historique:
            fichier.write(f"{entree['montant']} {entree['devise_origine']} => {entree['prix_converti']:.2f} {entree['devise_cible']}\n")

def charger_historique_conversion():
    try:
        with open('historique_conversion.txt', 'r') as fichier:
            return fichier.readlines()
    except FileNotFoundError:
        return []

def main():
    c = CurrencyRates()
    taux_de_change = c.get_rates('USD')
    historique_conversion = []
    montant = float(input("Entrez le montant à convertir : "))
    devise_origine = input("Entrez la devise d'origine (par exemple, YEN) : ").upper()
    devise_cible = input("Entrez la devise cible (par exemple, EUR) : ").upper()
    prix_converti = conversion(montant, devise_origine, devise_cible, taux_de_change)
    
    if prix_converti is not None:
        print(f"{montant} {devise_origine} équivaut à {prix_converti:.2f} {devise_cible}")
        historique_conversion.append({
            'montant': montant,
            'devise_origine': devise_origine,
            'devise_cible': devise_cible,
            'prix_converti': prix_converti
        })
    else:
        print("Conversion impossible. Vérifiez les devises saisies.")
    sauvegarder_historique_conversion(historique_conversion)
    print("\nHistorique des conversions :")
    for entree in charger_historique_conversion():
        print(entree.strip())

if __name__ == "__main__":
    main()
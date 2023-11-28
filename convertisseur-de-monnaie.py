from forex_python.converter import CurrencyRates

def convert_currency(amount, from_currency, to_currency, exchange_rates):
    rate = exchange_rates.get(to_currency) / exchange_rates.get(from_currency)
    return amount * rate if rate else None

def save_conversion_history(history):
    with open('conversion_history.txt', 'a') as file:
        for entry in history:
            file.write(f"{entry['amount']} {entry['from_currency']} => {entry['converted_amount']:.2f} {entry['to_currency']}\n")

def load_conversion_history():
    try:
        with open('conversion_history.txt', 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def main():
    c = CurrencyRates()
    exchange_rates = c.get_rates('USD')
    conversion_history = []
    amount = float(input("Entrez le montant à convertir : "))
    from_currency = input("Entrez la devise d'origine (par exemple, USD) : ").upper()
    to_currency = input("Entrez la devise cible (par exemple, EUR) : ").upper()
    converted_amount = convert_currency(amount, from_currency, to_currency, exchange_rates)
    
    if converted_amount is not None:
        print(f"{amount} {from_currency} équivaut à {converted_amount:.2f} {to_currency}")
        conversion_history.append({
            'amount': amount,
            'from_currency': from_currency,
            'to_currency': to_currency,
            'converted_amount': converted_amount
        })
    else:
        print("Conversion impossible. Vérifiez les devises saisies.")
    save_conversion_history(conversion_history)
    print("\nHistorique des conversions :")
    for entry in load_conversion_history():
        print(entry.strip())

if __name__ == "__main__":
    main()
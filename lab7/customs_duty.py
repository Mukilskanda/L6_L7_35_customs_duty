def parse_declaration(text):
    category, value = text.split(':')
    return category.strip().lower(), float(value)

def duty_amount(text):
    value, rate = text.split('@')
    return float(value) * float(rate) / 100

def hs_chapter(code):
    return int(code.split('.')[0][:2])

def main():
    print("==== Running parse_declaration ====")
    user_input = input("Enter category:value (e.g. electronics:25000): ")
    result = parse_declaration(user_input)
    print("Category and Value:", result)

    print("\n==== Running duty_amount ====")
    user_input = input("Enter value@rate (e.g. 25000@20): ")
    result = duty_amount(user_input)
    print("Duty Amount:", result)

    print("\n==== Running hs_chapter ====")
    user_input = input("Enter an HS code (e.g. 8517.12): ")
    result = hs_chapter(user_input)
    print("Chapter:", result)

if __name__ == "__main__":
    main()

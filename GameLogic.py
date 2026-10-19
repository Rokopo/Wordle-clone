import random as r

def get_random_word():
    with open("words.txt", "r", encoding="utf-8") as file:
        linie = file.readlines()
    wordNumber = int(r.random() * len(linie))
    return linie[wordNumber].strip().lower()

def validate(userWord):
    if len(userWord) != 5:
        print("Błąd: Słowo musi mieć 5 liter")
        return False
    if not userWord.isalpha():
        print("Błąd: Słowo składa się jedynie z liter")
        return False
    return True

def check_guess(userWord, trueWord):
    userWord = userWord.strip().lower()
    if not validate(userWord):
        return None

    tab = [""] * 5
    for i in range(len(userWord)):
        if userWord[i] == trueWord[i]:
            tab[i] = "zielone"
        elif userWord[i] in trueWord:
            tab[i] = "żółte"
        else:
            tab[i] = "szare"

    print(tab)
    return tab

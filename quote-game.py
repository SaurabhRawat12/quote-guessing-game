import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictReader

BASE_URL = "http://quotes.toscrape.com/"


def read_quotes(filename):
    with open(filename, "r") as file:
        csv_reader = DictReader(file)
        return list(csv_reader)


def start_game(quotes):
    quote = choice(quotes)
    remaining_guesses = 3
    print("Here's a quote: ")
    print(quote["text"])
    # print(quote["author"])
    guess = ''
    while guess.lower() != quote["author"].lower():
        guess = input(
            f"Who said this quote? Guesses ramaining: {remaining_guesses}\n")
        if guess.lower() == quote['author'].lower():
            print("You got it right")
            break
        hint = input(f"Oops, you got it wrong. Do you want a hint?(y/n)")
        if hint.lower() in ('y', 'yes'):
            if remaining_guesses > 0:
                remaining_guesses -= 1
                print_hint(quote, remaining_guesses)
            else:
                decision = input(f"Sorry you ran out of guesses. Do you want to quit?(y/n)")
                if decision.lower() in ('y', 'yes'):
                    print(f"The answer was {quote['author']}")
                    break
                else:
                    print("Keep trying")
        else:
            print("Keep trying")

    again = ''
    while again.lower() not in ('y', 'yes', 'n', 'no'):
        again = input("Would you like to play again (y/n)?")
        if again.lower() in ('y', 'yes'):
            return start_game(quotes)
        else:
            print("OK goodbye")


def print_hint(quote, remaining_guesses):
    if remaining_guesses == 2:
        res = requests.get(f"{BASE_URL}{quote['bio-link']}")
        soup = BeautifulSoup(res.text, "html.parser")
        birth_date = soup.find(class_="author-born-date").get_text()
        birth_place = soup.find(class_="author-born-location").get_text()
        print(f"Here's a hint: The author was born on {birth_date} {birth_place}")
    elif remaining_guesses == 1:
        print(f"Here's a hint: The author's first name starts with {quote['author'][0]}")
    elif remaining_guesses == 0:
        last_initial = quote['author'].split(" ")[1][0]
        print(f"Here's a hint: The author's last name starts with {last_initial}")


quotes = read_quotes("quotes.csv")
start_game(quotes)

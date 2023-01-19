from bs4 import BeautifulSoup
import requests
from random import choice
import csv


def fetchData():
    """
    Requests quote data from each page in 'http://quotes.toscrape.com/' and compiles it
    into a csv file
    """
    baseURL = 'http://quotes.toscrape.com/'
    URL = '/page/1'
    userInput = input('Do you want to fetch the data? y/n  ')
    if userInput.lower() == 'y':
        print('Fetching data...')
        with open("quotes.csv", "w+", encoding="utf-8", newline='') as csvFile:
            csvWriter = csv.writer(csvFile)
            csvWriter.writerow(['quote', 'quoteAuthor', 'bioURL'])

            while URL:
                print(f'Fetching {URL}')
                html = requests.get(baseURL + URL)
                soup = BeautifulSoup(html.text, "html.parser")
                quotes = soup.findAll('div', class_='quote')
                for quote in quotes:
                    quoteText = quote.find(class_='text').getText()
                    # print(quoteText)
                    quoteAuthor = quote.find(class_='author').getText()
                    # print(quoteAuthor)
                    bioURL = quote.find('a')['href']
                    csvWriter.writerow([quoteText, quoteAuthor, bioURL])

                nextBtn = soup.find(class_='next')
                if nextBtn:
                    URL = nextBtn.find('a')['href']
                else:
                    URL = ''


class Game:
    def __init__(self):
        print('Starting game...')
        with open('quotes.csv', 'r', encoding="utf-8") as csvFile:
            self.csvReader = csv.reader(csvFile)
            self.lines = [row for row in self.csvReader]
            self.baseURL = 'http://quotes.toscrape.com/'
            self._initGame()

    def playGame(self):
        print(f'Who said: {self.quote}?\n')
        while self.guesses > 0:
            if self.guesses != 1:
                print(f'{self.guesses} guesses remaining.')
            else:
                print(f'{self.guesses} guess remaining')
            guess = input()
            self.guesses -= 1
            if guess.lower() == self.author.lower():
                print("Congratulations you got it!!!")
                break
            elif self.guesses == 3:
                print(f"Their date of birth is {self.birthDate}")
            elif self.guesses == 2:

                print(f"They were born {self.birthLocation}")
            elif self.guesses == 1:
                print(
                    f"The initials for their first and last name are {self.authorFirstInitial} and "
                    f"{self.authorSecondInitial}")
            else:
                print(f'Better luck next time. The author of the quote was {self.author}')
        self.playAgain()

    def playAgain(self):
        playAgain = input("Do you want to play again? y/n  ")
        if playAgain.lower() == 'y':
            self._initGame()
            self.playGame()

    def _initGame(self):
        self.rndQuote = choice(self.lines)
        self.quote = self.rndQuote[0]
        self.author = self.rndQuote[1]
        self.bioLink = self.rndQuote[2]
        self.guesses = 4
        self.authorWordList = self.author.split()
        self.authorFirstInitial = self.author[0]
        self.authorSecondInitial = self.authorWordList[-1][0]
        self.authorInfo = requests.get(self.baseURL + self.bioLink)
        self.authorSoup = BeautifulSoup(self.authorInfo.text, "html.parser")
        self.birthDate = self.authorSoup.find(class_='author-born-date').getText()
        self.birthLocation = self.authorSoup.find(class_='author-born-location').getText()

# loading bars in the terminal rather than writing
# help function to display what the program does
# comment my code!!
# implement try and catch blocks
# upload to gitHub
# unit testing using pytest and make code robust! check timeouts and user inputs
# add a readme file, a small paragraph or two. markdown file (.md) or ascii (.adoc)


if __name__ == '__main__':
    # fetchData()
    # game = Game()
    # game.playGame()
    help(fetchData)

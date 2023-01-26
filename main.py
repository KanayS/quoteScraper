from bs4 import BeautifulSoup
import requests
from random import choice
import csv
from time import sleep
from tqdm import tqdm


class Game:
    """
    The Game class uses the quotes.csv file to create a quote author guessing game.
    Each time an incorrect guess is made, clues are provided and the user ultimately has 4 chances
    to guess correctly before the answer is given.
    """

    def __init__(self):
        self.URL = '/page/1'
        self.csvWriter = None
        self.html = None
        self.soup = None
        self.quotes = None
        self.quoteText = None
        self.quoteAuthor = None
        self.bioURL = None
        try:
            self._readCSV()
        except FileNotFoundError:
            print('No CSV file found, please import the data')
        self.baseURL = 'http://quotes.toscrape.com/'

    def _readCSV(self):
        with open('quotes.csv', 'r', encoding="utf-8") as csvFile:
            self.csvReader = csv.reader(csvFile)
            # transforms the csv file into a list for each row NOT including the header
            self.lines = [row for row in self.csvReader][1:]

    def fetchData(self):
        """
        Requests quote data from each page in 'http://quotes.toscrape.com/' and compiles it
        into a csv file named "quotes.csv" with the headers "quote, quoteAuthor and bioURL".
        No arguments are required to run this function.
        """

        userInput = input('Do you want to fetch the data? y/n  ')
        if userInput.lower() == 'y':
            print('Fetching data...')
            # creates or writes from beginning into quotes.csv and adds headers
            with open("quotes.csv", "w+", encoding="utf-8", newline='') as self.csvFile:
                self.csvWriter = csv.writer(self.csvFile)
                self.csvWriter.writerow(['quote', 'quoteAuthor', 'bioURL'])
                # while the url is not empty, get data from the page and scrape it into the csv file
                with tqdm(total=100) as pbar:
                    while self.URL:
                        # print(f'Fetching {self.URL}')
                        self.html = requests.get(self.baseURL + self.URL)
                        self.soup = BeautifulSoup(self.html.text, "html.parser")
                        # returns a list of html elements inside a quote class
                        self.quotes = self.soup.findAll('div', class_='quote')
                        # iterates and scrapes the inner text of the html and saves it to a row in
                        # the csv file
                        for quote in self.quotes:
                            pbar.update(1)
                            sleep(0.01)
                            self.quoteText = quote.find(class_='text').getText()
                            # print(quoteText)
                            self.quoteAuthor = quote.find(class_='author').getText()
                            # print(quoteAuthor)
                            self.bioURL = quote.find('a')['href']
                            self.csvWriter.writerow([self.quoteText, self.quoteAuthor, self.bioURL])
                        # looks for the html for the hyperlink in the next page button, if there is none it
                        # means it is scraping the final page
                        nextBtn = self.soup.find(class_='next')
                        if nextBtn:
                            self.URL = nextBtn.find('a')['href']
                        else:
                            self.URL = ''
            self._readCSV()

    def playGame(self):
        """
        Starts the quote guessing game in which the user guesses who the author of the quote is.
        The first failed guess gives them a hint of their date of birth. The second tells the user
        the author's birth location and the 3rd failed guess gives the authors initials.
        """
        self._initGame()
        print('Starting game...')
        print(f'Who said: {self.quote}?\n')
        while self.guesses > 0:
            if self.guesses != 1:
                print(f'{self.guesses} guesses remaining.')
            else:
                print(f'{self.guesses} guess remaining')
            guess = input()
            # reduces guesses after the user gives an input and, depending on how many guesses are left,
            # a clue is given.
            self.guesses -= 1
            if guess.lower() == self.author.lower():
                print("Congratulations you got it!!!")
                # exits the loop prematurely if the user guesses correctly
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
        # prompts the user asking if they want to play again after the round is over
        self._playAgain()

    def _playAgain(self):
        """
        Picks another quote from the csv file and initialises the game
        """
        playAgain = input('Do you want to play again? y/n  ')
        if playAgain.lower() == 'y':
            # picks a new quote from the list and finds its corresponding data, then starts the game
            self.playGame()
        else:
            print('Thanks for playing!')

    def _initGame(self):
        """
        Initialises the game by randomly picking a row from quotes.csv. It requests the author's
        birthdate and location based on the URL provided in the csv file. This is then used to
        play the game
        """
        # translates the csv into their own variables to be outputted
        if self.lines:
            self.rndQuote = choice(self.lines)
            self.quote = self.rndQuote[0]
            self.author = self.rndQuote[1]
            self.bioLink = self.rndQuote[2]
            self.guesses = 4
            self.authorFirstInitial = self.author[0]
            # creates a list of each word in the authors name and selects the first letter from the last word
            self.authorSecondInitial = self.author.split()[-1][0]
            self.authorInfo = requests.get(self.baseURL + self.bioLink)
            self.authorSoup = BeautifulSoup(self.authorInfo.text, "html.parser")
            self.birthDate = self.authorSoup.find(class_='author-born-date').getText()
            self.birthLocation = self.authorSoup.find(class_='author-born-location').getText()


if __name__ == '__main__':
    game = Game()
    game.fetchData()
    game.playGame()

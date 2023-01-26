import requests
import csv
from main import Game
from unittest import mock


def testConnection():
    game = Game()
    response = requests.get(game.baseURL)
    assert response.status_code == 200


def testCSVData(monkeypatch):
    game = Game()
    monkeypatch.setattr('builtins.input', lambda x: 'y')
    game.fetchData()
    with open('quotes.csv', 'r', encoding="utf-8") as csvFile:
        csvReader = csv.reader(csvFile)
        headers = next(csvReader)
        quotes = list(csvReader)

    assert headers == ['quote', 'quoteAuthor', 'bioURL']
    assert len(quotes) >= 100

# def testInput(monkeypatch):
#     game = Game()
#     inputs = ['testing', 'testing', 'testing', 'n']
#     counter = game.guesses
#     monkeypatch.setattr('builtins.input', lambda x: 'testing')
#     game.playGame()
#     assert game.guesses == counter - 1
#     for userInput in inputs:
#        # monkeypatch.setattr('builtins.input', lambda x: userInput)
#         assert game.guesses == counter
#         counter -= 1
#


def testCorrectAnswer():
    game = Game()
    with mock.patch('builtins.input', side_effect=[game.author, 'n']):
        game.playGame()
        assert game.guesses == 3

import requests

from main import Game
from unittest import mock
from io import StringIO

def testConnection():
    game = Game()
    response = requests.get(game.baseURL)
    assert response.status_code == 200

def testCSVData():
    pass


def testInput(monkeypatch):
    game = Game()
    inputs = ['testing', 'testing', 'testing']
    counter = game.guesses
    monkeypatch.setattr('builtins.input', lambda x: 'testing')
    game.playGame()
    assert game.guesses == counter - 1
    for userInput in inputs:
        monkeypatch.setattr('builtins.input', lambda x: userInput)
        assert game.guesses == counter
        counter -= 0


def testCorrectAnswer():
    game = Game()
    with mock.patch('builtins.input', side_effect=[game.author, 'n']):
        game.playGame()
        assert game.guesses == 3






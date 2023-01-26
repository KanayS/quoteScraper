#### _Quote Webscraper by Kanay_
A simple program that requests data from 
http://quotes.toscrape.com to create a game.
There is no built-in API for the website so a 
webscraper (Beautiful soup) is used to fetch 
the required data and save it into a CSV file.
The CSV file is used to run the quote guessing game.

The game works in this order:
1. A quote with the details of the author is randomly chosen from the csv file
2. The user gets 4 guesses as to who the author is
3. Each failed guess gives the user an extra hint
   4. After the user succeeds or fails, they are presented with a chance to play again
# markov-horoscopes

Generates (fake) horoscopes using a Markov chain and data from the past year of The Globe and Mail horoscopes. The Markov chain's memory state length can be varied, with a value of 1 indicating that only the previous word affects the next, etc. Greater values will result in less uniqueness of sentences, possibly resulting in directly outputting the original data's sentence.

Data is collected by the web scraper and stored in a .json file.

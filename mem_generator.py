import json
import unidecode
from collections import defaultdict, Counter
import random

# List of tuples of starting words
starting_states = []
STATE_LENGTH = 3

def load_data(dfile):
    """
    Loads the data from a json file.
    """
    with open(dfile) as json_data:
        jsonData = json.load(json_data)
    return jsonData


def toSentences(json_data):
    """
    Creates parsed list of strings. This method splits sentences by the '.'
    character (but adds it back).
    Removes parentheses.
    """
    corpus = ""
    for i in json_data:
        corpus += i["text"]

    corpus = unidecode.unidecode(corpus)
    lines = [e+'.' for e in corpus.split('.') if e]
    sentences = []
    for line in lines:
        sentences.append(line.strip())

    return sentences

def addWordsToMapping(sentence, markov_dict):
    """
    Adds the sentence to the markov defaultdict.
    Adds first state of sentence to starting_states list.
    """

    words = sentence.split(' ')

    start = words[:STATE_LENGTH]
    starting_states.append(tuple(start))

    for i in range(len(words) - STATE_LENGTH):
        curr_state = tuple(words[i:i + STATE_LENGTH])
        next_word = words[i + STATE_LENGTH]
        markov_dict[curr_state][next_word] += 1

    return markov_dict

def createDict(sentence_list):
    """
    Creates a Counter defaultdict and calls the addWordsToMapping method. Converts
    the Markov defaultdict to a Markov dictionary and returns it.
    """
    markov_dict = defaultdict(Counter)
    for sentence in sentence_list:
        # add sentence to map
        addWordsToMapping(sentence, markov_dict)

    #convert defaultdict to dict
    m_dict = dict(markov_dict)
    return m_dict


def sentenceCreator(m_dict):
    """
    Create a sentence based on the starting_states list and Markov dictionary.
    """

    sentence = ""
    punct = {'.', '!', '?'}

    # Pick a random starting state
    # Each starting state is a list of STATE_LENGTH words, concat each word
    curr_state = random.choice(starting_states)
    for word in curr_state:
        sentence += ' ' + word


    # Generate next word using dictionary and previous state.
    while sentence[-1] not in punct:

        next_options = m_dict[curr_state]

        # Choose next word based on weights
        next_word = random.choices(list(next_options), next_options.values())

        # Add to sentence
        sentence += ' ' + next_word[0]
        # Update current state to reflect added word
        # Turn
        curr_state_list = list(curr_state[1:])
        curr_state_list.append(next_word[0])
        curr_state = tuple(curr_state_list)


    sentence.strip()
    return sentence



def generateHoroscope():
    """
    Generate the horoscope.
    """

    print("Loading data...")
    data = load_data('theglobeandmail.json')

    # parse data
    print("Parsing data...")
    sentence_list = toSentences(data)

    # create markov counter dict
    print("Learning model...")
    m_dict = createDict(sentence_list)

    print("Generating horoscope...")
    # generate sentence
    horoscope = sentenceCreator(m_dict)
    print(horoscope)



def main():
    generateHoroscope()

if __name__ == "__main__":
    main()

'''
Created on Aug 8, 2016

@author: ian
'''

def words_by_length(words_filepath='./resources/words.txt'):
    sorted_words = {}

    with open(words_filepath, 'r') as words_file:
        for line in words_file:
            stripped_line = line.strip().replace("'", '')
            word_length = len(stripped_line)

            if not word_length in sorted_words:
                sorted_words[word_length] = []

            if stripped_line in sorted_words[word_length]:
                continue

            sorted_words[word_length].append(stripped_line)

    return sorted_words


def trim_words_file(words_filepath='./resources/words.txt'):
    words = words_by_length(words_filepath)
    
    with open(words_filepath, 'w') as words_file:
        for current_words in words.itervalues():
            words_file.write('\n'.join(current_words[:250]) + '\n')
            
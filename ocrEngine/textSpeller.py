import pyaspeller

def correct_spelling(text):
    checker = pyaspeller.YandexSpeller()
    # Get the list of misspelled words and their corrections
    result = checker.spell(text)
    corrected_text = text
    offset = 0  # Offset to adjust for changes in string length
    for item in result:
        if item['s']:
            incorrect_word = item['word']
            correct_word = item['s'][0]
            start_pos = item['pos'] + offset
            end_pos = start_pos + len(incorrect_word)
            corrected_text = corrected_text[:start_pos] + correct_word + corrected_text[end_pos:]
            offset += len(correct_word) - len(incorrect_word)
    return corrected_text

def check_accuracy(text):
    checker = pyaspeller.YandexSpeller()
    # Get the list of misspelled words
    result = checker.spell(text)
    total_words = len(text.split())
    if total_words == 0:
        return 0.0
    incorrect_words = sum(1 for item in result if item['s'])
    accuracy = (total_words - incorrect_words) / total_words * 100
    return accuracy
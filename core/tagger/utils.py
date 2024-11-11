import csv

from tagger.models import Sentence, Dataset


def read_sentences(dataset: Dataset, decoded_file) -> list[Sentence]:
    """
    reads sentences from a csv file and returns a list of sentences.
    """
    reader = csv.reader(decoded_file)
    sentences = []
    for row in reader:
        if row:
            sentence_body = row[0]
            sentences.append(Sentence(body=sentence_body, dataset=dataset))
    return sentences

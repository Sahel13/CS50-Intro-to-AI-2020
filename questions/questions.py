import nltk
import sys
import os
import math
import string

FILE_MATCHES = 4
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)
    print()


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    for filename in os.listdir(directory):
        f = open(os.path.join(directory, filename))
        files[filename] = f.read()
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    allwords = nltk.tokenize.word_tokenize(document)
    words = []
    for word in allwords:
        if (word not in string.punctuation) and (word not in nltk.corpus.stopwords.words("english")):
            words.append(word.lower())
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    wordsIDF = dict()
    totalDocuments = len(documents)

    for document in documents:
        # Remove duplicates in a single document
        documents[document] = list(set(documents[document]))
        for word in documents[document]:
            if word not in wordsIDF:
                wordsIDF[word] = 1
            else:
                wordsIDF[word] += 1
    
    for word in wordsIDF:
        wordsIDF[word] = math.log(totalDocuments / wordsIDF[word])
    return wordsIDF


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    rankings = dict()
    for document in files:
        tf_idf = 0
        for queryWord in query:
            idf = idfs[queryWord]
            count = 0
            for word in files[document]:
                if word == queryWord:
                    count += 1
            tf_idf += (idf * count)
        rankings[document] = tf_idf
    sortedRankings = [k for k,v in sorted(rankings.items(), key=lambda item: item[1], reverse=True)]
    return sortedRankings[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    rankings = dict()
    for sentence in sentences:
        idf = 0
        sentWords = sentences[sentence]
        count = 0
        for queryWord in query:
            if queryWord in sentWords:
                idf += idfs[queryWord]
                count += 1
        queryTermDensity = count / len(sentWords)
        rankings[sentence] = [idf, queryTermDensity]
    # Order based on queryTermDensity
    sortedRankings = {k: v for k, v in sorted(rankings.items(), key=lambda item: item[1][1], reverse=True)}
    # Order based on idf value
    sortedRankings = [k for k, v in sorted(sortedRankings.items(), key=lambda item: item[1][0], reverse=True)]
    return sortedRankings[:n]


if __name__ == "__main__":
    main()

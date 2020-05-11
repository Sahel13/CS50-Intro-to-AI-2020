import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])

    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    allPages = corpus.keys()
    linkedPages = corpus[page]
    numCorpus = len(corpus)
    numLinked = len(linkedPages)
    probabilities = {}

    # If the page has no links
    if not linkedPages:
        prob = 1/numCorpus
        for page in allPages:
            probabilities[page] = prob
    else:
        for page in allPages:
            if page in linkedPages:
                prob = (1 - damping_factor)/numCorpus + damping_factor/numLinked
            else:
                prob = (1 - damping_factor)/numCorpus
            probabilities[page] = prob
    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    listOfPages = []
    dictToReturn = {}
    allPages = corpus.keys()

    start = random.choice(list(allPages))
    listOfPages.append(start)
    page = start
    for i in range(n - 1):
        transModel = transition_model(corpus, page, damping_factor)
        newPage = random.choices(list(transModel.keys()), list(transModel.values()))
        page = newPage[0]
        listOfPages.append(page)
    for page in allPages:
        count = 0
        for element in listOfPages:
            if element == page:
                count += 1
        dictToReturn[page] = count/n
    return dictToReturn
            

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    numCorpus = len(corpus)
    allPages = corpus.keys()

    # Initializing required dictionaries
    listOfParents = dict()
    NumLinks = dict()
    currentPageRank = dict()
    nextPageRank = dict()
    
    for page in allPages:
        listOfParents[page] = []
        NumLinks[page] = len(corpus[page])
        currentPageRank[page] = 1/numCorpus
        nextPageRank[page] = 1/numCorpus

        # If the page has no links
        if NumLinks[page] == 0:
            for otherPages in allPages:
                corpus[page].add(otherPages)
            NumLinks[page] = numCorpus

    # Need to know the list of pages from which we can get to the current page
    for parent in allPages:
        for child in corpus[parent]:
            listOfParents[child].append(parent)

    constVal = ((1/damping_factor) - 1)/numCorpus

    # Iterating code
    while True:
        for page in allPages:
            currentPageRank[page] = nextPageRank[page]
            pRValue = constVal
            for parent in listOfParents[page]:
                pRValue += currentPageRank[parent]/NumLinks[parent]
            nextPageRank[page] = damping_factor * pRValue
        
        checkList = []
        for page in allPages:
            if abs(nextPageRank[page] - currentPageRank[page]) <= 0.001:
                checkList.append(True)
            else:
                checkList.append(False)
        if all(checkList):
            break
    return nextPageRank
    

if __name__ == "__main__":
    main()

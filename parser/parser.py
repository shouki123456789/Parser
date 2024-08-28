import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
NP -> Det N | Det AdjP N | N | NP PP
VP -> V | V NP PP| V AdvP | VP Conj VP | V PP |V AdvP PP
PP -> P NP
AdjP -> Adj | Adj adjP
AdvP -> Adv | Adv AdvP |Adv advP PP 
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    #convert the sentence to lowercase
    sentence = sentence.lower()
    
    #tokenize the sentence into words
    words = nltk.word_tokenize(sentence)
   
    new_words = []

    for word in words:
        
        #check if the word contains at least one alphabetic charecter
        if any(c.isalpha() for c in word):
           new_words.append(word)
    return new_words
def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []

    # Get all subtrees in the main tree
    for subtree in tree.subtrees():
        # Check if the subtree is labeled 'NP'
        if subtree.label() == 'NP':
            # Initialize a flag to track if there's a nested NP
            nested_np = False

            # Check for nested NP subtrees
            for st in subtree.subtrees():
                if st != subtree and st.label() == 'NP':
                    nested_np = True
                    break  # No need to check further if a nested NP is found

            # If no nested NP is found, add the subtree to chunks
            if not nested_np:
                chunks.append(subtree)

    return chunks

if __name__ == "__main__":
    main()
 # type: ignore
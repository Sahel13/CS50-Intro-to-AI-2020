from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Every character is a knight or a knave but not both
base_knowledge = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave))
)

# If someone said something, it's true if it's a knight, false if it's a knave
def someoneSaid(who, what):
    knight = Symbol(f"{who} is a Knight")
    knave = Symbol(f"{who} is a Knave")
    return And(
        Implication(knight, what),
        Implication(knave, Not(what))
    )

# Puzzle 0
# A says "I am both a knight and a knave."
A0said = And(AKnave, AKnight)
knowledge0 = And(
    base_knowledge,
    someoneSaid('A', A0said)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
A1said = And(AKnave, BKnave)
knowledge1 = And(
    base_knowledge,
    someoneSaid('A', A1said)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
A2said = Or(And(AKnave, BKnave), And(AKnight, BKnight))
B2said = Or(And(AKnave, BKnight), And(AKnight, BKnave))
knowledge2 = And(
    base_knowledge,
    someoneSaid('A', A2said),
    someoneSaid('B', B2said)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
AsaidKnave = AKnave
AsaidKnight = AKnight
B3said = CKnave
C3said = AKnight
knowledge3 = And(
    base_knowledge,
    someoneSaid('C', C3said),
    someoneSaid('B', B3said),
    # If B is a knight, then A did in fact say 'I am a knave'
    Implication(BKnight, someoneSaid('A', AsaidKnave)),
    # else if B is a knave, then A actually said 'I am a knight'
    Implication(BKnave, someoneSaid('A', AsaidKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()

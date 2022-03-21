from copy import deepcopy


class State:
    def __init__(self, left=None, right=None, boat=None):
        self.left = [0, 0, 0, 1, 1, 1] if left is None else left
        self.right = [] if right is None else right
        self.boat = "left" if boat is None else boat

    def printState(self):
        print(self.showStateSimple())

    def showStateSimple(self):
        return self.left, "_ " if self.boat == 'left' else " _", self.right

    def getSides(self):
        return (self.left, self.right) if self.boat == "left" else (self.right, self.left)

    def switchBoatSide(self):
        self.boat = "right" if self.boat == 'left' else "left"

    def move(self, *eles):
        _from, to = self.getSides()

        if len(eles) == 2:
            if eles[0] == eles[1] and _from.count(eles[0]) < 2:  # not enough people on the shore
                return False

            if eles[0] not in _from or eles[1] not in _from:  # person not on the shore
                return False
        else:
            if eles[0] not in _from:  # person not on the shore
                return False

        # move people
        for ele in eles:
            _from.remove(ele)
            to.append(ele)

        if isGameOver(self):
            return False

        self.switchBoatSide()
        return True


def isGameOver(s: State):
    # for each shore, check if game is over
    for shore in s.getSides():
        if shore.count(1) > 0 and shore.count(0) > 0:
            if shore.count(1) > shore.count(0):  # there are more devils than priests on one shore
                return True

    return False


def isWin(s):
    if len(s.left) == 0:  # if there is no one on the starting side of the shore (left), game is won!
        print(f"\n\n{s.showStateSimple()}\nGame won!!\n")
        return True
    return False


def row(s, eles) -> State:
    startState = deepcopy(s)

    # if move results in game over, return earlier state
    if not s.move(*eles):
        print(f"{eles} is game over")
        return startState

    return s


def manualPlay(s: State):
    if isGameOver(s):
        return False

    if isWin(s):
        return True
    s.printState()

    choice = input(printManualPlayMenu())

    if choice == "1":
        manualPlay(row(s, [0]))  # send 0

    if choice == "2":
        manualPlay(row(s, [0, 0]))  # send 0 0

    if choice == "3":
        manualPlay(row(s, [1]))  # send 1

    if choice == "4":
        manualPlay(row(s, [1, 1]))  # send 1 1

    if choice == "5":
        manualPlay(row(s, [0, 1]))  # send 0 1

    if choice == "R":
        print("\n## New Game ##")  # reset

        manualPlay(State())

    if choice == "0":
        return False


possible_moves = [[0], [0, 0], [1], [1, 1], [0, 1]]
seen, q = [], []
ctr = 0


def solve(s: State, mode="dfs", verbose=False):
    global ctr
    if isWin(s):
        print(f"{mode} took {ctr} steps")
        return True

    ctr += 1
    print(f"\nTrying moves for \n{s.showStateSimple()}\n") if verbose else ""

    for m in possible_moves:
        # create a copy of s, instead of a reference
        temp_s = deepcopy(s)

        # check if move is valid
        if temp_s.move(*m):
            t = (temp_s.showStateSimple(), m)  # tuple
            if t not in seen:
                q.append(temp_s)
                seen.append(t)

    dataStruct = 'stack' if mode == 'dfs' else 'queue'

    if verbose:
        print(f"\nMoves on {dataStruct}:")
        for x in q:
            print(f"{x.showStateSimple()}")

    print(f"Number of moves on {dataStruct}: {len(q)}")

    # dfs pops last (lifo), bfs pops first (fifo)
    solve(q.pop((len(q) - 1) if mode == 'dfs' else 0), mode, verbose)


def printMenu():
    return """
    1  - Play
    2  - Solve using DFS
    2v - Solve using DFS (Verbose)
    3  - Solve using BFS
    3v - Solve using BFS (Verbose)
    T  - Thoughts
    0 - exit

    """


def printManualPlayMenu():
    return """
    1 - send 1 priest 🕋
    2 - send 2 priests 🕋
    3 - send 1 devil 👿
    4 - send 2 devils 👿
    5 - send 1 priest + 1 devil ☯
    R - reset
    0 - exit

    """


def printThoughts():
    return """
                                Thoughts

        Depth-first Search uses a Stack - Last In First Out (LIFO)
        Breadth-first Search uses a Queue - First In First Out (FIFO)

        For this problem in particular, DFS takes significantly less 
        steps than BFS. This happens because BFS is an algorithm that
        'digs down' on the tree of possible moves, while DFS checks 
        every single move for each state, thus finding the solution 
        as soon as it appears, while BFS is busy making (possibly 
        useless) moves.

        bj - pp
"""


if __name__ == '__main__':
    while (menu := input(printMenu())) != "0":

        q, seen = [], []
        ctr = 0
        print(menu)

        if menu == "1":
            manual = True
            while manual:
                print("\n## New Game ##")
                manual = manualPlay(State())

        if menu == "2":
            solve(State(), "dfs")

        if menu == "3":
            solve(State(), "bfs")

        if menu == "2b":
            solve(State(), "dfs", True)

        if menu == "3b":
            solve(State(), "bfs", True)

        if menu == "T":
            print(printThoughts())

    print("goodbye 👋")

# TODO : add hints (right answer for each step)
# TODO : graphs for # of moves in queue
# TODO : add list to store solution moves

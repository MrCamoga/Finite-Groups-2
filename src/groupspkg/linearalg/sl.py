from groups import Group, GL

class SL(Group):
    def __init__(self, n, k):
        G = GL(n, k)
        # G = Quotient(GL)  # TODO
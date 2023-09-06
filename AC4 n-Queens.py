import matplotlib as mpl
from matplotlib import pyplot

n = 5


def display(doms, fail=False):
    board = []
    for b in doms:
        l = b.domain
        row = [-2 for i in range(len(doms))]
        for o in l:
            if len(l) > 1:
                row[o] = 2
            else:
                row[o] = 0
        board.append(row)

    if fail:
        cmap = mpl.colors.ListedColormap(['black', 'red', 'orange'])
        pyplot.title("FAIL")
    else:
        cmap = mpl.colors.ListedColormap(['black', 'lime', 'cyan'])
        pyplot.title("SOLUTION FOUND")

    bounds = [-2, -1, 1, 2]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    img = pyplot.imshow(board, interpolation='nearest', cmap=cmap, norm=norm)

    for index in range(n):
        pyplot.axhline(y=(index + 0.5), color='w', linestyle='-')
        pyplot.axvline(x=(index + 0.5), color='w', linestyle='-')

    pyplot.show()


class Domain:

    def __init__(self, index, dom):
        self.domain = dom
        self.index = index
        self.sat = {}
        self.M = {}
        for d in self.domain:
            self.M[d] = 0
            self.sat[d] = []


L = []


class Constraint:
    def __init__(self, A, B, constraint_func, reverse=False):
        self.a = A
        self.b = B
        self.reverse = reverse

        self.constraint = constraint_func
        self.counter = {}
        for a in self.a.domain:
            self.counter[a] = 0

    def run_constraint(self, a, b):
        if self.reverse:
            return self.constraint([a[0], -1 * a[1]], [b[0], -1 * b[1]])
        else:
            return self.constraint(a, b)

    def checkConstraintDomains(self):
        for a in self.a.domain:
            for b in self.b.domain:
                if self.run_constraint([self.a.index, a], [self.b.index, b]):
                    self.counter[a] += 1
                    self.b.sat[b].append([self.a, a])
            if self.counter[a] == 0:
                self.a.M[a] = 1
                L.append((self.a, a))
        self.a.domain = [aa for aa in self.a.M if self.a.M[aa] == 0]
        if len(self.a.domain) == 0:
            display(domains, fail=True)
            exit(69)

    def output_counter(self):
        for i in self.counter:
            print(f'x{self.a.index} -> x{self.b.index} {i} : {self.counter[i]}')
        print(self.counter)

    def create_reverse_arc(self):
        return Constraint(self.b, self.a, self.constraint, True)


def lt(a, b):
    return a[1] < b[1]


def gt(a, b):
    return a[1] > b[1]


def qconstraint(a, b):
    xi = a[1]
    xj = b[1]
    i = a[0]
    j = b[0]
    return (xi != xj) and (xj != (xi + j - i)) and (xj != xi - (j - i))


domains = []

domains.append(Domain(0, [4]))
domains.append(Domain(1, [2]))
domains.append(Domain(2, [ii for ii in range(n)]))
domains.append(Domain(3, [ii for ii in range(n)]))
domains.append(Domain(4, [ii for ii in range(n)]))

constraints = []

for y in range(n):
    for x in range(n):
        if x < y:
            constraints.append(Constraint(domains[x], domains[y], qconstraint))

nc = [c for c in constraints]
for c in constraints:
    nc.append(c.create_reverse_arc())
constraints = nc

print("original input")
for d in domains:
    print(d.domain)

for c in constraints:
    c.checkConstraintDomains()

print("initialized input")
for d in domains:
    print(d.domain)

while len(L) != 0:
    p = L.pop()  # L =  <xj, dj>
    # for <xi, di> in S[xj,dj]> (formatted as xj.S[dj] here)
    for sa in p[0].sat[p[1]]:
        for i in range(len(constraints)):
            if constraints[i].b == p[0] and constraints[i].a == sa[0]:
                constraints[i].counter[sa[1]] -= 1
                if constraints[i].counter[sa[1]] == 0 and sa[1] in constraints[i].a.domain:
                    L.append(sa)
                    constraints[i].a.domain.remove(sa[1])
                    if len(constraints[i].a.domain) == 0:
                        display(domains, fail=True)
                        exit(69)
print("final output")
for d in domains:
    print(d.domain)

display(domains)

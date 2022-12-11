
from bauhaus import Encoding, proposition, constraint, print_theory
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

HOUSE           = [1, 2, 3, 4, 5]
NATIONALITY     = ["Dane", "Englishman", "German", "Swede", "Norwegian"]
COLOUR          = ["blue", "green", "red", "white", "yellow"]
DRINK           = ["beer", "coffee", "milk", "tea", "water"]
CIGARETTE       = ["Blend", "BlueMaster", "Dunhill", "PallMall", "Prince"]
PET             = ["birds", "cats", "dogs", "fish", "horses"]

class Unique(object):
    def __hash__(self):
        return hash(str(self))
    def __eq__(self, other):
        return hash(self) == hash(other)
    def __repr__(self):
        return str(self)
    def __str__(self):
        assert False, "You need to define the __str__ function on a proposition class"

####################################
# CLASSES FOR ATOMIC PROPOSITIONS
####################################
@proposition(E)
class Nat(Unique):
    def __init__(self,id,nat):
        self.id = id
        self.nat = nat

    def __str__(self):
        return f"H{self.id}:{self.nat},_,_,_,_"

@proposition(E)
class Col(Unique):
    def __init__(self,id,col):
        self.id = id
        self.col = col

    def __str__(self):
        return f"H{self.id}:_,{self.col},_,_,_"

@proposition(E)
class Dri(Unique):
    def __init__(self,id,dri):
        self.id = id
        self.dri = dri

    def __str__(self):
        return f"H{self.id}:_,_,{self.dri},_,_"

@proposition(E)
class Cig(Unique):
    def __init__(self,id,cig):
        self.id = id
        self.cig = cig

    def __str__(self):
        return f"H{self.id}:_,_,_,{self.cig},_"

@proposition(E)
class Pet(Unique):
    def __init__(self,id,pet):
        self.id = id
        self.pet = pet

    def __str__(self):
        return f"H{self.id}:_,_,_,_,{self.pet}"


####################################
# CONSTRAINTS
####################################

# C1: "The Englishman lives in the red house"
constraint.add_exactly_one(E, [(Nat(id,"Englishman") & Col(id,"red")) for id in HOUSE])

# C2: "The Swede keeps dogs"
# constraint.add_exactly_one(E, [(Nat(id,"Swede") & Pet(id,"dogs")) for id in HOUSE])

# C3: "The Dane drinks tea"
# constraint.add_exactly_one(E, [(Nat(id,"Dane") & Dri(id,"tea")) for id in HOUSE])

# C4: "The green house is just to the left of the white one"
# constraint.add_exactly_one(E, [(Col(id,"green") & Col(id+1,"white")) for id in HOUSE])

# C5: "The owner of the green house drinks coffee"
# constraint.add_exactly_one(E, [(Col(id,"green") & Dri(id,"coffee")) for id in HOUSE])

# C6: "The Pall Mall smoker keeps birds"
# constraint.add_exactly_one(E, [(Cig(id,"PallMall") & Pet(id,"birds")) for id in HOUSE])

# C7: "The owner of the yellow house smokes Dunhills"
# constraint.add_exactly_one(E, [(Col(id,"yellow") & Cig(id,"Dunhill")) for id in HOUSE])

# C8: "The man in the center house drinks milk"
# E.add_constraint(Dri(3,"milk"))

# C9: "The Norwegian lives in the first house"
# E.add_constraint(Nat(1,"Norwegian"))

# C10: "The Blend smoker has a neighbor who keeps cats"
# constraint.add_exactly_one(E, [(Cig(id,"Blend") & (Pet(id-1,"cats") | Pet(id+1,"cats"))) for id in HOUSE])

# C11: "The man who smokes Blue Masters drinks beer"
# constraint.add_exactly_one(E, [(Cig(id,"BlueMaster") & Dri(id,"beer")) for id in HOUSE])

# C12: "The man who keeps horses lives next to the Dunhill smoker"
# constraint.add_exactly_one(E, [Pet(id,"horses") & (Cig(id-1,"Dunhill") | Cig(id+1,"Dunhill"))for id in HOUSE])

# C13: "The German smokes Prince"

# C14: "The Norwegian lives next to the blue house"

# C15: "The Blend smoker has a neighbor who drinks water"

########################
# ADDITIONAL CONSTRAINTS
########################
# additional constraints; change as appropriate to capture how task values compare

##########################
# CONSTRAINTS FOR CHECKING 
##########################

#########
# SOLVING
#########

# Don't compile until you're finished adding all your constraints!
T = E.compile()
# E.introspect()
# After compilation (and only after), you can check some of the properties
# of your model:
print("\nsatisfiable? %s" % T.satisfiable())
# print("#solutions: %d" % count_solutions(T))
soln = T.solve()
# E.introspect(soln)
# print("Pretty print of theory:")
# E.pprint(T, soln)

# print solution
# print_theory(soln)
# print("solution: %s" % soln)

if soln: 
#     order = {}
#     for p in POS:
#         order[str(p)] = '_'

    for k in soln:
        if soln[k]:
            print(k)
#             order[str(k)[4]] = str(k)[1]

#     print("Dependencies: ", end="")
#     for k in soln:
#         if str(k)[2]=='>' and soln[k]:
#             print(k, end="   ")
 
#     print("\nPosition:     ", end="")
#     for p in POS:
#         print(p, end="    ")

#     print("\nTask:         ", end="")
#     for p in POS:
#         print(order[str(p)][0], end="    ")

#     print("\nlikelihood that specific atomic proposition is true:")
#     # for v,vn in zip([DepOn(t,p) for t in TASK  for p in POS], ["t1@p1","t@p2","t1@p3","t2@p1","t2@p2","t2@p3","t3@p1","t3@p2","t3@p3"]):
#     for v,vn in zip([At(t,p) for t in TASK  for p in POS], [str(At(t,p)) for t in TASK  for p in POS]):
#         # Ensure that you only send these functions NNF formulas
#         # Literals are compiled to NNF here
#         print(" %s: %.2f" % (vn, likelihood(T, v)))

# print("\nnegating theory...")
# T = T.negate()
# print("negation satisfiable: %s" % T.satisfiable())

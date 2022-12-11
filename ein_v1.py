
from bauhaus import Encoding, proposition, constraint, print_theory
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

HOUSE           = [1, 2, 3, 4, 5]
COLOUR          = ["blue", "green", "red", "white", "yellow"]
NATIONALITY     = ["Dane", "Englishman", "German", "Swede", "Norwegian"]
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
class House(Unique):
    def __init__(self,id,nat,col,dri,cig,pet):
        self.id = id
        self.nat = nat
        self.col = col
        self.dri = dri
        self.cig = cig
        self.pet = pet

    def __str__(self):
        return f"H{self.id}:{self.nat},{self.col},{self.dri},{self.cig},{self.pet}"

####################################
# CONSTRAINTS
####################################

# C1: "The Englishman lives in the red house"
constraint.add_exactly_one(E, [House(id,"Englishman","red",dri,cig,pet) \
        for id in HOUSE for dri in DRINK for cig in CIGARETTE for pet in PET])

# C2: "The Swede keeps dogs"
constraint.add_exactly_one(E, [House(id,"Swede",col,dri,cig,"dogs") \
        for id in HOUSE for col in COLOUR for dri in DRINK for cig in CIGARETTE])

# C3: "The Dane drinks tea"
constraint.add_exactly_one(E, [House(id,"Dane",col,"tea",cig,pet) \
        for id in HOUSE for col in COLOUR for cig in CIGARETTE for pet in PET])

# C4: "The green house is just to the left of the white one"
# constraint.add_exactly_one(E, [(House(id1,nat1,"green",dri1,cig1,pet1) & House(id1+1,nat2,"white",dri2,cig2,pet2)) \
#         for id1 in HOUSE for nat1 in NATIONALITY for dri1 in DRINK for cig1 in CIGARETTE for pet1 in PET \
#             for nat2 in NATIONALITY for dri2 in DRINK for cig2 in CIGARETTE for pet2 in PET])

# C5: "The owner of the green house drinks coffee"
constraint.add_exactly_one(E, [House(id,nat,"green","coffee",cig,pet) \
        for id in HOUSE for nat in NATIONALITY for cig in CIGARETTE for pet in PET])

# C6: "The Pall Mall smoker keeps birds"
constraint.add_exactly_one(E, [House(id,nat,col,dri,"PallMall","birds") \
        for id in HOUSE for nat in NATIONALITY for col in COLOUR for dri in DRINK for cig in CIGARETTE for pet in PET])

# C7: "The owner of the yellow house smokes Dunhills"
constraint.add_exactly_one(E, [House(id,nat,"yellow",dri,"Dunhills",pet) \
        for id in HOUSE for nat in NATIONALITY for dri in DRINK for pet in PET])

# C8: "The man in the center house drinks milk"
constraint.add_exactly_one(E, [House(3,nat,col,"milk",cig,pet) \
        for nat in NATIONALITY for col in COLOUR for cig in CIGARETTE for pet in PET])

# C9: "The Norwegian lives in the first house"
constraint.add_exactly_one(E, [House(1,"Norwegian",col,dri,cig,pet) \
        for col in COLOUR for dri in DRINK for cig in CIGARETTE for pet in PET])

# C10: "The Blend smoker has a neighbor who keeps cats"
# constraint.add_exactly_one(E, [House(id1,nat1,col1,"Blend",cig1,pet1) & (House(id1-1,nat2,col2,cig2,"cats") | House(id1+1,nat3,col3,cig3,"cats")) \
#         for id in HOUSE for dri in DRINK for cig in CIGARETTE for pet in PET])

# C11: "The man who smokes Blue Masters drinks beer"
constraint.add_exactly_one(E, [House(id,nat,col,"beer","BlueMasters",pet) \
        for id in HOUSE for nat in NATIONALITY for col in COLOUR for pet in PET])

# C12: "The man who keeps horses lives next to the Dunhill smoker"
# constraint.add_exactly_one(E, [House(id1,nat1,col1,dri1,cig1,"horses") & (House(id1-1,nat2,col2,"Dunhill",pet2) | House(id1+1,nat2,col2,"Dunhill",pet2)) 
#     for id in HOUSE for dri in DRINK for cig in CIGARETTE for pet in PET])

# C13: "The German smokes Prince"
constraint.add_exactly_one(E, [House(id,"German",col,"beer","Prince",pet) \
        for id in HOUSE for col in COLOUR for pet in PET])

# C14: "The Norwegian lives next to the blue house"
# constraint.add_exactly_one(E, [House(id1,"Norwegian",col1,dri1,cig1,pet1) & (House(id1-1,nat2,"blue",cig2,pet2) | House(id1+1,nat2,"blue",cig2,pet2)) \
#         for id in HOUSE for dri in DRINK for cig in CIGARETTE for pet in PET])

# C15: "The Blend smoker has a neighbor who drinks water"
# constraint.add_exactly_one(E, [House(id1,nat1,col1,dri1,"Blend",pet1) & (House(id1-1,nat2,col2,"water",cig2,pet2) | House(id1+1,nat2,col2,"water",cig2,pet2)) \
#         for id in HOUSE for dri in DRINK for cig in CIGARETTE for pet in PET])

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


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
        return f"H{self.id}:nat={self.nat}"

@proposition(E)
class Col(Unique):
    def __init__(self,id,col):
        self.id = id
        self.col = col

    def __str__(self):
        return f"H{self.id}:col={self.col}"

@proposition(E)
class Dri(Unique):
    def __init__(self,id,dri):
        self.id = id
        self.dri = dri

    def __str__(self):
        return f"H{self.id}:dri={self.dri}"

@proposition(E)
class Cig(Unique):
    def __init__(self,id,cig):
        self.id = id
        self.cig = cig

    def __str__(self):
        return f"H{self.id}:cig={self.cig}"

@proposition(E)
class Pet(Unique):
    def __init__(self,id,pet):
        self.id = id
        self.pet = pet

    def __str__(self):
        return f"H{self.id}:pet={self.pet}"


####################################
# CONSTRAINTS
####################################

# C1: "The Englishman lives in the red house"
E.add_constraint((Nat(1,"Englishman") & Col(1,"red")) | \
                 (Nat(2,"Englishman") & Col(2,"red")) | \
                 (Nat(3,"Englishman") & Col(3,"red")) | \
                 (Nat(4,"Englishman") & Col(4,"red")) | \
                 (Nat(5,"Englishman") & Col(5,"red")))
    

# C2: "The Swede keeps dogs"
E.add_constraint((Nat(1,"Swede") & Pet(1,"dogs")) | \
                 (Nat(2,"Swede") & Pet(2,"dogs")) | \
                 (Nat(3,"Swede") & Pet(3,"dogs")) | \
                 (Nat(4,"Swede") & Pet(4,"dogs")) | \
                 (Nat(5,"Swede") & Pet(5,"dogs")))

# C3: "The Dane drinks tea"
E.add_constraint((Nat(1,"Dane") & Dri(1,"tea")) | \
                 (Nat(2,"Dane") & Dri(2,"tea")) | \
                 (Nat(3,"Dane") & Dri(3,"tea")) | \
                 (Nat(4,"Dane") & Dri(4,"tea")) | \
                 (Nat(5,"Dane") & Dri(5,"tea")))

# C4: "The green house is just to the left of the white one"+
E.add_constraint((Col(1,"green") & Col(2,"white")) | \
                 (Col(2,"green") & Col(3,"white")) | \
                 (Col(3,"green") & Col(4,"white")) | \
                 (Col(4,"green") & Col(5,"white")))

# C5: "The owner of the green house drinks coffee"
E.add_constraint((Col(1,"green") & Dri(1,"coffee")) | \
                 (Col(2,"green") & Dri(2,"coffee")) | \
                 (Col(3,"green") & Dri(3,"coffee")) | \
                 (Col(4,"green") & Dri(4,"coffee")) | \
                 (Col(5,"green") & Dri(5,"coffee")))

# C6: "The Pall Mall smoker keeps birds"
E.add_constraint((Cig(1,"PallMall") & Pet(1,"birds")) | \
                 (Cig(2,"PallMall") & Pet(2,"birds")) | \
                 (Cig(3,"PallMall") & Pet(3,"birds")) | \
                 (Cig(4,"PallMall") & Pet(4,"birds")) | \
                 (Cig(5,"PallMall") & Pet(5,"birds")))

# C7: "The owner of the yellow house smokes Dunhills"
E.add_constraint((Col(1,"yellow") & Cig(1,"Dunhill")) | \
                 (Col(2,"yellow") & Cig(2,"Dunhill")) | \
                 (Col(3,"yellow") & Cig(3,"Dunhill")) | \
                 (Col(4,"yellow") & Cig(4,"Dunhill")) | \
                 (Col(5,"yellow") & Cig(5,"Dunhill")))

# C8: "The man in the center house drinks milk"
E.add_constraint(Dri(3,"milk"))

# C9: "The Norwegian lives in the first house"
E.add_constraint(Nat(1,"Norwegian"))

# C10: "The Blend smoker has a neighbor who keeps cats"
E.add_constraint((Cig(1,"Blend") & Pet(2,"cats")) | \
                 (Cig(2,"Blend") & Pet(1,"cats")) | \
                 (Cig(2,"Blend") & Pet(3,"cats")) | \
                 (Cig(3,"Blend") & Pet(2,"cats")) | \
                 (Cig(3,"Blend") & Pet(4,"cats")) | \
                 (Cig(4,"Blend") & Pet(5,"cats")) | \
                 (Cig(5,"Blend") & Pet(4,"cats")))

# C11: "The man who smokes Blue Masters drinks beer"
E.add_constraint((Cig(1,"BlueMaster") & Dri(1,"beer")) | \
                 (Cig(2,"BlueMaster") & Dri(2,"beer")) | \
                 (Cig(3,"BlueMaster") & Dri(3,"beer")) | \
                 (Cig(4,"BlueMaster") & Dri(4,"beer")) | \
                 (Cig(5,"BlueMaster") & Dri(5,"beer")))

# C12: "The man who keeps horses lives next to the Dunhill smoker"
E.add_constraint((Pet(1,"horses") & Cig(2,"Dunhill")) | \
                 (Pet(2,"horses") & Cig(1,"Dunhill")) | \
                 (Pet(2,"horses") & Cig(3,"Dunhill")) | \
                 (Pet(3,"horses") & Cig(4,"Dunhill")) | \
                 (Pet(3,"horses") & Cig(2,"Dunhill")) | \
                 (Pet(4,"horses") & Cig(5,"Dunhill")) | \
                 (Pet(4,"horses") & Cig(3,"Dunhill")) | \
                 (Pet(5,"horses") & Cig(4,"Dunhill")))

# C13: "The German smokes Prince"
E.add_constraint((Nat(1,"German") & Cig(1,"Prince")) | \
                 (Nat(2,"German") & Cig(2,"Prince")) | \
                 (Nat(3,"German") & Cig(3,"Prince")) | \
                 (Nat(4,"German") & Cig(4,"Prince")) | \
                 (Nat(5,"German") & Cig(5,"Prince")))

# C14: "The Norwegian lives next to the blue house"
E.add_constraint((Nat(1,"Norwegian") & Col(2,"blue")) | \
                 (Nat(2,"Norwegian") & Col(3,"blue")) | \
                 (Nat(2,"Norwegian") & Col(1,"blue")) | \
                 (Nat(3,"Norwegian") & Col(4,"blue")) | \
                 (Nat(3,"Norwegian") & Col(2,"blue")) | \
                 (Nat(4,"Norwegian") & Col(5,"blue")) | \
                 (Nat(4,"Norwegian") & Col(3,"blue")) | \
                 (Nat(5,"Norwegian") & Col(4,"blue")))

# C15: "The Blend smoker has a neighbor who drinks water"
E.add_constraint((Cig(1,"Blend") & Dri(2,"water")) | \
                 (Cig(2,"Blend") & Dri(3,"water")) | \
                 (Cig(2,"Blend") & Dri(1,"water")) | \
                 (Cig(3,"Blend") & Dri(4,"water")) | \
                 (Cig(3,"Blend") & Dri(2,"water")) | \
                 (Cig(4,"Blend") & Dri(5,"water")) | \
                 (Cig(4,"Blend") & Dri(3,"water")) | \
                 (Cig(5,"Blend") & Dri(4,"water")))

########################
# ADDITIONAL CONSTRAINTS
########################
# Given a nationality, exactly one house owner has it
for nat in NATIONALITY:
    constraint.add_exactly_one(E, [Nat(h,nat) for h in HOUSE])
# Given a colour, exactly one house has it
for col in COLOUR:
    constraint.add_exactly_one(E, [Col(h,col) for h in HOUSE])
# Given a drink, exactly one house owner prefers it
for dri in DRINK:
    constraint.add_exactly_one(E, [Dri(h,dri) for h in HOUSE])
# Given a cigarette, exactly one house owner prefers it
for cig in CIGARETTE:
    constraint.add_exactly_one(E, [Cig(h,cig) for h in HOUSE])
# Given a pet, exactly one house owner owns it
for pet in PET:
    constraint.add_exactly_one(E, [Pet(h,pet) for h in HOUSE])

# The owner of a house has exactly one nationality
for h in HOUSE:
    constraint.add_exactly_one(E, [Nat(h,nat) for nat in NATIONALITY])
# A house has exactly one colour
for h in HOUSE:    
    constraint.add_exactly_one(E, [Col(h,col) for col in COLOUR])
# The owner of a house has exactly one drink preference
for h in HOUSE:
    constraint.add_exactly_one(E, [Dri(h,dri) for dri in DRINK])
# The owner of a house has exactly one cigarette preference    
for h in HOUSE:
    constraint.add_exactly_one(E, [Cig(h,cig) for cig in CIGARETTE])
# The owner of a house has exactly one kind of pet    
for h in HOUSE:
    constraint.add_exactly_one(E, [Pet(h,pet) for pet in PET])

##########################
# CONSTRAINTS FOR CHECKING 
##########################
# fish owner cannot be in house 2 (but in 1, 3, 4, 5)
# E.add_constraint(Pet(1,"fish") | Pet(2,"fish") | Pet(3,"fish") | Pet(5,"fish"))

# fish owner can be in house 4
# E.add_constraint(Pet(4,"fish"))

# only the German can be fish owners
# E.add_constraint(Nat(4,"German"))
# E.add_constraint(Nat(4,"Norwegian"))

#########
# SOLVING
#########

# Don't compile until you're finished adding all your constraints!
T = E.compile()
# E.introspect()
# After compilation (and only after), you can check some of the properties
# of your model:
print("\nsatisfiable? %s" % T.satisfiable())
print("#solutions: %d" % count_solutions(T))
soln = T.solve()
# E.introspect(soln)
# print("Pretty print of theory:")
# E.pprint(T, soln)

# print solution
# print_theory(soln)
# print("solution: %s" % soln)

if soln:
    dict = {}
    for h in ['H1', 'H2', 'H3', 'H4', 'H5']:
        dict[h] = {}

    for k in soln:
        if soln[k]:
            if str(k)[3:6] == 'nat':
                dict[str(k)[0:2]]['nat'] = str(k)[7:]
            elif str(k)[3:6] == 'col':
                dict[str(k)[0:2]]['col'] = str(k)[7:]
            elif str(k)[3:6] == 'dri':
                dict[str(k)[0:2]]['dri'] = str(k)[7:]
            elif str(k)[3:6] == 'cig':
                dict[str(k)[0:2]]['cig'] = str(k)[7:]
            elif str(k)[3:6] == 'pet':
                dict[str(k)[0:2]]['pet'] = str(k)[7:]
            else:
                print("bug!")

    for h in ['H1', 'H2', 'H3', 'H4', 'H5']:
        print(f"{h}: ", end="")        
        for c in ['nat', 'col', 'dri', 'cig', 'pet']:
            if c in dict[h].keys():
                print(dict[h][c], end=" ")
            else:
                print("*", end=" ")
        print(" ")


from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class BasicProp:
    def __init__(self, data):
        self.data = data
    def __repr__(self):
        return f"B.{self.data}"


# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html
@constraint.at_least_one(E)
@proposition(E)
class AtLeast1Prop:
    def __init__(self, data):
        self.data = data
    def __repr__(self):
        return f"L1.{self.data}"

@constraint.exactly_one(E)
@proposition(E)
class Exactly1Prop:
    def __init__(self, data):
        self.data = data
    def __repr__(self):
        return f"E1.{self.data}"

# Call your variables whatever you want
a = BasicProp("a")
b = BasicProp("b")   
c = BasicProp("c")

i = AtLeast1Prop("i")
j = AtLeast1Prop("j")   
k = AtLeast1Prop("k")

# # At least one of these will be true
x = Exactly1Prop("x")
y = Exactly1Prop("y")
z = Exactly1Prop("z")

# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_encoding():
    # Add custom constraints by creating formulas with the variables you created. 
    
    E.add_constraint((a | b) & ~c)
    E.add_constraint(x)
    # Implication
    # E.add_constraint(y >> z)
    # Negate a formula    
    # E.add_constraint(~(x & y))
    # You can also add more customized "fancy" constraints. Use case: you don't want to enforce "exactly one"
    # for every instance of BasicPropositions, but you want to enforce it for a, b, and c.:

#    E.add_constraint((a | ~a))
    return E
 

if __name__ == "__main__":
    E = example_encoding()
    # Don't compile until you're finished adding all your constraints!
    T = E.compile()
    # E.introspect()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print(" #solutions: %d" % count_solutions(T))
    soln = T.solve()
    # E.introspect(soln)    
    if soln:
        print("   Pretty print of theory:")
        E.pprint(T, soln)
        print("   Solution: %s" % soln)
        for v in [a,b,c,i,j,k,x,y,z]:
            print(" %s: \t%s" % (v, soln[v])) 

        print("\nVariable likelihoods:")
        for v,vn in zip([a,b,c,i,j,k,x,y,z], 'abcijkxyz'):
            # Ensure that you only send these functions NNF formulas
            # Literals are compiled to NNF here
            print(" %s: %.2f" % (vn, likelihood(T, v)))
        
    print("\nValid: %s" % T.valid())
    # print("\nNegating theory:")
    # T = T.negate()
    # print("\nNegation satisfiable: %s" % T.satisfiable())
    # soln = T.solve()    
    # print("   Solution: %s" % soln)    
    print()

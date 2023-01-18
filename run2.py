
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class Prop:
    def __init__(self, data):
        self.data = data
    def __repr__(self):
        return f"P.{self.data}"


# Call your variables whatever you want
a = Prop("a")
b = Prop("b")   
c = Prop("c")

i = Prop("i")
j = Prop("j")   
k = Prop("k")

x = Prop("x")
y = Prop("y")
z = Prop("z")

# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_encoding():
    # Add custom constraints by creating formulas with the variables you created. 
    
    E.add_constraint((a | b) & ~c)
    constraint.add_exactly_one(E, [i,j,k])
    E.add_constraint(i)
    constraint.add_at_least_one(E, [x,y,z])
    E.add_constraint(x>>(y&z))
    # Implication
    # E.add_constraint(y >> z)
    # Negate a formula    
    # E.add_constraint(~(x & y))
    # E.add_constraint((a | ~a))
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
            print(" %s: %s" % (v, soln[v])) 

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

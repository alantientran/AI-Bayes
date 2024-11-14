# factorOperations.py
# -------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from bayesNet import Factor
import operator as op
import util
from functools import reduce

def joinFactorsByVariableWithCallTracking(callTrackingList=None):


    def joinFactorsByVariable(factors, joinVariable):
        """
        Input factors is a list of factors.
        Input joinVariable is the variable to join on.

        This function performs a check that the variable that is being joined on 
        appears as an unconditioned variable in only one of the input factors.

        Then, it calls your joinFactors on all of the factors in factors that 
        contain that variable.

        Returns a tuple of 
        (factors not joined, resulting factor from joinFactors)
        """

        if not (callTrackingList is None):
            callTrackingList.append(('join', joinVariable))

        currentFactorsToJoin =    [factor for factor in factors if joinVariable in factor.variablesSet()]
        currentFactorsNotToJoin = [factor for factor in factors if joinVariable not in factor.variablesSet()]

        # typecheck portion
        numVariableOnLeft = len([factor for factor in currentFactorsToJoin if joinVariable in factor.unconditionedVariables()])
        if numVariableOnLeft > 1:
            print("Factor failed joinFactorsByVariable typecheck: ", factor)
            raise ValueError("The joinBy variable can only appear in one factor as an \nunconditioned variable. \n" +  
                               "joinVariable: " + str(joinVariable) + "\n" +
                               ", ".join(map(str, [factor.unconditionedVariables() for factor in currentFactorsToJoin])))
        
        joinedFactor = joinFactors(currentFactorsToJoin)
        return currentFactorsNotToJoin, joinedFactor

    return joinFactorsByVariable

joinFactorsByVariable = joinFactorsByVariableWithCallTracking()


def joinFactors(factors):
    """
    Question 3: Your join implementation 

    Input factors is a list of factors.  
    
    You should calculate the set of unconditioned variables and conditioned 
    variables for the join of those factors.

    Return a new factor that has those variables and whose probability entries 
    are product of the corresponding rows of the input factors.

    You may assume that the variableDomainsDict for all the input 
    factors are the same, since they come from the same BayesNet.

    joinFactors will only allow unconditionedVariables to appear in 
    one input factor (so their join is well defined).

    Hint: Factor methods that take an assignmentDict as input 
    (such as getProbability and setProbability) can handle 
    assignmentDicts that assign more variables than are in that factor.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """

    # typecheck portion
    setsOfUnconditioned = [set(factor.unconditionedVariables()) for factor in factors]
    if len(factors) > 1:
        intersect = reduce(lambda x, y: x & y, setsOfUnconditioned)
        if len(intersect) > 0:
            print("Factor failed joinFactors typecheck: ", factor)
            raise ValueError("unconditionedVariables can only appear in one factor. \n"
                    + "unconditionedVariables: " + str(intersect) + 
                    "\nappear in more than one input factor.\n" + 
                    "Input factors: \n" +
                    "\n".join(map(str, factors)))


    "*** YOUR CODE HERE ***"
    uncond = set()
    cond = set()

    # Build sets that only contain the new vars.
    # We combine all of the unconditioned vars, but leave 
    # only the combinitions of conditioned vars that aren't included 
    # in the unconditioned vars
    for factor in factors: 
        uncond.update(factor.unconditionedVariables())
        cond.update(factor.conditionedVariables())
    cond = cond - uncond

    f = Factor(uncond, cond, factors[0].variableDomainsDict())
    print("uncond: ", uncond)
    print("cond: ", cond)
    
    # We could look through every combination of assignments in all of the
    # given factors, but that would be difficult to verify we are combining
    # the right info. Instead, we'll just loop over the new assignments
    # and find the appearances of that in the existing factors.
    for assignment in f.getAllPossibleAssignmentDicts() :
        prob = 1
        for factor in factors :
            prob *= factor.getProbability(assignment)
        f.setProbability(assignment, prob)
    return f

def eliminateWithCallTracking(callTrackingList=None):

    def eliminate(factor, eliminationVariable):
        """
        Question 4: Your eliminate implementation 

        Input factor is a single factor.
        Input eliminationVariable is the variable to eliminate from factor.
        eliminationVariable must be an unconditioned variable in factor.
        
        You should calculate the set of unconditioned variables and conditioned 
        variables for the factor obtained by eliminating the variable
        eliminationVariable.

        Return a new factor where all of the rows mentioning
        eliminationVariable are summed with rows that match
        assignments on the other variables.

        Useful functions:
        Factor.getAllPossibleAssignmentDicts
        Factor.getProbability
        Factor.setProbability
        Factor.unconditionedVariables
        Factor.conditionedVariables
        Factor.variableDomainsDict

        https://www.cs.cmu.edu/~15281-f23/coursenotes/bayesnets/index.html 
        def variable_elimination(query, e, bn):  
            q = re-express query in terms of bn.CPTs  
            factors = all probability tables in q  
            for v in order(bn.variables):  
                new_factor = make_factor(v, factors)  
                factors.add(new_factor)  
            return normalize(product of all factors)  
      
        def make_factor(v, factors):  
            relevant_factors = [remove all f from factors if f depends on v]  
            new_factor = product of all relevant_factors  
            return sum_out(relevant_factors, v)  
        """
        
        # autograder tracking -- don't remove
        if not (callTrackingList is None):
            callTrackingList.append(('eliminate', eliminationVariable))

        # typecheck portion
        if eliminationVariable not in factor.unconditionedVariables():
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Elimination variable is not an unconditioned variable " \
                            + "in this factor\n" + 
                            "eliminationVariable: " + str(eliminationVariable) + \
                            "\nunconditionedVariables:" + str(factor.unconditionedVariables()))
        
        if len(factor.unconditionedVariables()) == 1:
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Factor has only one unconditioned variable, so you " \
                    + "can't eliminate \nthat variable.\n" + \
                    "eliminationVariable:" + str(eliminationVariable) + "\n" +\
                    "unconditionedVariables: " + str(factor.unconditionedVariables()))

        "*** YOUR CODE HERE ***"
        uncond = factor.unconditionedVariables().copy()
        for var in factor.unconditionedVariables() :
            if var == eliminationVariable :
                uncond.remove(var)
        f = Factor(uncond, factor.conditionedVariables(), factor.variableDomainsDict())
        print(f)
        
        for assign in f.getAllPossibleAssignmentDicts() : 
            prob = 0
            print(assign)
            for factor_assign in factor.getAllPossibleAssignmentDicts() :
                # We want to find all matches of the smaller combination inside
                # the larger CPT (i.e. Weather = Rain and Ground = Wet inside of a larger
                # distribution that also contains Temperature = Cold; add probabilites that 
                # match the two conditions in the marginal).

                # Used an LLM to help with this line.
                compatible = all(
                    assign[var] == factor_assign[var]
                    for var in assign if var in factor_assign
                )

                if compatible:
                    prob += factor.getProbability(factor_assign)  # Accumulate probability

            f.setProbability(assign, prob)
                    
# 
        return f
    return eliminate

eliminate = eliminateWithCallTracking()


def normalize(factor):
    """
    Question 5: Your normalize implementation 

    Input factor is a single factor.

    The set of conditioned variables for the normalized factor consists 
    of the input factor's conditioned variables as well as any of the 
    input factor's unconditioned variables with exactly one entry in their 
    domain.  Since there is only one entry in that variable's domain, we 
    can either assume it was assigned as evidence to have only one variable 
    in its domain, or it only had one entry in its domain to begin with.
    This blurs the distinction between evidence assignments and variables 
    with single value domains, but that is alright since we have to assign 
    variables that only have one value in their domain to that single value.

    Return a new factor where the sum of the all the probabilities in the table is 1.
    This should be a new factor, not a modification of this factor in place.

    If the sum of probabilities in the input factor is 0,
    you should return None.

    This is intended to be used at the end of a probabilistic inference query.
    Because of this, all variables that have more than one element in their 
    domain are assumed to be unconditioned.
    There are more general implementations of normalize, but we will only 
    implement this version.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """

    # typecheck portion
    variableDomainsDict = factor.variableDomainsDict()
    for conditionedVariable in factor.conditionedVariables():
        if len(variableDomainsDict[conditionedVariable]) > 1:
            print("Factor failed normalize typecheck: ", factor)
            raise ValueError("The factor to be normalized must have only one " + \
                            "assignment of the \n" + "conditional variables, " + \
                            "so that total probability will sum to 1\n" + 
                            str(factor))

    "*** YOUR CODE HERE ***"
    variableDomainsDict = factor.variableDomainsDict()
    totalProb = 0  
    for assign in factor.getAllPossibleAssignmentDicts() :
        totalProb += factor.getProbability(assign)
    conditionedVariables = set(factor.conditionedVariables())

    unconditionedVariables = set(factor.unconditionedVariables())
    for var in factor.unconditionedVariables():
        if len(variableDomainsDict[var]) == 1:
            conditionedVariables.add(var)
            unconditionedVariables.remove(var)
    
    f = Factor(unconditionedVariables, conditionedVariables, variableDomainsDict)



    for assign in f.getAllPossibleAssignmentDicts() :
        if (totalProb > 0) :
            f.setProbability(assign, factor.getProbability(assign) / totalProb)
    
    return f

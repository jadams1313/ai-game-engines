import itertools

def create_burglary_cpts():

    # P(B) 
    cpt_b = {
        (True,): 0.001,
        (False,): 0.999
    }
    
    # P(E) 
    cpt_e = {
        (True,): 0.002,
        (False,): 0.998
    }
    
    # P(A|B,E) 
    # format: (B, E, A) - probability
    cpt_a = {
        (True, True, True): 0.95,
        (True, True, False): 0.05,
        (True, False, True): 0.94,
        (True, False, False): 0.06,
        (False, True, True): 0.29,
        (False, True, False): 0.71,
        (False, False, True): 0.001,
        (False, False, False): 0.999
    }
    
    # P(J|A) 
    # format: (A, J) - probability
    cpt_j = {
        (True, True): 0.90,
        (True, False): 0.10,
        (False, True): 0.05,
        (False, False): 0.95
    }
    
    # P(M|A) 
    # format: (A, M) - probability
    cpt_m = {
        (True, True): 0.70,
        (True, False): 0.30,
        (False, True): 0.01,
        (False, False): 0.99
    }
    
    return {
        'B': (['B'], cpt_b),
        'E': (['E'], cpt_e),
        'A': (['B', 'E', 'A'], cpt_a),
        'J': (['A', 'J'], cpt_j),
        'M': (['A', 'M'], cpt_m)
    }

def restrict(cpt_vars, cpt_table, var_name, var_value):
    if var_name not in cpt_vars:
        return cpt_vars, cpt_table
    
    var_idx = cpt_vars.index(var_name)
    new_vars = [v for v in cpt_vars if v != var_name]
    new_table = {}
    
    for assignment, prob in cpt_table.items():
        if assignment[var_idx] == var_value:
            reduced = tuple(assignment[i] for i in range(len(assignment)) if i != var_idx)
            new_table[reduced] = prob
    
    return new_vars, new_table

def multiply_cpts(cpt1_vars, cpt1_table, cpt2_vars, cpt2_table):

    # union of variables
    new_vars = list(dict.fromkeys(cpt1_vars + cpt2_vars))
    new_table = {}
    
    #all possible assignments
    for assignment in itertools.product([False, True], repeat=len(new_vars)):
        idx1 = tuple(assignment[new_vars.index(v)] for v in cpt1_vars)
        idx2 = tuple(assignment[new_vars.index(v)] for v in cpt2_vars)
        # probs
        prob = cpt1_table.get(idx1, 0) * cpt2_table.get(idx2, 0)
        new_table[assignment] = prob
    
    return new_vars, new_table
def sum_var(cpt_vars, cpt_table, elim_var): 
    if elim_var not in cpt_vars:
        return cpt_vars, cpt_table
    var_idx = cpt_vars.index(elim_var)
    new_vars = [v for v in cpt_vars if v != elim_var]
    new_table = {}
    
    for assignment, prob in cpt_table.items():
        reduced = tuple(assignment[i] for i in range(len(assignment)) if i != var_idx)
        new_table[reduced] = new_table.get(reduced, 0) + prob
    
    return new_vars, new_table

def normalize(cpt_vars, cpt_table):
    total = sum(cpt_table.values())
    if total == 0:
        return cpt_vars, cpt_table
    
    normalized = {k: v / total for k, v in cpt_table.items()}
    return cpt_vars, normalized

def variable_elimination(table, query_var, evidence, elim_order):

    #so i don't modify the tables
    current_cpts = [(vars_list, table) for vars_list, table in table.values()]
    
    #restrict cpt
    restricted_cpts = []
    for cpt_vars, cpt_table in current_cpts:
        restricted_vars, restricted_table = cpt_vars, cpt_table
        for var, value in evidence.items():
            restricted_vars, restricted_table = restrict(
                restricted_vars, restricted_table, var, value
            )
        restricted_cpts.append((restricted_vars, restricted_table))
    
    # eliminate variables in order
    for var in elim_order:
        # find CPTs containing this variable
        relevant = [(v, t) for v, t in restricted_cpts if var in v]
        irrelevant = [(v, t) for v, t in restricted_cpts if var not in v]
        
        if not relevant:
            continue
        product_vars, product_table = relevant[0]
        for vars_list, table in relevant[1:]:
            product_vars, product_table = multiply_cpts(
                product_vars, product_table, vars_list, table
            )
        marginalized_vars, marginalized_table = sum_var(
            product_vars, product_table, var
        )
        restricted_cpts = irrelevant + [(marginalized_vars, marginalized_table)]
    
    # multiply remaining CPTs
    result_vars, result_table = restricted_cpts[0]
    for vars_list, table in restricted_cpts[1:]:
        result_vars, result_table = multiply_cpts(
            result_vars, result_table, vars_list, table
        )
    
    # remember to normalize 
    return normalize(result_vars, result_table)

def main():

    cpts = create_burglary_cpts()

    query_var = 'B'
    evidence = {'J': True} 
    elimination_order = ['E', 'M', 'A']

    result_vars, result_table = variable_elimination(
        cpts, query_var, evidence, elimination_order
    )
    
    for assignment in sorted(result_table.keys()):
        burglary_value = assignment[0]
        burglary_label = "+b (True)" if burglary_value else "-b (False)"
        prob = result_table[assignment]
        print(f"{burglary_label} {prob}")
    
    total_prob = sum(result_table.values())
    print(total_prob)


if __name__ == "__main__":
    main()



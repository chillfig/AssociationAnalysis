from __future__ import print_function
import collections
import sys
from typing import Counter



def apriori(dataset, min_support=0.5, verbose=False):
    """Implements the Apriori algorithm.

    The Apriori algorithm will iteratively generate new candidate
    k-itemsets using the frequent (k-1)-itemsets found in the previous
    iteration.

    Parameters
    ----------
    dataset : list
        The dataset (a list of transactions) from which to generate
        candidate itemsets.

    min_support : float
        The minimum support threshold. Defaults to 0.5.

    Returns
    -------
    F : list
        The list of frequent itemsets.

    support_data : dict
        The support data for all candidate itemsets.

    References
    ----------
    .. [1] R. Agrawal, R. Srikant, "Fast Algorithms for Mining Association
           Rules", 1994.

    """
    C1 = create_candidates(dataset)
    D = list(map(set, dataset))
    F1, support_data = get_freq(D, C1, min_support, verbose=False) # get frequent 1-itemsets
    F = [F1] # list of frequent itemsets; initialized to frequent 1-itemsets
    k = 2 # the itemset cardinality
    while (len(F[k - 2]) > 0):
        Ck = apriori_gen(F[k-2], k) # generate candidate itemsets
        Fk, supK  = get_freq(D, Ck, min_support) # get frequent itemsets
        support_data.update(supK)# update the support counts to reflect pruning
        F.append(Fk)  # add the frequent k-itemsets to the list of frequent itemsets
        k += 1

    if verbose:
        # Print a list of all the frequent itemsets.
        for kset in F:
            for item in kset:
                print(""                     + "{"                     + "".join(str(i) + ", " for i in iter(item)).rstrip(', ')                     + "}"                     + ":  sup = " + str(round(support_data[item], 3)))

    return F, support_data

def create_candidates(dataset, verbose=False):
    """Creates a list of candidate 1-itemsets from a list of transactions.

    Parameters
    ----------
    dataset : list
        The dataset (a list of transactions) from which to generate candidate
        itemsets.

    Returns
    -------
    The list of candidate itemsets (c1) passed as a frozenset (a set that is
    immutable and hashable).
    """
    c1 = [] # list of all items in the database of transactions
    for transaction in dataset:
        for item in transaction:
            if not [item] in c1:
                c1.append([item])
    c1.sort()
    
    if verbose:
        # Print a list of all the candidate items.
        print(""             + "{"             + "".join(str(i[0]) + ", " for i in iter(c1)).rstrip(', ')             + "}")

    # Map c1 to a frozenset because it will be the key of a dictionary.
    return list(map(frozenset, c1))

def get_freq(dataset, candidates, min_support, verbose=False):
    """

    This function separates the candidates itemsets into frequent itemset and infrequent itemsets based on the min_support,
	and returns all candidate itemsets that meet a minimum support threshold.

    Parameters
    ----------
    dataset : list
        The dataset (a list of transactions) from which to generate candidate
        itemsets.

    candidates : frozenset
        The list of candidate itemsets.

    min_support : float
        The minimum support threshold.

    Returns
    -------
    freq_list : list
        The list of frequent itemsets.

    support_data : dict
        The support data for all candidate itemsets.
    """

   
    
    
    lcv = 0   #loop control variable used for mapping list cand_set to the frozen set of candidates 
    freq_list = []
    support_data = dict()
    
    if candidates == []:    #return if you have no candidates
        return freq_list, support_data

    cand_set = ([list(x) for x in candidates]) #data more easily appendable to dict
    # count support
    for item in cand_set:
        if len(item) == 1:
            support_data[item[0]] = 0
        else:
            support_data[tuple(item)] = 0
        for transaction in dataset:
            if (candidates[lcv].issubset(transaction)):
                #count.update(Counter(item))  
                if len(item) == 1:
                    support_data[item[0]] += 1
                else:
                    support_data[tuple(item)] += 1
        lcv += 1
    
    #support_data = dict(count)
    # generate list of frequent items
    for key, value in support_data.items():
        if((float(value/len(dataset))) >= min_support):
            if len(item) == 1:
                freq_list.append(set([key]))
            else:
                freq_list.append(set(key))
        freq_list.sort()
    # if len(item) == 1:
        
        # freq_list = list(map(set,freq_list)) # map the itemsets to sets within the list
    
    return freq_list, support_data
    # TODO

def apriori_gen(freq_sets, k):
    """Generates candidate itemsets (via the F_k-1 x F_k-1 method).

    This part generates new candidate k-itemsets based on the frequent
    (k-1)-itemsets found in the previous iteration.

    The apriori_gen function performs two operations:
    (1) Generate length k candidate itemsets from length k-1 frequent itemsets
    (2) Prune candidate itemsets containing subsets of length k-1 that are infrequent

    Parameters
    ----------
    freq_sets : list
        The list of frequent (k-1)-itemsets.

    k : integer
        The cardinality of the current itemsets being evaluated.

    Returns
    -------
    candidate_list : list
        The list of candidate itemsets.
    """
    # operation 1
    freq_lists = ([sorted(list(x)) for x in freq_sets])
    candidate_list = []

    if k == 2:    
        for a in freq_lists:
            for b in freq_lists:
                #union = sorted(a + [d for d in b if not d in a]) # for list iteration
                #union = a | b  # for set iteration
                union = sorted(a + [d for d in b if not d in a])
                if len(union) == k and a != b and not union in candidate_list:
                    candidate_list.append(union)
    else:
        for a in freq_lists:
            for b in freq_lists:
                union = sorted(a + [d for d in b if not d in a])
                if list(a)[0:k-2] == list(b)[0:k-2] and len(union) == k and a != b and not union in candidate_list:
                    candidate_list.append(union)

    # operation 2
    if k > 2:
        removedCand = []
        for itemset in candidate_list:  
            subsets = []
            x = len(itemset)
            for i in range(1 << x):
                subsets.append(sorted([itemset[j] for j in range(x) if (i & (1 << j))]))
            for subset in subsets:
                if len(subset) == k-1 and not subset in freq_lists:
                    removedCand.append(itemset)
                    continue
        for removal in removedCand:
            candidate_list.remove(removal)   
    
    candidate_list.sort()
    candidate_list = ([set(y) for y in candidate_list]) # for list iteration    
    
    return candidate_list
    # TODO


def loadDataSet(fileName, delim=','):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    return stringArr



def run_apriori(data_path, min_support, verbose=False):
    dataset = loadDataSet(data_path)
    F, support = apriori(dataset, min_support=min_support, verbose=verbose)
    return F, support



def bool_transfer(input):
    ''' Transfer the input to boolean type'''
    input = str(input)
    if input.lower() in ['t', '1', 'true' ]:
        return True
    elif input.lower() in ['f', '0', 'false']:
        return False
    else:
        raise ValueError('Input must be one of {T, t, 1, True, true, F, F, 0, False, false}')




if __name__ == '__main__':
    if len(sys.argv)==3:
        F, support = run_apriori(sys.argv[1], float(sys.argv[2]))
    elif len(sys.argv)==4:
        F, support = run_apriori(sys.argv[1], float(sys.argv[2]), bool_transfer(sys.argv[3]))
    else:
        F, support = run_apriori('market_data_transaction.txt', 0.5) #justin added for testing DELETE ME
        #raise ValueError('Usage: python apriori_templete.py <data_path> <min_support> <is_verbose>')
    print(F)
    print(support)

    '''
    Example: 
    
    python apriori_templete.py market_data_transaction.txt 0.5 
    
    python apriori_templete.py market_data_transaction.txt 0.5 True
    
    '''






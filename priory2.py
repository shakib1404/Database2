import numpy as np
from itertools import chain, combinations

def load_transactions(path_to_data, order=None):
    Transactions = []
    with open(path_to_data, 'r') as fid:
        for line in fid:
            transaction = list(line.strip().split(','))
            unique_items = list(np.unique(transaction))
            if order:
                unique_items.sort(key=lambda x: order.index(x))
            Transactions.append(unique_items)
    return Transactions

def count_occurrences(itemset, Transactions):
    return sum(1 for transaction in Transactions if set(itemset).issubset(set(transaction)))

def join_two_itemsets(it1, it2, order):
    it1_sorted = sorted(it1, key=lambda x: order.index(x))
    it2_sorted = sorted(it2, key=lambda x: order.index(x))
    
    for i in range(len(it1_sorted) - 1):
        if it1_sorted[i] != it2_sorted[i]:
            return []
    if order.index(it1_sorted[-1]) < order.index(it2_sorted[-1]):
        return it1_sorted + [it2_sorted[-1]]
    
    return []

def join_set_itemsets(set_of_itemsets, order):
    C = []
    for i in range(len(set_of_itemsets)):
        for j in range(i + 1, len(set_of_itemsets)):
            new_itemset = join_two_itemsets(set_of_itemsets[i], set_of_itemsets[j], order)
            if new_itemset:
                C.append(new_itemset)
    return C

def get_frequent_itemsets(itemsets, Transactions, min_support, prev_discarded):
    L = []
    supp_count = []
    new_discarded = []
    
    k = len(prev_discarded.keys())
    
    for s in range(len(itemsets)):
        discarded = any(set(it).issubset(set(itemsets[s])) for it in prev_discarded.get(k, []))

        if not discarded:
            count = count_occurrences(itemsets[s], Transactions)
            if count / len(Transactions) >= min_support:
                L.append(itemsets[s])
                supp_count.append(count)
            else:
                new_discarded.append(itemsets[s])

    return L, supp_count, new_discarded

def powerset(s):
    return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1)))

def write_rules(X, X_S, S, conf, supp, lift, num_trans):
    out_rules = ""
    out_rules += "Freq. Itemset: {} \n".format(X)
    out_rules += "    Rule: {} -> {} \n".format(list(S), list(X_S))
    out_rules += "    Conf: {} \n".format(conf)
    out_rules += "    Supp: {} \n".format(supp / num_trans)
    out_rules += "    Lift: {} \n".format(lift)
    return out_rules

def get_properties(Transactions, L, min_conf, min_support, num_trans):
    assoc_rules_str = ""
    
    for i in range(1, len(L)):
        for j in range(len(L[i])):
            s = powerset(L[i][j])
            s.pop()  # Remove the empty set
            for z in s:
                S = set(z)
                X = set(L[i][j])
                X_S = set(X - S)
                sup_x = count_occurrences(X, Transactions)
                sup_x_s = count_occurrences(X_S, Transactions)

                # Prevent division by zero
                conf = sup_x / count_occurrences(S, Transactions) if count_occurrences(S, Transactions) > 0 else 0
                lift = conf / (sup_x_s / num_trans) if sup_x_s > 0 else 0
                
                if conf >= min_conf and sup_x >= min_support:
                    assoc_rules_str += write_rules(X, X_S, S, conf, sup_x, lift, num_trans)

    return assoc_rules_str

def print_table(itemsets, supp_counts, level_name):
    print(f"{level_name} | {'Itemset':<20} | {'Frequency':<10}")
    print('-' * 50)
    for itemset, count in zip(itemsets, supp_counts):
        print(f"  {str(itemset):<20} | {count:<10}")
    print("\n")

def apriori(path_to_data, min_support, min_conf, order=None):
    Transactions = load_transactions(path_to_data, order)
    print("Transactions loaded:")
    for t in Transactions:
        print(t)

    # Initialize
    C = {}
    L = {}
    discarded_itemsets = {}
    itemset_size = 1

    # Generate initial candidate itemsets (C1)
    if order is None:
        order = sorted({item for transaction in Transactions for item in transaction})
    
    C[itemset_size] = [[item] for item in order]
    print(f"\nInitial Candidates (C1):")
    print_table(C[itemset_size], [count_occurrences(it, Transactions) for it in C[itemset_size]], f"C{itemset_size}")

    # Generate first set of frequent itemsets (L1)
    L[itemset_size], supp_count_L, discarded_itemsets[itemset_size] = get_frequent_itemsets(C[itemset_size], Transactions, min_support, discarded_itemsets)
    print(f"\nFrequent Itemsets (L1):")
    print_table(L[itemset_size], supp_count_L, f"L{itemset_size}")

    # Iteratively generate candidate itemsets and frequent itemsets
    k = itemset_size + 1
    while True:
        C[k] = join_set_itemsets(L[k - 1], order)
        if not C[k]:
            break

        print(f"\nCandidates (C{k}):")
        print_table(C[k], [count_occurrences(it, Transactions) for it in C[k]], f"C{k}")
        
        L[k], supp_count_L, discarded_itemsets[k] = get_frequent_itemsets(C[k], Transactions, min_support, discarded_itemsets)
        
        if not L[k]:
            break
        print(f"\nFrequent Itemsets (L{k}):")
        print_table(L[k], supp_count_L, f"L{k}")

        k += 1

    # Generate association rules
    num_trans = len(Transactions)
    assoc_rules = get_properties(Transactions, L, min_conf, min_support, num_trans)
    print("\nAssociation Rules:")
    print(assoc_rules)

if __name__ == "__main__":
    path_to_data = "data1.txt"  # Update with your data file path
    min_support = 2 / 9  # Adjust the minimum support as needed
    min_conf = 0.5  # Set your minimum confidence threshold here
    apriori(path_to_data, min_support, min_conf)

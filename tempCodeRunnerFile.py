def process_recovery_log(log):
    transactions = {}
    redo = set()
    undo = set()
    

    entries = log.splitlines()
    
    for entry in entries:
        if "<START T" in entry:
            txn_id = entry.split()[1] 
         
            txn_id = txn_id.strip('>')
            #txn_id = txn_id.strip('<')

            transactions[txn_id] = {'active': True, 'committed': False}
        
        elif "<COMMIT" in entry:
            txn_id = entry.split()[1] 
            txn_id = txn_id.strip('>')
            if txn_id in transactions:
                transactions[txn_id]['committed'] = True
                transactions[txn_id]['active'] = False
                redo.add(txn_id)
        
        elif "<CKPT" in entry:
            active_txns = entry.split('(')[1].split(')')[0].split(',')
            for txn_id in active_txns:
                txn_id = txn_id.strip()
                if txn_id in transactions:
                    transactions[txn_id]['active'] = False
                    if not transactions[txn_id]['committed']:
                        undo.add(txn_id)

        elif "<END CKPT>" in entry:
            continue

    
    for txn_id, status in transactions.items():
        if status['active'] and not status['committed']:
            undo.add(txn_id)

    return list(redo), list(undo)



def read_log_from_file(file_path):
    with open(file_path, 'r') as file:
        log = file.read()
    return log



file_path = 'recover_log.txt'  
log = read_log_from_file(file_path)

redo_transactions, undo_transactions = process_recovery_log(log)

print("Redo Transactions:", redo_transactions)
print("Undo Transactions:", undo_transactions)

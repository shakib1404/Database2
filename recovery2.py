def process_recovery_log(log):
    transactions = {}
    redo = set()
    undo = set()
    checkpoint_active_txns = set()
    checkpoint_started = False
    

    entries = log.splitlines()
    
    for entry in entries:
        if "<START T" in entry:
            txn_id = entry.split(" ")[1] 
            txn_id = txn_id[:-1]
            #txn_id = txn_id.strip('<')

            transactions[txn_id] = {'active': True, 'committed': False}
        
        elif "<COMMIT" in entry:
            txn_id = entry.split()[1] 
            txn_id = txn_id.strip('>')
            if txn_id in transactions:
                transactions[txn_id]['active'] = False
                transactions[txn_id]['committed'] = True
                if checkpoint_started or txn_id in checkpoint_active_txns:
                 redo.add(txn_id)
                # if txn_id in undo:
                 #   undo.remove(txn_id)
        
        elif "<CKPT" in entry:
            active_txns  = entry.split('(')[1].split(')')[0].split(',')
            checkpoint_active_txns = { txn_id in active_txns}
            checkpoint_started = True 

           # for txn_id in active_txns:
               # txn_id = txn_id.strip()
               # if txn_id in transactions:
                 #   transactions[txn_id]['active'] = False
                  #  if not transactions[txn_id]['committed']:
                        
                   #     undo.add(txn_id)

        elif "<END CKPT>" in entry:
            checkpoint_started = False
            continue

    
    for txn_id, status in transactions.items():
        if status['active'] and not status['committed']:
            undo.add(txn_id)

    return list(redo), list(undo)



def read_log_from_file(file_path):
    with open(file_path, 'r') as file:
        log = file.read()
    return log



file_path = ' log.txt'  
log = read_log_from_file(file_path)

redo_transactions, undo_transactions = process_recovery_log(log)

print("Undo Transactions:", undo_transactions)
print("Redo Transactions:", redo_transactions)


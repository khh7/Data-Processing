class InMemoryDB:
    def __init__(self):
        self.main_db = {}
        self.transaction_db = None
        self.in_transaction = False

    def get(self, key):
        # return the value associated with the key or null if the key doesn’t exist
        return self.main_db.get(key, None)

    def put(self, key, value):
        # if called when a transaction is not in progress throw an exception
        if not self.in_transaction:
            raise Exception("No active transaction.")
        # Store changes in transaction_db
        self.transaction_db[key] = value

    def begin_transaction(self):
        # starts a new transaction; at a time only a single transaction may exist
        # should not be “visible” to get(), until the transaction is committed
        if self.in_transaction:
            raise Exception("Transaction is already in progress.")
        self.transaction_db = {}
        self.in_transaction = True

    def commit(self):
        # applies changes made within the transaction to the main state
        # allowing any future gets() to “see” the changes made within the transaction
        if not self.in_transaction:
            raise Exception("No active transaction to commit.")
        self.main_db.update(self.transaction_db)
        self.transaction_db = None
        self.in_transaction = False

    def rollback(self):
        # abort all the changes made within the transaction and everything should go back to the way it was before
        if not self.in_transaction:
            raise Exception("No active transaction to rollback.")
        self.transaction_db = None
        self.in_transaction = False

## *** TODO: Uncomment below to test with example given in instructions ***
# if __name__ == "__main__":
#     inmemoryDB = InMemoryDB()

#     try:
#         # should return null, because A doesn’t exist in the DB yet
#         print(inmemoryDB.get("A"))
#     except Exception as e:
#         print(e)

#     try:
#         # should throw an error because a transaction is not in progress
#         inmemoryDB.put("A", 5)
#     except Exception as e:
#         print(e)

#     # starts a new transaction
#     inmemoryDB.begin_transaction()

#     # sets value of A to 5, but its not committed yet
#     inmemoryDB.put("A", 5)

#     try:
#         # should return null, because updates to A are not committed yet
#         print(inmemoryDB.get("A"))
#     except Exception as e:
#         print(e)

#     # update A’s value to 6 within the transaction
#     inmemoryDB.put("A", 6)

#     # commits the open transaction
#     inmemoryDB.commit()

#     # should return 6, that was the last value of A to be committed
#     print(inmemoryDB.get("A"))

#     try:
#         # throws an error, because there is no open transaction
#         inmemoryDB.commit()
#     except Exception as e:
#         print(e)

#     try:
#         # throws an error because there is no ongoing transaction
#         inmemoryDB.rollback()
#     except Exception as e:
#         print(e)

#     # should return null because B does not exist in the database
#     print(inmemoryDB.get("B"))

#     # starts a new transaction
#     inmemoryDB.begin_transaction()

#     # Set key B’s value to 10 within the transaction
#     inmemoryDB.put("B", 10)

#     # Rollback the transaction - revert any changes made to B
#     inmemoryDB.rollback()

#     # Should return None because changes to B were rolled back
#     print(inmemoryDB.get("B"))
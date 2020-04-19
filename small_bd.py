class Db:
    def __init__(self):
        self.main_db = {}
        self.transactions = []
        self.is_work = True

    def set(self, key, value):
        if self.transactions:
            self.transactions[-1][key] = value
        else:
            self.main_db[key] = value

    def get(self, key):
        for db in reversed(self.transactions):
            if key in db:
                print(db[key])
                return None
        print(self.main_db.get(key, "NULL"))

    def unset(self, key):
        if self.transactions:
            if key in self.transactions[-1]:
                del self.transactions[-1][key]
            else:
                self.transactions[-1][key] = "NULL"
        else:
            if key in self.main_db:
                del self.main_db[key]

    def count(self, value):
        print(list(self.main_db.values()).count(value))

    def begin(self):
        self.transactions.append({})

    def rollback(self):
        if self.transactions:
            del self.transactions[-1]

    def commit(self):
        for transaction in self.transactions:
            for key, value in transaction.items():
                if value == "NULL" and self.main_db[key]:
                    del self.main_db[key]
                else:
                    self.main_db[key] = value
        self.transactions = []

    def end(self):
        self.is_work = False
        

def run():
    database = Db()
    commands = {"set": database.set, "unset": database.unset,
                "get": database.get, "counts": database.count,
                "begin": database.begin, "rollback": database.rollback,
                "commit": database.commit, "end": database.end}

    while database.is_work:
        user_input = input().split()
        command = user_input[0].lower()
        params = user_input[1:]

        if command not in commands:
            print("Unknown command")
            continue

        commands[command](*params)

        

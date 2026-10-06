from account import Account

class SameUsernameError(Exception):
    pass

class Twitter:
    def __init__(self, accounts = None):
        if accounts is None:
            self.accounts = []
        else:
            self.accounts = accounts

    def create_account(self, username, password):
        for account in self.accounts:
            if (username == account.username):
                raise SameUsernameError(f"Username'{username}' is already taken")
        account = Account(username, password)
        self.accounts.append(account)
            
        
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

    def login(self, username, password):
        for account in self.accounts:
            if account.username == username and account.password == password:
                return account

        print("Invalid username and/or password")
        return None

    def run(self):
        while True:
            print("\nWelcome to Twitter!")
            print("1. Login")
            print("2. Create Account")
            print("3. Quit")

            choice = input("Choose an option: ")

            if choice == "1":
                while True:
                    username = input("Enter username: ")
                    password = input("Enter password: ")

                    account = self.login(username, password)

                    if account is not None:
                        print("Login successful!")
                        print(f"Welcome, {account.username}!")

                        print("\nYour Feed:")
                        if len(account.posts) == 0:
                            print("No posts yet.")
                        else:
                            for post in account.posts:
                                print(post)

                        break

                    retry = input("Would you like to try again? (yes/no): ")
                    if retry.lower() != "yes":
                        break

            elif choice == "2":
                username = input("Choose a username: ")
                password = input("Choose a password: ")

                try:
                    self.create_account(username, password)
                    print("Account created successfully!")

                except SameUsernameError as error:
                    print(error)

            elif choice == "3":
                print("Goodbye!")
                break

            else:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    twitter = Twitter()
    twitter.run()

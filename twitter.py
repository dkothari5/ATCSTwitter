from account import Account

# Custom exceptions
class SameUsernameError(Exception):
    pass

class LoginError(Exception):
    pass

class Twitter:

    # Constructor
    def __init__(self, accounts = None):
        # So when you deserialize all of the accounts will be saved but if it is a new run then nothing will be saved
        if accounts is None:
            self.accounts = []
        else:
            self.accounts = accounts

    def check_username(self, username):
        # Goes through all of the accounts and if that exact username is taken than throw an error
        for account in self.accounts:
            if (username == account.username):
                raise SameUsernameError(f"Username '{username}' is already taken")
    
    def create_account(self, username, password):
        # If unique username create a new account and add it to the accounts
        account = Account(username, password)
        self.accounts.append(account)

    def login(self, username, password):
        for account in self.accounts:
            if account.username == username and account.password == password:
                return account

        raise LoginError(f"Invalid username and/or password")

    def show_feed(self, user):
        print("\nYour Feed:")

        # If not following any account remind the user
        if len(user.following) == 0:
            print("You haven't followed anyone")

        # Go through every account followed and print out all their posts
        else:     
            for account in user.following:
                for post in account.posts:
                    print(post)
                

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

                    try:
                        account = self.login(username, password)
                        print("\nSuccessful Login!")
                        self.show_feed(account)
                        break
                    except LoginError as e:
                        print(e)

                    retry = input("Would you like to try again? (yes/no): ")
                    if retry.lower() != "yes":
                        break

            elif choice == "2":

                username = input("Choose a username: ")
                try:
                    self.check_username(username)
                except SameUsernameError as e:
                    print(e)
                    continue
                password = input("Choose a password: ")
                self.create_account(username, password)
                print("Account created successfully!")

            elif choice == "3":
                print("Goodbye!")
                break

            else:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    twitter = Twitter()
    twitter.run()

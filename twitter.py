from account import Account, AlreadyFollowingError, SameTitleError, SelfFollowError
from post import Post
import json

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
                
    def follow_account(self, user, username):
        # Allows user to follow an account by matching the username of the account the user wishes to follow with the actual username of the account
        for account in self.accounts:
            if account.username == username:
                user.follow(account)
                print("Successfully followed " + username)
                return
        # If there is no actual account with the username of the account the user wishes to follow then return a failure message
        print("Account not found")

    def home_page(self, account):
        # In App Options
        print("\n1. View Feed")
        print("2. Follow Account")
        print("3. Create Post")
        print("4. Logout")                    
        choice = input("Choose an option: ")

        # Shows Feed
        if choice == "1":
            self.show_feed(account)

        # Follow Account
        elif choice == "2":
            username_to_follow = input("Enter username to follow: ")

            # Will check if the account is a valid follow
            try:
                self.follow_account(account, username_to_follow)
            except (AlreadyFollowingError, SelfFollowError) as e:
                print(e)

        
        # Create Post
        elif choice == "3":
            title = input("Enter post title: ")
            text = input("Enter post text: ")

            # Try and create the post
            try:
                account.create_post(title, text) 
                print("Post created successfully!")
            except SameTitleError as e:
                print(e) 
        
        # Logout    
        elif choice == "4":
            print("Logged out!")
            return False
        
        # If user does not enter 1, 2, 3, or 4, they will be prompted to try again
        else:
            print("Invalid option. Please try again.")   
        return True    

    def run(self):
        while True:
            # Pre-login Options
            print("\nWelcome to Twitter!")
            print("1. Login")
            print("2. Create Account")
            print("3. Quit")
            choice = input("Choose an option: ")

            # Login
            if choice == "1":
                while True:
                    username = input("Enter username: ")
                    password = input("Enter password: ")

                    # Check if valid login, if not let them try again
                    try:
                        account = self.login(username, password)
                    except LoginError as e:
                        print(e)
                        retry = input("Would you like to try again? (yes/no): ")
                        if retry.lower() != "yes":
                            break
                        continue
                    # If valid then take them to home page
                    print("\nSuccessful Login!")
                    while self.home_page(account):
                        pass
                    break
                        
            # Create Account
            elif choice == "2":
                try:

                    # Checks if valid username first before asking for password
                    username = input("Choose a username: ")
                    self.check_username(username)
                except SameUsernameError as e:
                    print(e)
                    continue

                # Creates the account
                password = input("Choose a password: ")
                self.create_account(username, password)
                print("Account created successfully!")

            # Quit
            elif choice == "3":
                print("Goodbye!")
                break

            # If user does not enter 1, 2, or 3 they will be prompted to try again
            else:
                print("Invalid option. Please try again.")

    def to_dict(self):
        return {"accounts": [account.to_dict() for account in self.accounts]}

    def save_to_file(self, file_path = "save.json"):
        with open(file_path, "w") as file:
            json.dump(self.to_dict(), file)
        print("Saved!")

    def load_from_file(self, file_path = "save.json"):
        try:
            with open(file_path) as file:
                data = json.load(file)
        except FileNotFoundError:
            return

        # Create the accounts list and a dictionary to store the username and the account it leads to
        self.accounts = []
        username_to_account = {}

        # Go through every account in the file
        for account in data["accounts"]:

            # Get the posts for that account
            posts = [Post(post["title"], post["text"], post["poster"]) for post in account["posts"]]

            # Append the account without the followed section
            account = Account(account["username"], account["password"], posts)
            self.accounts.append(account)

            # Add to the dictionary the username as the key and the created account as the value
            username_to_account[account.username] = account

        # Go through every account in the file
        for account_data in data["accounts"]:

            # Get the account without the followed accounts from the dictionary
            account = username_to_account[account_data["username"]]

            # Go through the account in the file and the usernames of the account they are following
            for name in account_data["following"]:

                # Find the actual account using the dictionary and add it to the followed accounts
                account.following.append(username_to_account[name])
            


if __name__ == "__main__":
    twitter = Twitter()
    twitter.load_from_file()
    twitter.run()
    twitter.save_to_file()

from password_manager import PasswordManager


def main():
    password_manager = PasswordManager()
    while True:
        print("\n\nPlease enter the number of option, from given menu or enter 'quit' to quit the program:")
        print("1- Generate Password")
        print("2- Save new password")
        print("3- List passwords")
        user_choice = input("> ")
        if user_choice == "quit":
            exit()
        if user_choice == "1":
            password_manager.generate_password_with_user_input()
        elif user_choice == "2":
            password_manager.add_credential_item_with_user_input()
        elif user_choice == "3":
            password_manager.print_credential_items()
        else:
            print("Wrong input try again.")
            



main()
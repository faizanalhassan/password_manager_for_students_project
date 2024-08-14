import random
import pickle
import psycopg2
from credential_item import CredentialItem

DATA_FILE_NAME = "credentials.bin"
class PasswordManager:
    def __init__(self):
        self.lower_chars = "abcdefghijklmnopqrstuvwxyz"
        self.upper_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.number_chars = "0123456789"
        self.symbol_chars = "!@#$%^&*()_+=\/<>"
        self.credential_items = []
        self.conn = psycopg2.connect(database="password_manager",
                        host="localhost",
                        user="postgres",
                        password="password",
                        port="5432")

    
    def get_bool_input_from_user(self, prompt_substring):
        choice = input(f"Do you want to include {prompt_substring}? (Y/n): ")
        choice = choice.lower()
        if choice == "n":
            return False
        return True


    def save_data(self):
        file_handler = open(DATA_FILE_NAME, "wb")
        pickled_credentials = pickle.dumps(self.credential_items)
        file_handler.write(pickled_credentials)
        file_handler.close()

    def load_data(self):
        file_handler = open(DATA_FILE_NAME, "rb")
        pickled_data = file_handler.read()
        credentials = pickle.loads(pickled_data)
        self.credential_items = credentials

    def generate_password(self, 
                          length=10,
                           is_upper_included=True,
                             is_lower_included=True,
                               is_number_included=True,
                                 is_symbol_included=True):
        password = ""
        if length == 0 or (
            is_lower_included is False 
            and is_number_included is False 
            and is_symbol_included is False 
            and is_upper_included is False):
            return password
        characters_set = ""
        if is_lower_included:
            characters_set += self.lower_chars
        if is_number_included:
            characters_set += self.number_chars
        if is_symbol_included:
            characters_set += self.symbol_chars
        if is_upper_included:
            characters_set += self.upper_chars
        while len(password) < length:
            waseem = random.randrange(0, len(characters_set))
            char = characters_set[waseem]
            password += char
            

        return password
    

    def generate_password_with_user_input(self):
        password_length = input("Please enter length of password: ")
        if not password_length.isdigit():
            print("Invlid input. You must give postivie integer value. Returning to main menu.")
            return
        password_length = int(password_length)
        input_lower = self.get_bool_input_from_user("lower characters")
        input_upper = self.get_bool_input_from_user("upper characters")
        input_number = self.get_bool_input_from_user("number characters")
        input_symbol = self.get_bool_input_from_user("symbol characters")
        if input_lower is False and input_number is False and input_symbol is False and input_upper is False:
            print("You have selected 'n' for all flags, cannot generate password for you. returning to main menu.")
            return
        password = self.generate_password(
            password_length,
            is_lower_included=input_lower,
            is_number_included=input_number,
            is_upper_included=input_upper,
            is_symbol_included=input_symbol
        )
        print("Your password with", end='')
        if input_lower:
            print(" lower characters ", end='')
        if input_number:
            print(" and numbers ", end='')
        if input_symbol:
            print(" and symbols ", end='')
        if input_upper:
            print(" and upper characters ", end='')
        print(f"is: {password}")

    def add_credential_item(self,  name, username, password, category=None, notes=None):
        # ci = CredentialItem(
        #     name=name,
        #     username=username,
        #     password=password,
        #     category=category,
        #     notes=notes
        # )
        # self.credential_items.append(ci)
        cusrsor = self.conn.cursor()
        cusrsor.execute("select id, name from category where name = %s", (category,))
        result = cusrsor.fetchone()
        if result:
            category_id = result[0]
        else:
            cusrsor.execute("insert into category(name) values(%(name)s) RETURNING id;", {"name": category})
            result_tuple = cusrsor.fetchone()
            category_id = result_tuple[0]
        cusrsor.execute("""
        insert into credential (category_id, "name", username, "password", notes) values (%s, %s, %s, %s, %s);
        """, (category_id, name, username, password, notes))
        self.conn.commit()
        cusrsor.close()

    def add_credential_item_with_user_input(self):
        name = input("Please enter name for your credential item: ")
        username = input("Please enter username for your credential item: ")
        password = input("Please enter password for your credential item: ")
        category = input("Please enter category for your credential item: ")
        notes = input("Please enter notes for your credential item: ")
        return self.add_credential_item(
            name,
            username,
            password,
            category,
            notes
        )


    def print_credential_items(self):
        print("name\t\t\tusername\t\t\tpassword\t\t\tcategory\t\t\tnotes")
        for credential_item in self.credential_items:
            print(f"{credential_item.name}\t\t\t{credential_item.username}"
                  f"\t\t\t{credential_item.password}"
                  f"\t\t\t{credential_item.category}\t\t\t{credential_item.notes}")
            
    
    def list_crdentials(self):
        cusrsor = self.conn.cursor()
        cusrsor.execute("""
            select id, name, username, password, category_id, notes
            from credential;
        """)
        credentials_list_of_tuple = cusrsor.fetchall()
        credentials_list_of_dict = []
        for credential_tuple in credentials_list_of_tuple:
            credenital_dict = {
                "id": credential_tuple[0],
                "name": credential_tuple[1],
                "username": credential_tuple[2],
                "password": credential_tuple[3],
                "category_id": credential_tuple[4],
                "notes": credential_tuple[5],
            }
            # note: query in loop is very bad approach,we are just doing it for learing purpose, because we haven't learn other ways yet.
            cusrsor.execute("select id, name from category where id = %s", (credenital_dict["category_id"],))
            result = cusrsor.fetchone()
            if result:
                credenital_dict["category_name"] = result[1]
            else:
                credenital_dict["category_name"] = ''
            credentials_list_of_dict.append(credenital_dict)
        return credentials_list_of_dict






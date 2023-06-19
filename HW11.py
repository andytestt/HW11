from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value=None):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self):
        super().__init__()
    
    @Field.value.setter
    def value(self, value):
        if isinstance(value, str) and value.isdigit():
            self._value = value
        else:
            print('The phone number must contain only digits.')


class AddressBook(UserDict):
    def __iter__(self):
        return iter(self.data.values())
    
    def add_record(self, record):
        self.data[record.name.value] = record


class Record:
    def __init__(self, name, birthday=None):
        self.name = name
        self.phone = Phone()
        self.birthday = birthday
    
    def add_phone(self, phone):
        self.phone.value = phone
    
    def remove_phone(self, phone):
        if self.phone.value == phone:
            self.phone.value = None
    
    def edit_phone(self, old_phone, new_phone):
        if self.phone.value == old_phone:
            self.phone.value = new_phone
    
    def days_to_birthday(self):
        if self.birthday is None:
            return None
        today = datetime.now().date()
        next_birthday_year = today.year
        birthday_this_year = datetime(next_birthday_year, self.birthday.month, self.birthday.day).date()
        if birthday_this_year < today:
            next_birthday_year += 1
            birthday_this_year = datetime(next_birthday_year, self.birthday.month, self.birthday.day).date()
        return (birthday_this_year - today).days


contacts = AddressBook()

def add_contact(name, phone, birthday=None):
    record = Record(Name(), birthday)
    record.name.value = name
    record.add_phone(phone)
    contacts.add_record(record)
    return "Contact added successfully."

def change_phone(name, phone):
    if name in contacts.data:
        record = contacts.data[name]
        record.add_phone(phone)
        return "Phone number updated successfully."
    else:
        raise KeyError("Contact not found.")

def get_phone(name):
    if name in contacts.data:
        record = contacts.data[name]
        return record.phone.value
    else:
        raise KeyError("Contact not found.")

def get_days_to_birthday(name):
    if name in contacts.data:
        record = contacts.data[name]
        days = record.days_to_birthday()
        if days is not None:
            return f"Days to next birthday: {days}"
        else:
            return "No birthday set for this contact."
    else:
        raise KeyError("Contact not found.")

def display_contacts():
    if len(contacts.data) == 0:
        return "No contacts found."
    else:
        output = ""
        for record in contacts:
            output += f"{record.name.value}: {record.phone.value}\n"
        return output.strip()

def main():
    print("How can I help you?")

    while True:
        command = input("> ").lower()

        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            try:
                _, name, phone, *birthday = command.split(" ")
                if birthday:
                    birthday = datetime.strptime(" ".join(birthday), "%Y %m %d")
                else:
                    birthday = None
                print(add_contact(name, phone, birthday))
            except ValueError:
                print("Invalid input. Please enter name and phone number separated by a space.")
            except TypeError:
                print("Invalid birthday format. Please enter year, month, and day separated by spaces.")
        elif command.startswith("change"):
            try:
                _, name, phone = command.split(" ")
                print(change_phone(name, phone))
            except ValueError:
                print("Invalid input. Please enter name and phone number separated by a space.")
            except KeyError:
                print("Contact not found.")
        elif command.startswith("phone"):
            try:
                _, name = command.split(" ")
                print(get_phone(name))
            except ValueError:
                print("Invalid input. Please enter a name.")
            except KeyError:
                print("Contact not found.")
        elif command.startswith("birthday"):
            try:
                _, name = command.split(" ")
                print(get_days_to_birthday(name))
            except ValueError:
                print("Invalid input. Please enter a name.")
            except KeyError:
                print("Contact not found.")
        elif command == "show all":
            print(display_contacts())
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()

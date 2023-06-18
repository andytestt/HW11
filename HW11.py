from collections import UserDict
from datetime import datetime, timedelta

class AddressBook(UserDict):
    def __iter__(self):
        return AddressBookIterator(self.data)
    
    def add_record(self, record):
        self.data[record.name.get_value()] = record

class AddressBookIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        key = list(self.data.keys())[self.index]
        record = self.data[key]
        self.index += 1
        return f"{key}: {record.phone.get_value()}"

class Record:
    def __init__(self, name, birthday=None):
        self.name = name
        self.phone = Phone()
        self.birthday = birthday
    
    def add_phone(self, phone):
        self.phone.add_phone(phone)
    
    def remove_phone(self, phone):
        self.phone.remove_phone(phone)
    
    def edit_phone(self, old_phone, new_phone):
        self.phone.edit_phone(old_phone, new_phone)
    
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

class Field:
    def __init__(self):
        self.value = None
    
    def set_value(self, value):
        self.validate(value)
        self.value = value
    
    def get_value(self):
        return self.value
    
    def validate(self, value):
        pass

class Name(Field):
    def set_value(self, value):
        if not value:
            raise ValueError("Name field cannot be empty.")
        super().set_value(value)

class Phone(Field):
    def __init__(self):
        super().__init__()
        self.value = []
    
    def add_phone(self, phone):
        self.validate(phone)
        self.value.append(phone)
    
    def remove_phone(self, phone):
        if phone in self.value:
            self.value.remove(phone)
    
    def edit_phone(self, old_phone, new_phone):
        self.validate(new_phone)
        if old_phone in self.value:
            index = self.value.index(old_phone)
            self.value[index] = new_phone
    
    def validate(self, phone):
        if not isinstance(phone, str) or not phone.isdigit():
            raise ValueError("Phone number should be a string of digits.")

class Birthday(Field):
    def set_value(self, value):
        self.validate(value)
        super().set_value(value)
    
    def validate(self, value):
        if value is not None and not isinstance(value, datetime):
            raise ValueError("Birthday should be a datetime object or None.")

contacts = AddressBook()

def add_contact(name, phone, birthday=None):
    record = Record(Name(), Birthday())
    record.name.set_value(name)
    record.add_phone(phone)
    if birthday is not None:
        record.birthday.set_value(birthday)
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
        return record.phone.get_value()
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
        for contact in contacts:
            output += contact + "\n"
        return output.strip()

def main():
    print("How can I help you?")

    while True:
        command = input("> ").lower()

        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            try:
                _, name, phone = command.split(" ")
                print(add_contact(name, phone))
            except ValueError:
                print("Invalid input. Please enter name and phone number separated by a space.")
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

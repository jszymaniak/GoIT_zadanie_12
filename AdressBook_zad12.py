from collections import UserDict
from dataclasses import dataclass
from datetime import datetime
import pickle

class AddressBook(UserDict):
    def __iter__(self):
        return iter(self.data.values())
    
    def add_record(self, record):
        key = record.name.value
        self.data[key] = record
    
    def iterator(self, N):
        records = list(self.data.values())
        for i in range(0, len(records), N):
            yield records[i:i + N]

    def save(self, file_name):
        with open(file_name, "wb") as file:
            pickle.dump(self.data, file)

    def load(self, file_name):
        try:
            with open(file_name, "rb") as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            print("File not found.")

    
    def search(self, query):
        result = []
        for record in self.data.values():
            if query.lower() in record.name.value.lower():
                result.append(record)
            for phone in record.phones:
                if query in phone.value:
                    result.append(record)
                    break
        return result

@dataclass
class Field:
    value: str

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        self._value = new_value
    
class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value):
        if not new_value.isdigit():
            raise ValueError("Wrong number.")
        self._value = new_value

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
    
    @Field.value.setter
    def value(self, new_value):
        try:
            datetime.strptime(new_value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Wrong date.")
        self._value = new_value


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday
        if birthday:
            self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        rmv = Phone(phone)
        if rmv in self.phones:
            self.phones.remove(rmv)

    def edit_phone(self, old_phone, new_phone):
        _old_phone = Phone(old_phone)
        if _old_phone in self.phones:
            index = self.phones.index(_old_phone)
            self.phones[index] = Phone(new_phone)    

    def days_to_birthday(self):
        if self.birthday is not None:
            birthday = datetime.strptime(self.birthday.value, "%d.%m.%Y")
            today = datetime.now()
            next_birthday = birthday.replace(year=today.year)
            if today > next_birthday:
                next_birthday = birthday.replace(year=today.year + 1)
            days_to_birthday = (next_birthday - today).days
            return f"Days to birthday: {days_to_birthday}."

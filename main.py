from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value
    
    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        super().__init__(name)

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if value.isnumeric() and len(value) == 10:
            self._Field__value = value
        else:
            raise ValueError('Phone is not valid')
        
class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        try:
            datetime.strptime(value, '%Y.%m.%d')
            return True
        except ValueError:
            return False

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.__birthday = None
        if Birthday(birthday):
            self.birthday = birthday
        else:
            self.birthday = None

    def add_phone(self, phone_number):
        valid_number = Phone(phone_number)
        if not valid_number is None:
            self.phones.append(valid_number)
        else:
            return 'Phone is not valid'
        
    def remove_phone(self, phone_number):
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)

    def edit_phone(self, old_phone_number, new_phone_number):
        phone = self.find_phone(old_phone_number)
        if phone:
            phone.value = new_phone_number
        else:
            raise ValueError('Phone not found')

    def find_phone(self, phone):
        valid_number = Phone(phone)
        for ph in self.phones:
            if ph.value == valid_number.value:
                return ph
            
    def days_to_birthday(self,):
        if isinstance(self.birthday, Birthday):
            new_day = '2023' + self.birthday[4:]
            birth_day = datetime.strptime(new_day, '%Y.%m.%d')
            if datetime.strptime(new_day, '%Y.%m.%d') < datetime.now():
                new_day = '2024' + self.birthday[4:]
                birth_day = datetime.strptime(new_day, '%Y.%m.%d')
            return (birth_day - datetime.now()).days + 1
        else:
            raise ValueError('Birthday is not correct')


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        if isinstance(record, Record):
            self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            print(f"Not found")

    def iterator(self, count_res):
        counter = 0
        result = ''
        for item, record in self.data.items():
            result += F'{item}: {record}'
            counter += 1
            if counter >= count_res:
                yield result
                counter = 0
                result = ''


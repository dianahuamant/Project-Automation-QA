from faker import Faker

fake = Faker()

def random_first_name():
    return fake.first_name()

def random_last_name():
    return fake.last_name()

def random_email():
    return fake.email()

def random_zip_code():
    return fake.zipcode()

def random_password():
    return fake.password(length=10)

def random_phone():
    return fake.phone_number()

def random_address():
    return fake.street_address()

def random_city():
    return fake.city()

def random_country():
    return fake.country()
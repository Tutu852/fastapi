from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class Patient(BaseModel):
    name:str
    gender:str
    age:str
    address: Address

address_dict = {
    'street': '123 Main St',
    'city': 'Anytown',
    'zip_code': '12345'
    }
adderess_obj = Address(**address_dict)

patient_info={'name':'rajesh Kumar','gender':'male','age':'27','address':adderess_obj}
patient = Patient(**patient_info)
print(patient)
print(patient.address.city)
print(patient.address.zip_code)
print(patient.address.street)


# why we use nested models?
# Better organization if realated date (e.g., vitals,address,insurance)

# Reusability of models across different parent models(e.g., Address model used in Patient and Hospital models)

# Readability : Easier for developers to API consumers to undeerstand structure and relationships of data

# Validation : Each nested models are validated independently ensuring data integrity at all levels
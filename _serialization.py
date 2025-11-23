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

# it will convert the model to a dictionary
# temp = patient.model_dump()

# using include i can select specific fields to dump
temp = patient.model_dump(include={'name','age'})

#exlude_unset=True  ye un fields ko exclude kar dega jinka value set nahi hua hai
# temp = patient.model_dump(exclude_unset=True)

print(temp)
print(type(temp))

# it will convert the model to a json string
temp2= patient.address.model_dump_json()
print(temp2)
print(type(temp2))



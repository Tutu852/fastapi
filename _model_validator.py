from pydantic import BaseModel,EmailStr,field_validator,model_validator
from typing import List, Dict, Optional


class Patient(BaseModel):
    name:str
    email:EmailStr
    age:int
    weight:float
    married:bool
    allergies: Optional[List[str]]
    contact_Details : Dict[str, str]

    @model_validator(mode="after")

    def check_emergency_contact(self):
        if self.age > 60:
            if 'emergency_contact' not in self.contact_Details:
                raise ValueError("Emergency contact is required for patients over 60")
        return self
    
def update_patient_data(patient:Patient):
        print(patient.name)
        print(patient.email)
        print(patient.age)
        print(patient.weight)
        print(patient.married)
        print(patient.allergies)
        print(patient.contact_Details)
        print('updating data into the database')

patient_info={'name':'rajesh Kumar','email':'852tutukumar@gmail.com','age':'66','weight':45.5,"married"  :True, 'allergies':['pollen','dust'],
              'contact_Details':{'email':'rajeshKumarBehera.com', 'phone':'8249607661' ,'emergency_contact':'234213143' } }
    
# this is a object of Patient class
patient2 = Patient(**patient_info)
update_patient_data(patient2)
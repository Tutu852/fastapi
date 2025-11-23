from pydantic import BaseModel,EmailStr,computed_field
from typing import List, Dict, Optional


class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    height:float
    married: bool
    allergies: Optional[List[str]]
    contact_Details : Dict[str, str]

    #these are decorators
    @computed_field
    # @property in Python is mainly used for creating getter and setter methods — but in a clean and elegant way (without using parentheses () when calling them).
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
def update_patient_data(patient:Patient):
        print(patient.name)
        print(patient.email)
        print(patient.age)
        print(patient.weight)
        print(patient.height)
        print('BMI' ,patient.bmi)
        print(patient.married)
        print(patient.allergies)
        print(patient.contact_Details)
        print('updating data into the database')

patient_info={'name':'rajesh Kumar','email':'852tutukumar@gmail.com','age':'66','weight':45.5,'height':1.72,"married"  :True, 'allergies':['pollen','dust'],
              'contact_Details':{'email':'rajeshKumarBehera.com', 'phone':'8249607661' ,'emergency_contact':'234213143' } }
    
# this is a object of Patient class
patient2 = Patient(**patient_info)
update_patient_data(patient2)
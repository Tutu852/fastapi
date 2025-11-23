
from pydantic import BaseModel, EmailStr,field_validator,model_validator
from typing import List, Dict, Optional

# create a pydantic model for patient data with custom validation
# agar age 60 se jyada he then contact_details me 'emergency_contact' key hona chahiye bar na nehni hoga

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: Optional[List[str]]
    contact_Details : Dict[str, str]

    # model_validator multiple fields ko combine karke validate karne me help kartahe
    @model_validator(mode="after")
    def chack_emergency_contact(self):
        if self.age > 60:
            if 'emergency_contact' not in self.contact_Details:
                raise ValueError("Emergency contact is required for patients over 60")
        return self

    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        valid_domains = ["gmail.com", "yahoo.com", "outlook.com"]
        # abc@gmail.com issme se mujhe gmail.com chahiye
        domain = value.split("@")[-1]
        if domain not in valid_domains:
            raise ValueError("Invalid email address")
        return value
    
    # default mode="after " hi hota hai
    @field_validator('name')
    @classmethod
    def validate_name(cls,value):
         return value.upper()
    
    # before means ki validation value set hone se pehle hoga
    #agar me age '30' before se wo type coursion karke int me convert karega
    # dekho yahna age string me he to ye error dega but if i change to after mode then ye string ko int me convert karega
    @field_validator('age',mode="after")
    @classmethod
    def validate_age(cls,value):
         if 0 <  value < 120:
              return value
         else:
                raise ValueError("Age must be between 0 and 120")

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
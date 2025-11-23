from pydantic import BaseModel, Field,EmailStr
from typing import List,Dict,Optional,Annotated
# create a pydantic model for patient data

class Patient(BaseModel):
    # after annottated give the date type then the field function to add more metadata
    name: Annotated [str , Field(..., description="Name of the patient", example="Rajesh kumar")]
    # here EmailStr is a special type provided by pydantic to validate email format
    email: EmailStr = Field(..., description="Email address of the patient", example="rajeshKumarBehera.com")
    #ge means greater than or equal to 0
    #le means less than or equal to 120
    age: int = Field(..., ge=0, le=120, description="Age of the patient", example=30)
    # gt means greater than 0
    # this strict will ensure that only float values are accepted not int
    weight: Annotated[float , Field(..., gt=0, description="Weight of the patient in kg", example=70.5,strict=True)]
    married:bool = Field(False, description="Marital status of the patient", example=False)
    # yahna ye khud me list he par har ek list ke andar string he
    allergies: Optional[List[str]] = Field([], description="List of allergies", example=["pollen", "nuts"])
    contact_Details : Dict[str, str] = Field({}, description="Contact details of the patient")
                                                                                                    

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_Details)
    print('insterting data into the database')

def update_patient_data( patient: Patient):
 
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_Details)
    print('updating data into the database')

patient_info={'name':'rajesh Kumar','email':'852tutukumar@gmail.com','age':27,'weight':45.5,"married"  :True, 'allergies':['pollen','dust'],
              'contact_Details':{'email':'rajeshKumarBehera.com', 'phone':'8249607661'} }
# *Unpacks a list or tuple Example: func(*[1, 2, 3])
# **Unpacks a dictionary Example: func(**{"a": 1, "b": 2})
patient1 = Patient(**patient_info)

# insert_patient_data(patient1)
update_patient_data(patient1)

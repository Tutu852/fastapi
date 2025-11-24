from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse 
import json
from typing import Annotated, Literal,Optional

app = FastAPI()

# this is patient pydantic model
class Patient(BaseModel):

    id: Annotated[str, Field(..., description="unique identifier for the patient", example="P001")]
    name: Annotated[str, Field(..., description="Name of the patient", example="Rajesh kumar")]
    city: Annotated[str, Field(..., description="City where the patient resides", example="New York")]
    age: Annotated[int, Field(..., ge=0, le=120, description="Age of the patient", example=30)]
    gender: Annotated[Literal['male', 'female', 'other'], Field(..., description="Gender of the patient", example="male")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in cm", example=175.5)]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kg", example=70.5)]

    # there is two more filed is there bmi and verdict i will calculate dynamically useing patient class height and weight

    # jab me kisi field ko dynamically calculate karna chata hu to me computed_field ka use karta hu
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / ((self.height / 100) ** 2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal weight"
        else:
            return "Overweight"
        
# for update and delete i am creating a new pydantic model without id field because there all are required fields except id
class PatientUpdate(BaseModel):
    name:Annotated[Optional[str],Field(None, description="Name of the patient", example="Rajesh kumar")]
    city:Annotated[Optional[str],Field(None,description="City where the patient resides", example="New York")]
    age:Annotated[Optional[int],Field(None,ge=0,le=120, description="Age of the patient", example=30)]
    gender:Annotated[Optional[Literal['male','female','other']], Field(None, description="Gender of the patient", example="male")]
    height:Annotated[Optional[float],Field(None,gt=0, description="Height of the patient in cm",example=175.5)]
    weight:Annotated[Optional[float], Field(None, gt=0, description="Weight of the patient in kg", example=70.5)]



# improved to handle missing or empty file gracefully
def load_data():
    try:
        with open('patients.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# save data function
def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)


@app.get("/")
def hello():
    return {'message': "Patient Management System API"}


@app.get("/about")
def about():
    return {'message': 'A Fully functional API to manage your patient records'}


@app.get("/view")
def view():
    data = load_data()
    return data


@app.get("/patient/{patient_id}")
# ... means required
# using path function i am improving my readbility
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', example='P001')):
    # load all the patient
    data = load_data()
    # it is checking patient_id key present he ki nehni data
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')


@app.get("/sort")
def sort_Patients(
    sort_by: str = Query(..., description='Sort on the basis of height weight or bmi'),
    order: str = Query('asc', description='Sort in asc or desc order')
):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        # ✅ fixed string formatting
        raise HTTPException(status_code=400, detail=f'Invalid field. Select from {valid_fields}')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')

    data = load_data()

    sort_order = True if order == 'desc' else False
    # agar reverse true he desc order and agar reverse= false he the asc order me sort hoga
    sorted_data = sorted(data.values(), 
                         key=lambda x: x.get(sort_by, 0), 
                         reverse=sort_order)

    return sorted_data


@app.post('/create')
# jo parameter me patient de rha hu wo patient class ka object hoga
def create_patient(patient: Patient):
    # load all the patient
    data = load_data()

    # check if patient with same id already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient with this ID already exists')

    # add new patient to data
    # yahan pydantic data ko dict me convert kar raha hu
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save updated data back to file
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient created successfully'})

@app.put('/update/{patient_id}')
def update_patient(patient_id:str, patient_update:PatientUpdate):
    data = load_data()

    # checking if patient with given id exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    # get existing patient data
    existing_patient_data = data[patient_id]
    # update only the fields provided in the request
    #exclude_unset=True will only include fields that were explicitly set when creating the model instance.
    patient_update_dict = patient_update.model_dump(exclude_unset=True)
    # updating the existing patient data with new values
    for key ,value in  patient_update_dict.items():
        existing_patient_data[key] = value

    # convert in to pydanctic object to recalculate computed fields
    # existing_patient_data -> pydantic object -> updated bmi + verdict 
    patient_pydantic_obj = Patient(id=patient_id, **existing_patient_data)
    #-> pydantic object -> dict
    existing_patient_data = patient_pydantic_obj.model_dump(exclude=['id'])

    # add this dict to data
    data[patient_id] = existing_patient_data

    #save data
    save_data(data) 

    return JSONResponse(status_code=200, content={'message':'Patient updated successfully'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data = load_data()

    # checking if patient with given id exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    # delete patient
    del data[patient_id]
    # save data
    save_data(data)
    return JSONResponse(status_code=200, content={'message':'Patient deleted successfully'})
    

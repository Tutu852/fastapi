field_validator (validate a single field)
🔥 Use when you want to validate one specific field.

Example:

from pydantic import BaseModel, field_validator

class User(BaseModel):
    username: str

    @field_validator("username")
    def validate_username(cls, value):
        if " " in value:
            raise ValueError("Username cannot contain spaces")
        return value

✔ Validates only one field
✔ Runs when the model is created
🧠 When to use field_validator?

Use it when you want to validate:

length of a string

email format

password strong or not

age must be > 18

anything related to ONE field

✅ 2. model_validator (validate entire model)
🔥 Use when you want to validate multiple fields together.

Example:

from pydantic import BaseModel, model_validator

class User(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def check_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

✔ Used when validation depends on multiple values
✔ Replaces old root_validator
🧠 When to use model_validator?

password == confirm_password

start_date < end_date

quantity <= stock

latitude + longitude checks

cross-field validation

✅ 3. computed_field (virtual field)
🔥 Create a field that doesn’t exist in database, but is calculated automatically.

Example:

from pydantic import BaseModel, computed_field

class Product(BaseModel):
    price: float
    quantity: int

    @computed_field
    def total(self) -> float:
        return self.price * self.quantity

✔ total is NOT stored
✔ it is computed every time model is returned
🧠 When to use computed_field?

total_price = qty * price

age = today – birthdate

full_name = first + last

URL building

file size formatting

🎉 Summary Table (Very Easy)
Feature	Purpose	Applies To	Example Use
field_validator	Validate one field	Single field	Check username has no spaces
model_validator	Validate multiple fields	Entire model	password == confirm_password
computed_field	Create calculated field	Output only	total price, full name
🔥 One-Line Definitions (Interview Answer)

field_validator → Validate and clean a single field.
model_validator → Validate relation between multiple fields.
computed_field → Create dynamic, calculated fields that are not stored.
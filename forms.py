from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField, FloatField, IntegerField, FileField, SelectField,BooleanField,RadioField
from wtforms.validators import InputRequired, EqualTo, DataRequired, Optional, NumberRange

class RegistrationForm(FlaskForm):
    user_name = StringField("User ID", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    password2 = PasswordField("Confirm Password", validators=[InputRequired(),EqualTo("password")])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    user_name = StringField("User ID", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Sign In")

class addItem(FlaskForm):
    product = StringField("Product Name", validators=[InputRequired()])
    description = StringField("Description:", validators=[InputRequired()])
    price  = FloatField("Price:", validators=[InputRequired()])
    stock = IntegerField("Stock:", validators=[InputRequired()])
    size = StringField("Size:", validators=[InputRequired()])
    category = SelectField("Category",choices=['Kayaks','Dry Suits','Wet Suits','Bouyancy Aid','Shoes','Helmet','Spray Deck', 'Towels','Paddles'], validators=[InputRequired()])
    color = StringField("Color", validators=[InputRequired()])
    brand = StringField("Brand", validators=[InputRequired()])
    image = FileField("Image:", validators=[DataRequired()])
    submit = SubmitField("Submit")
class updateForm(FlaskForm):
    product = StringField("Product Name", validators=[InputRequired()])
    description = StringField("Description:", validators=[InputRequired()])
    price  = FloatField("Price:", validators=[InputRequired()])
   
    category = SelectField("Category",choices=['Kayaks','Dry Suits','Wet Suits','Bouyancy Aid','Shoes','Helmet','Spray Deck', 'Towels','Paddles'], validators=[InputRequired()])
    brand = StringField("Brand", validators=[InputRequired()])
    image = FileField("Image:", validators=[Optional()])
    submit = SubmitField("Submit")
class addColorForm(FlaskForm):
    color = StringField("Color", validators=[InputRequired()])
    size = StringField("Size:", validators=[InputRequired()])
    stock = IntegerField("Stock:", validators=[InputRequired()])
    image = FileField("image:",validators=[Optional()])
    submit = SubmitField("Submit")
    
class ChangePassword(FlaskForm):
    password = PasswordField("Password:", validators=[InputRequired()])
    password2 = PasswordField("Confirm Password:", validators=[InputRequired(),EqualTo("password")])
    submit = SubmitField("Change Password")

class QuantityForm(FlaskForm):
    quantity = SelectField("Quantity:", validators=[InputRequired()] ,choices=[])
    submit = SubmitField("Add to basket")

class SearchForm(FlaskForm):
    search = StringField("Search:")
    sort = SelectField("Sort By", choices=["Price, low to high", "Price, high to low", "Alphabetically A - Z", "Alphabetically Z - A"])
    brand = RadioField("Brand", choices=["Palm","NRS"])
    color = RadioField("Color", choices=["Red","Black","Blue"])
    submit = SubmitField("Search")

class IncrementForm(FlaskForm):
    increment = SubmitField("+")
    decrement = SubmitField("-")

class CheckOut(FlaskForm):
    firstName = StringField()
    lastName = StringField()
    address1 = StringField()
    address2 =StringField()
    address3 = StringField()
    postCode = StringField()
    cardDetails = StringField()
    cvc = StringField()
    expiry = StringField()
    submit = SubmitField("Check out")


class ReviewForm(FlaskForm):
    rating = SelectField(choices=[1,2,3,4,5])
    review = StringField()
    image = FileField("image", validators=[Optional()])
    submit = SubmitField()


class ReplyForm(FlaskForm):
    review = StringField("review",validators=[DataRequired()])
    submit = SubmitField()

class SearchUserForm(FlaskForm):
    search = StringField("Search:", validators=[Optional()])
    submit = SubmitField("Search")

class addressForm(FlaskForm):
    firstName = StringField("First Name", validators=[InputRequired()])
    lastName = StringField("Last Name", validators=[InputRequired()])
    address1 = StringField("Address 1", validators=[InputRequired()])
    address2 = StringField("Address 2", validators=[InputRequired()])
    address3 = StringField("Address 3", validators=[InputRequired()])
    postCode = StringField("Post Code", validators=[InputRequired()])
    submit = SubmitField("Submit")
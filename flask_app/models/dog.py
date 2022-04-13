from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.controllers.dog_controller import delete_dog
from flask_app.models import owner

class Dog:
    db= "petshow_schema"
    def __init__(self,data):
        self.id=data["id"]

        self.name=data["name"]
        self.breed=data["breed"]
        self.age=data["age"]
        self.owner_id=data["owner_id"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
       
        self.owner ={}
    @staticmethod
    def validate_dog(data):
        is_valid= True
        if len(data["name"]) <2 :
            flash("Dog name must be at least 2 characters long!")
            is_valid= False
        if len(data["breed"])<3 :
            flash("dog breed must be at least 3 character long")
            is_valid= False


        if data["age"] == "":
            flash("please enter an age for your dog!")
            is_valid= False


        elif int(data["age"]) <3:
            flash("dog must be 3 yearsof age or older")
            is_valid= False

        return is_valid
    @classmethod
    def create_dog(cls,data):
        query= "INSERT INTO dogs (name,breed,age, owner_id, created_at) VALUES (%(name)s, %(breed)s, %(age)s, %(owner_id)s, NOW());"
        results= connectToMySQL("petshow_schema").query_db(query,data)
        return results
    @classmethod
    def get_all(cls):
        query= "SELECT * FROM dogs  LEFT JOIN owners ON dogs.owner_id = owners.id;"
        results =connectToMySQL("petshow_schema").query_db(query)
        all_dogs=[]
    
        for row in results:
            dog = cls(row)
            owner_data= {
                "id" : row["owners.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["created_at"],
                "updated_at" :row["updated_at"]
            }
            dog.owner =owner.Owner(owner_data)
            all_dogs.append(dog) 
        return all_dogs

    @classmethod
    def get_dog_with_owner(cls,data):
        query = "SELECT * FROM dogs LEFT JOIN owners ON dogs.owner_id = owners.id WHERE dogs.id= %(dog_id)s;"
        results = connectToMySQL("petshow_schema").query_db(query,data)

        dog = cls (results[0])
        owner_data= {
                "id" : results[0]["owners.id"],
                "first_name" : results[0]["first_name"],
                "last_name" :results[0]["last_name"],
                "email" : results[0]["email"],
                "password" : results[0]["password"],
                "created_at" : results[0]["owners.created_at"],
                "updated_at" :results[0]["owners.updated_at"]
            }
        dog.owner=owner.Owner(owner_data)
        return dog

    @classmethod
    def update_dog_info(cls,data):
        query = "UPDATE dogs SET name = %(name)s, breed = %(breed)s, age = %(age)s, updated_at = NOW() WHERE id = %(dog_id)s;"
        results= connectToMySQL("petshow_schema").query_db(query, data)
        return

    @classmethod
    def delete_dog(cls, data):
        query ="DELETE FROM dogs WHERE id= %(dog_id)s;"
        results= connectToMySQL("petshow_schema"). query_db(query,data)
        return

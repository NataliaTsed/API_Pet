import json
import requests
from settings import RegisterData, RequestURL, MyPets, OtherPets


class Pets:
    def __init__(self):
        self.base_url = RequestURL.BASE_URL

    def get_token(self) -> json:
        """The method POST/login to the site Swagger is designed to get a unique user token
        with valid email and password."""
        data = {'email': RegisterData.VALID_EMAIL,
                'password': RegisterData.VALID_PASSWORD}
        res = requests.post(self.base_url + 'login', data=json.dumps(data))
        my_token = res.json()['token']
        my_id = res.json()['id']
        status = res.status_code
        return my_token, status, my_id

    def get_list_of_users(self) -> json:
        """The method GET/users to the site Swagger is designed to get a list of users
         by using the token."""
        my_token = Pets().get_token()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        res = requests.get(self.base_url + 'users', headers=headers)
        status = res.status_code
        my_id = res.text
        return status, my_id

    def post_pet(self) -> json:
        """The method POST/pet to the site Swagger is designed to create my pet account."""
        my_token = Pets().get_token()[0]
        my_id = Pets().get_token()[2]
        headers = {'Authorization': f'Bearer {my_token}'}
        data = {"name": MyPets.NAME_CAT, "type": MyPets.TYPE_CAT, "age": MyPets.AGE_CAT, "owner_id": my_id,
                "gender": MyPets.GENDER_CAT}
        res = requests.post(self.base_url + 'pet', data=json.dumps(data), headers=headers)
        status = res.status_code
        return status

    def get_list_of_pets(self) -> json:
        """The method POST/pets to the site Swagger is designed to get a list of my pets"""
        my_token = Pets().get_token()[0]
        my_id = Pets().get_token()[2]
        headers = {'Authorization': f'Bearer {my_token}'}
        data = {"user_id": my_id}
        res = requests.post(self.base_url + 'pets', data=json.dumps(data), headers=headers)
        status = res.status_code
        pets_list = res.json()['list']
        pets_quantity = res.json()['total']
        return status, pets_list, pets_quantity

    def post_pet_photo(self) -> json:
        """""The method POST/pet/{pet_id}/image to the site Swagger is designed to add a photo
        to my pet account."""
        my_token = Pets().get_token()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        pets_list = Pets().get_list_of_pets()[1]
        pet_id = pets_list[0]['id']
        files = {'pic': ('nothing.jpg', open('photo\\kitty.jpg', 'rb'), 'image/jpg')}
        res = requests.post(self.base_url + f'pet/{pet_id}/image', headers=headers, files=files)
        status = res.status_code
        return status 

    def put_pet_like(self) -> json:
        """""The method PUT/pet/{pet_id}/like to the site Swagger is designed to put a like
        to my pet."""
        my_token = Pets().get_token()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        pets_list = Pets().get_list_of_pets()[1]
        pet_id = pets_list[0]['id']
        res = requests.put(self.base_url + f'pet/{pet_id}/like', headers=headers)
        status = res.status_code
        response = res.next
        return status, response

    def put_pet_comment(self) -> json:
        """""The method PUT/pet/{pet_id}/comment to the site Swagger is designed to
        leave a comment to my pet."""
        my_token = Pets().get_token()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        pets_list = Pets().get_list_of_pets()[1]
        pet_id = pets_list[0]['id']
        data = {"message": MyPets.MESSAGE}
        res = requests.put(self.base_url + f'pet/{pet_id}/comment', data=json.dumps(data), headers=headers)
        status = res.status_code
        return status

    def patch_pet_update(self) -> json:
        """The method PATCH/pet to the site Swagger is designed to update my pet account."""
        my_token = Pets().get_token()[0]
        my_id = Pets().get_token()[2]
        headers = {'Authorization': f'Bearer {my_token}'}
        pets_list = Pets().get_list_of_pets()[1]
        pet_id = pets_list[0]['id']
        data = {'id': pet_id, 'name': MyPets.NAME_HAMSTER, 'type': MyPets.TYPE_HAMSTER, 'gender': MyPets.GENDER_HAMSTER,
                'age': MyPets.AGE_HAMSTER, 'owner_id': my_id}
        res = requests.patch(self.base_url + 'pet', data=json.dumps(data), headers=headers)
        status = res.status_code
        return status

    def change_pet_photo(self) -> json:
        """""The method POST/pet/{pet_id}/image to the site Swagger is designed to change a photo
        to my pet account."""
        my_token = Pets().get_token()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        pets_list = Pets().get_list_of_pets()[1]
        pet_id = pets_list[0]['id']
        files = {'pic': ('nothing.jpg', open('photo\\hamster.jpg', 'rb'), 'image/jpg')}
        res = requests.post(self.base_url + f'pet/{pet_id}/image', headers=headers, files=files)
        status = res.status_code
        return status 

    def get_pet_id(self) -> json:
        """""The method GET/pet/{pet_id} to the site Swagger is designed to get the information
                about my pet."""
        my_token = Pets().get_token()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        pets_list = Pets().get_list_of_pets()[1]
        pet_id = pets_list[0]['id']
        res = requests.get(self.base_url + f'pet/{pet_id}', headers=headers)
        status = res.status_code
        inf_pets = res.json()['pet']
        inf_comments = res.json()['comments']
        return status, inf_pets, inf_comments

    def delete_pet_account(self) -> json:
        """""The method DELETE/pet/{pet_id} to the site Swagger is designed to delete
        my pet account."""
        my_token = Pets().get_token()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        pets_list = Pets().get_list_of_pets()[1]
        pet_id = pets_list[0]['id']
        res = requests.delete(self.base_url + f'pet/{pet_id}', headers=headers)
        status = res.status_code
        return status

    def change_not_my_pet(self) -> json:
        """The method PATCH/pet to the site Swagger try to change the data in another
        user's pet account."""
        my_token = Pets().get_token()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        pet_id = 74
        data = {'id': pet_id, 'name': OtherPets.NAME_PET, 'type': OtherPets.TYPE_PET}
        res = requests.patch(self.base_url + 'pet', data=json.dumps(data), headers=headers)
        status = res.status_code
        return status

    def delete_not_my_pet(self) -> json:
        """""The method DELETE/pet/{pet_id} to the site Swagger try to delete another
        user's pet account."""
        my_token = Pets().get_token()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        pet_id = 1529
        res = requests.delete(self.base_url + f'pet/{pet_id}', headers=headers)
        status = res.status_code
        return status

    def expired_token(self) -> json:
        """The method GET/users to the site Swagger try to get a list of users
         by using the expired token."""
        my_token = RegisterData.EXPIRED_TOKEN
        headers = {'Authorization': f'Bearer {my_token}'}
        res = requests.get(self.base_url + 'users', headers=headers)
        status = res.status_code
        return status

    def get_pet_id_without_authorization(self) -> json:
        """""The method GET/pet/{pet_id} to the site Swagger gets the information
                about the pet without authorization."""
        headers = {'Authorization': 'Bearer'}
        pet_id = 1529
        res = requests.get(self.base_url + f'pet/{pet_id}', headers=headers)
        status = res.status_code
        return status

    def put_pet_like_without_authorization(self) -> json:
        """""The method PUT/pet/{pet_id}/like to the site Swagger try to put a like
        to the pet without authorization."""
        headers = {'Authorization': 'Bearer'}
        pet_id = 1529
        res = requests.put(self.base_url + f'pet/{pet_id}/like', headers=headers)
        status = res.status_code
        return status

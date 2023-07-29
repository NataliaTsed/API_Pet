import pytest

from api import Pets

pet = Pets()

"""Precondition: I'm registered on the website by using method POST/Register.
And I don't have any pet accounts."""


@pytest.mark.authorized
@pytest.mark.positive_testing
def test_get_token():
    """This test gets a unique token."""
    status = pet.get_token()[1]
    token = pet.get_token()[0]
    my_id = pet.get_token()[2]
    assert token
    assert status == 200
    assert my_id


@pytest.mark.authorized
@pytest.mark.positive_testing
def test_get_list_of_users():
    """This test gets a list of site users. Actual result - only my user id was received."""
    status = pet.get_list_of_users()[0]
    my_id = pet.get_list_of_users()[1]
    assert status == 200
    assert my_id


@pytest.mark.authorized
@pytest.mark.positive_testing
def test_check_list_of_my_pets():
    """This test makes sure that there are no created pets in my profile."""
    pet_list = pet.get_list_of_pets()[1]
    pets_quantity = pet.get_list_of_pets()[2]
    assert pet_list == []
    assert pets_quantity == 0


@pytest.mark.authorized
@pytest.mark.positive_testing
def test_create_pet():
    """This test creates a pet."""
    status = pet.post_pet()
#    pets_list = Pets().get_list_of_pets()[1]  # pet_id беру из метода GET, чтоб тест не создал второго питомца
#    pet_id = pets_list[0]['id']  # правильно ли это? Или надо брать именно из метода POST?
    assert status == 200
#    assert pet_id


@pytest.mark.authorized
@pytest.mark.positive_testing
def test_get_list_of_pets():
    """This test makes sure that the pet is created in my profile."""
    status = pet.get_list_of_pets()[0]
    pets_list = pet.get_list_of_pets()[1]
    pets_quantity = pet.get_list_of_pets()[2]
    assert status == 200
    assert pets_list
    assert pets_quantity


@pytest.mark.authorized
@pytest.mark.positive_testing
def test_add_pet_photo():
    """This test adds a photo to the pet's account."""
    status = pet.post_pet_photo()
    #    link = pet.post_pet_photo()[0]
    assert status == 200
    #    assert link


@pytest.mark.authorized
@pytest.mark.positive_testing
def test_add_pet_like():
    """This test puts a like to the pet's account."""
    status = pet.put_pet_like()[0]
    response = pet.put_pet_like()[1]
    response_body = None
    assert status == 200
    assert response == response_body  # имеет смысл здесь это проверять?


@pytest.mark.authorized
@pytest.mark.positive_testing
def test_add_pet_comment():
    """This test adds a comment to the pet's account."""
    status = pet.put_pet_comment()
    assert status == 200


@pytest.mark.authorized
@pytest.mark.positive_testing
def test_update_pet_account():
    """This test updates the information in the pet's account."""
    status = pet.patch_pet_update()
    #    id_updated_pet = pet.patch_pet_update()[1] # два раза обновит здесь запись, потому что два раза вызывается
    assert status == 200
    #    assert id_updated_pet


@pytest.mark.authorized
@pytest.mark.positive_testing
def test_change_pet_photo():
    """This test changes a photo to the pet's account."""
    status = pet.change_pet_photo()
    assert status == 200


@pytest.mark.authorized
@pytest.mark.positive_testing
def test_check_info_about_pet():
    """This test makes sure that all the entered information is contained
     in the pet's account."""
    status = pet.get_pet_id()[0]
    inf_pets = pet.get_pet_id()[1]
    inf_comments = pet.get_pet_id()[2]
    assert status == 200
    assert inf_pets
    assert inf_comments


@pytest.mark.authorized
@pytest.mark.positive_testing
def test_delete_pet():
    """This test deletes the pet's account."""
    status = pet.delete_pet_account()
    assert status == 200


@pytest.mark.authorized
@pytest.mark.positive_testing
def test_checking_for_deletion():
    """This test makes sure that pet's account was deleted in my profile."""
    pet_list = pet.get_list_of_pets()[1]
    pets_quantity = pet.get_list_of_pets()[2]
    assert pet_list == []
    assert pets_quantity == 0


@pytest.mark.authorized
@pytest.mark.negative_testing
def test_change_not_my_pet():
    """This test check that updating the information in another user's pet account
     is impossible."""
    status = pet.change_not_my_pet()
    assert status != 200


@pytest.mark.authorized
@pytest.mark.negative_testing
def test_delete_not_my_pet():
    """This test check that deletion another user's pet account
         is impossible."""
    status = pet.delete_not_my_pet()
    assert status != 200


@pytest.mark.invalid_authorized
@pytest.mark.negative_testing
def test_can_work_expired_token():
    """This test check that using the expired token
             is impossible."""
    status = pet.expired_token()
    assert status == 401    # Error: Unauthorized


@pytest.mark.not_authorized
@pytest.mark.positive_testing
def test_get_information_about_pet():
    """This test check that getting the information about the pet
    without authorization is possible."""
    status = pet.get_pet_id_without_authorization()
    assert status == 200


@pytest.mark.not_authorized
@pytest.mark.negative_testing
def test_check_putting_a_like():
    """This test check that putting a like to the pet
    without authorization is impossible."""
    status = pet.put_pet_like_without_authorization()
    assert status != 200

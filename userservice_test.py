import unittest
import userservice
import json

class UserServiceTest(unittest.TestCase):
    def test_validate_json(self):
        """
        Test JSON correctness
        """
        json_string = {'userName': 'user11', 'age': 10, 'name': 'name3', 'surname': 'surname3'}
        result = userservice.validate_json(json_string)
        self.assertEqual(result , "ok" )

    def test_validate_json_wrong_username(self):
        """
        Test JSON correctness with misspelled username
        """
        json_string = {'useName': 'user11', 'age': 10, 'name': 'name3', 'surname': 'surname3'}
        result = userservice.validate_json(json_string)
        self.assertEqual(result, "userName in json file")

    def test_validate_json_missing_username(self):
        """
        Test JSON correctness with misspelled username
        """
        json_string = { 'age': 10, 'name': 'name3', 'surname': 'surname3'}
        result = userservice.validate_json(json_string)
        self.assertEqual(result, "userName in json file")

    def test_validate_json_wrong_name(self):
        """
        Test JSON correctness with misspelled name
        """
        json_string = {'userName': 'user11', 'age': 10, 'nae': 'name3', 'surname': 'surname3'}
        result = userservice.validate_json(json_string)
        self.assertEqual(result, "name in json file")

    def test_validate_json_missing_name(self):
        """
        Test JSON correctness with misspelled name
        """
        json_string = {'userName': 'user11', 'age': 10, 'surname': 'surname3'}
        result = userservice.validate_json(json_string)
        self.assertEqual(result, "name in json file")

    def test_validate_json_wrong_surname(self):
        """
        Test JSON correctness with misspelled surname
        """
        json_string = {'userName': 'user11', 'age': 10, 'name': 'name3', 'suname': 'surname3'}
        result = userservice.validate_json(json_string)
        self.assertEqual(result, "surname in json file")

    def test_validate_json_wrong_age(self):
        """
        Test JSON correctness with misspelled age
        """
        json_string = {'userName': 'user11', 'ae': 10, 'name': 'name3', 'surname': 'surname3'}
        result = userservice.validate_json(json_string)
        self.assertEqual(result, "age in json file")

    def test_validate_json_negative_age(self):
        """
        Test JSON correctness with misspelled age
        """
        json_string = {'userName': 'user11', 'age': -1, 'name': 'name3', 'surname': 'surname3'}
        result = userservice.validate_json(json_string)
        self.assertEqual(result, "incorrect age")

    def test_insert_user(self):
        """
        Test insert user
        """
        json_string = {'userName': 'user11', 'age': 10, 'name': 'name3', 'surname': 'surname3'}
        result = userservice.insertUser(json_string)
        equals_to = '{ "code" : 1, "defalutMessage" : "user has been inserted", ' \
                      + str(json_string) + ' }'

        self.assertEqual(result, json.dumps(equals_to))

    def test_insert_user_wrong_username(self):
        """
        Test insert user with misspelled username
        """
        json_string = {'userame': 'user1', 'age': 10, 'name': 'name3', 'surname': 'surname3'}
        result = userservice.insertUser(json_string)
        equals_to = '{ \"code\" : -2, \"defalutMessage\" : userName in json file}'

        self.assertEqual(result, json.dumps(equals_to))

    def test_get_user_details(self):
        """
        Test get user
        """
        json_string = {'userName': 'user1', 'age': 10, 'name': 'name3', 'surname': 'surname3'}
        userservice.insertUser(json_string)
        user = 'user1'
        result = userservice.getUserDetails(user)
        equals_to = "{'userName': 'user1', 'age': 10, 'name': 'name3', 'surname': 'surname3'}"
        print(json.loads(result))
        self.assertTrue(equals_to in json.loads(result))

    def test_get_user_details_not_present(self):
        """
        Test get user
        """
        user = "use"
        result = userservice.getUserDetails(user)
        equals_to = '{ \"code\" : -1, \"defalutMessage\" : Failed find: no matching}'
        self.assertEqual(result, json.dumps(equals_to))



if __name__ == '__main__':
    unittest.main()
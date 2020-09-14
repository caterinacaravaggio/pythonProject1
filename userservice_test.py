import unittest
from flask import json, request, jsonify

import userservice



class UserServiceTest(unittest.TestCase):
    def test_validate_json(self):
        """
        Test JSON correctness
        """
        json_string = {'userName': 'user11', 'age': 10, 'name': 'name3', 'surname': 'surname3'}
        result = userservice.validate_json(json_string)
        self.assertEqual(result , "user has been saved" )

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

    def test_validate_json_void_name(self):
        """
        Test JSON correctness with misspelled name
        """
        json_string = {'userName': 'user11', 'age': 10, 'name' : '', 'surname': 'surname3'}
        result = userservice.validate_json(json_string)
        self.assertEqual(result, "void field name")

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
        with userservice.app.test_client() as c:
            rv = c.post('/userService/insertUser', json={
                'userName': 'user11',
                'age': 10,
                'name': 'name3',
                'surname': 'surname3'
            })
            json_data = rv.get_json()
            self.assertEqual(json_data, {
                'code' : 1,
                'defaultMessage' : 'user has been saved',
                'userName': 'user11',
                'age': 10,
                'name': 'name3',
                'surname': 'surname3'
            })

    def test_insert_user_wrong_username(self):
        """
        Test insert user with misspelled username
        """
        with userservice.app.test_client() as c:
            rv = c.post('/userService/insertUser', json={
                'userNam': 'user11',
                'age': 10,
                'name': 'name3',
                'surname': 'surname3'
            })
            json_data = rv.get_json()
            self.assertEqual(json_data, {
                'code': -2,
                'defaultMessage': 'userName in json file'
            })

    def test_get_user_details(self):
        """
        Test get user
        """
        with userservice.app.test_client() as c:
            rv = c.get('/userService/getUser?userName=user11')
            json_data = rv.get_json()
            print(str(json_data))
            self.assertTrue(
                "'code': 1, 'defaultMessage': 'user has been found'" in str(json_data))

    def test_get_user_details_not_present(self):
        """
        Test get user
        """
        with userservice.app.test_client() as c:
            rv = c.get('/userService/getUser?userName=userNotPresent')
            json_data = rv.get_json()
            self.assertEqual(json_data, {
                'code': -1,
                'defaultMessage': 'Failed find: no matching'
            })



if __name__ == '__main__':
    unittest.main()
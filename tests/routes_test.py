import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.routes import user_bp, user_repo

class UserRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(user_bp)
        self.client = self.app.test_client()

    @patch.object(user_repo, 'add')
    @patch('app.models.User')
    def test_create_user_success(self, MockUser, mock_add):
        mock_add.return_value = 1
        MockUser.validate_name.return_value = None
        response = self.client.post('/users', json={'name': 'Lucas'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {'id': 1, 'name': 'Lucas'})

    @patch('app.models.User')
    def test_create_user_invalid_json(self, MockUser):
        response = self.client.post('/users', data='notjson', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    @patch('app.models.User')
    def test_create_user_invalid_name(self, MockUser):
        MockUser.validate_name.return_value = "Nome inválido"
        response = self.client.post('/users', json={'name': ''})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    @patch.object(user_repo, 'add')
    @patch('app.models.User')
    def test_create_user_internal_error(self, MockUser, mock_add):
        mock_add.side_effect = Exception("DB error")
        MockUser.validate_name.return_value = None
        response = self.client.post('/users', json={'name': 'Lucas'})
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.get_json())

    @patch.object(user_repo, 'get_all')
    def test_get_users_success(self, mock_get_all):
        user_mock = MagicMock()
        user_mock.to_dict.return_value = {'id': 1, 'name': 'Lucas'}
        mock_get_all.return_value = [user_mock]
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [{'id': 1, 'name': 'Lucas'}])

    @patch.object(user_repo, 'get_all')
    def test_get_users_internal_error(self, mock_get_all):
        mock_get_all.side_effect = Exception("DB error")
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.get_json())

    @patch.object(user_repo, 'get_by_id')
    def test_get_user_success(self, mock_get_by_id):
        user_mock = MagicMock()
        user_mock.to_dict.return_value = {'id': 1, 'name': 'Lucas'}
        mock_get_by_id.return_value = user_mock
        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'id': 1, 'name': 'Lucas'})

    @patch.object(user_repo, 'get_by_id')
    def test_get_user_not_found(self, mock_get_by_id):
        mock_get_by_id.return_value = None
        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())

    @patch.object(user_repo, 'get_by_id')
    def test_get_user_internal_error(self, mock_get_by_id):
        mock_get_by_id.side_effect = Exception("DB error")
        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.get_json())

    @patch.object(user_repo, 'get_by_id')
    @patch.object(user_repo, 'update')
    @patch('app.models.User')
    def test_update_user_success(self, MockUser, mock_update, mock_get_by_id):
        MockUser.validate_name.return_value = None
        user_mock = MagicMock()
        user_mock.to_dict.return_value = {'id': 1, 'name': 'Lucas'}
        mock_get_by_id.side_effect = [user_mock, user_mock]
        response = self.client.put('/users/1', json={'name': 'Lucas'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'id': 1, 'name': 'Lucas'})

    @patch('app.models.User')
    def test_update_user_invalid_json(self, MockUser):
        response = self.client.put('/users/1', data='notjson', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    @patch('app.models.User')
    def test_update_user_invalid_name(self, MockUser):
        MockUser.validate_name.return_value = "Nome inválido"
        response = self.client.put('/users/1', json={'name': ''})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    @patch.object(user_repo, 'get_by_id')
    @patch.object(user_repo, 'update')
    @patch('app.models.User')
    def test_update_user_not_found(self, MockUser, mock_update, mock_get_by_id):
        MockUser.validate_name.return_value = None
        mock_get_by_id.return_value = None
        response = self.client.put('/users/1', json={'name': 'Lucas'})
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())

    @patch.object(user_repo, 'get_by_id')
    @patch.object(user_repo, 'update')
    @patch('app.models.User')
    def test_update_user_internal_error(self, MockUser, mock_update, mock_get_by_id):
        MockUser.validate_name.return_value = None
        mock_get_by_id.side_effect = Exception("DB error")
        response = self.client.put('/users/1', json={'name': 'Lucas'})
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.get_json())

    @patch.object(user_repo, 'get_by_id')
    @patch.object(user_repo, 'delete')
    def test_delete_user_success(self, mock_delete, mock_get_by_id):
        user_mock = MagicMock()
        user_mock.name = 'Lucas'
        mock_get_by_id.return_value = user_mock
        response = self.client.delete('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Usuário Lucas deletado com sucesso.', response.get_json().get('message', ''))

    @patch.object(user_repo, 'get_by_id')
    @patch.object(user_repo, 'delete')
    def test_delete_user_not_found(self, mock_delete, mock_get_by_id):
        mock_get_by_id.return_value = None
        response = self.client.delete('/users/1')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())

    @patch.object(user_repo, 'get_by_id')
    @patch.object(user_repo, 'delete')
    def test_delete_user_internal_error(self, mock_delete, mock_get_by_id):
        mock_get_by_id.side_effect = Exception("DB error")
        response = self.client.delete('/users/1')
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.get_json())
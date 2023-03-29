class AuthActions(object):
    """
    Helper class for authentication in testing
    """

    def __init__(self, client):
        self._client = client

    def register(self, username='test', email='test@test.com', password='test'):
        return self._client.post(
            '/api/auth/register',
            content_type='application/json',
            json={
                'username': username,
                'email': email,
                'password': password
            })

    def login(self, username='test', password='test'):
        return self._client.post(
            '/api/auth/login',
            content_type='application/json',
            json={
                'username': username,
                'password': password
            })

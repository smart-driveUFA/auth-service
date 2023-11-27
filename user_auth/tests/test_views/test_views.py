# from datetime import datetime, timedelta
# from rest_framework.test import APITestCase
# from rest_framework import status
# from django.urls import reverse
# from user_auth.factories import UserFactory
# from core.models import ApiKey
#
#
# class VerifyTokenTest(APITestCase):
#     def setUp(self):
#         self.user = UserFactory()
#         self.api_key = ApiKey.objects.create(
#             user=self.user, expired_at=datetime.utcnow().date() + timedelta(days=30)
#         )
#         self.valid_token = self.api_key.jwt_token
#
#     def test_verify_token_success(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.valid_token}")
#         url = reverse("user_auth:verify_token")
#         response = self.client.post(url)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_verify_token_failure(self):
#         invalid_token = "Bearer invalid_token"
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {invalid_token}")
#
#         url = reverse("user_auth:verify_token")
#         response = self.client.post(url)
#
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

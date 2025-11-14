#!/usr/bin/env python3
"""Unit tests for client module"""
import sys
import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized

# Mock utils module before importing client
sys.modules['utils'] = MagicMock()
from client import GithubOrgClient  # noqa: E402


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        test_payload = {"payload": True}
        mock_get_json.return_value = test_payload
        test_client = GithubOrgClient(org_name)
        result = test_client.org()

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the expected value"""
        test_payload = {"repos_url": "https://api.github.com/orgs/test/repos"}
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock,
                   return_value=test_payload):
            test_client = GithubOrgClient("test")
            result = test_client._public_repos_url

            self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repos"""
        test_repos_url = "https://api.github.com/orgs/test/repos"
        test_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        mock_get_json.return_value = test_repos_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock,
                   return_value=test_repos_url) as mock_public_repos_url:
            test_client = GithubOrgClient("test")
            result = test_client.public_repos()

            expected_repos = [repo["name"] for repo in test_repos_payload]
            self.assertEqual(result, expected_repos)
            mock_get_json.assert_called_once_with(test_repos_url)
            mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns the expected value"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

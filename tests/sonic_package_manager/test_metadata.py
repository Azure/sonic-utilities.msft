#!/usr/bin/env python

import json
import contextlib
from unittest.mock import Mock, MagicMock

import pytest

from sonic_package_manager.database import PackageEntry
from sonic_package_manager.errors import MetadataError
from sonic_package_manager.manifest import Manifest
from sonic_package_manager.metadata import MetadataResolver
from sonic_package_manager.version import Version


@pytest.fixture
def manifest_str():
    return json.dumps({
        'package': {
            'name': 'test',
            'version': '1.0.0',
        },
        'service': {
            'name': 'test',
            'asic-service': False,
            'host-service': True,
        },
        'container': {
            'privileged': True,
        },
    })


def test_metadata_resolver_local(mock_registry_resolver, mock_docker_api):
    metadata_resolver = MetadataResolver(mock_docker_api, mock_registry_resolver)
    # it raises exception because mock manifest is not a valid manifest
    # but this is not a test objective, so just suppress the error.
    with contextlib.suppress(MetadataError):
        metadata_resolver.from_local('image')
    mock_docker_api.labels.assert_called_once()


def test_metadata_resolver_remote(mock_registry_resolver, mock_docker_api):
    metadata_resolver = MetadataResolver(mock_docker_api, mock_registry_resolver)
    mock_registry = MagicMock()
    mock_registry.manifest = MagicMock(return_value={'config': {'digest': 'some-digest'}})

    def return_mock_registry(repository):
        return mock_registry

    mock_registry_resolver.get_registry_for = Mock(side_effect=return_mock_registry)
    # it raises exception because mock manifest is not a valid manifest
    # but this is not a test objective, so just suppress the error.
    with contextlib.suppress(MetadataError):
        metadata_resolver.from_registry('test-repository', '1.2.0')
    mock_registry_resolver.get_registry_for.assert_called_once_with('test-repository')
    mock_registry.manifest.assert_called_once_with('test-repository', '1.2.0')
    mock_registry.blobs.assert_called_once_with('test-repository', 'some-digest')
    mock_docker_api.labels.assert_not_called()


def test_metadata_construction(manifest_str):
    metadata = MetadataResolver.from_labels({
        'com': {
            'azure': {
                'sonic': {
                    'manifest': manifest_str,
                    'yang-module': 'TEST'
                }
            }
        }
    })
    assert metadata.yang_modules == ['TEST']

    metadata = MetadataResolver.from_labels({
        'com': {
            'azure': {
                'sonic': {
                    'manifest': manifest_str,
                    'yang-module': {
                        'sonic-test': 'TEST',
                        'sonic-test-2': 'TEST 2',
                    },
                },
            },
        },
    })
    assert metadata.yang_modules == ['TEST', 'TEST 2']


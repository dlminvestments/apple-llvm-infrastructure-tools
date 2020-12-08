"""
  Tests for the tracked branch ref (used by git apple-llvm pr).
"""

import pytest
from git_apple_llvm.git_tools import git
from git_apple_llvm.git_tools.tracked_branch_ref import TrackedBranchRef, get_tracked_branch_ref
from typing import Optional


@pytest.fixture(scope='function',
                params=['origin/',
                        ''])
def optional_remote_prefix(request) -> str:
    return request.param


def test_get_tracked_branch_ref(cd_to_monorepo_clone, monorepo_test_fixture, optional_remote_prefix: str):
    ref: Optional[TrackedBranchRef] = get_tracked_branch_ref(optional_remote_prefix + 'internal/master')
    if ref is None:
        raise AssertionError
    if ref.remote_name != 'origin':
        raise AssertionError
    if ref.remote_url != monorepo_test_fixture.path:
        raise AssertionError
    if ref.branch_name != 'internal/master':
        raise AssertionError
    if ref.head_hash is None:
        raise AssertionError


def test_different_tracked_branch_ref(cd_to_monorepo_clone, monorepo_test_fixture, optional_remote_prefix: str):
    branch_name = 'test-tracked-branch'
    git('branch', '-D', branch_name, ignore_error=True)
    git('checkout', '-b', branch_name)
    git('branch', '-u', 'origin/internal/master', branch_name)
    ref: Optional[TrackedBranchRef] = get_tracked_branch_ref(optional_remote_prefix + branch_name)
    if len(optional_remote_prefix) > 0:
        # The ref doesn't exist on the remote
        if ref is not None:
            raise AssertionError
        return
    if ref is None:
        raise AssertionError
    if ref.remote_name != 'origin':
        raise AssertionError
    if ref.remote_url != monorepo_test_fixture.path:
        raise AssertionError
    if ref.branch_name != 'internal/master':
        raise AssertionError


def test_get_no_tracked_branch_ref(cd_to_monorepo_clone, optional_remote_prefix: str):
    ref: Optional[TrackedBranchRef] = get_tracked_branch_ref(optional_remote_prefix + 'foo')
    if ref is not None:
        raise AssertionError

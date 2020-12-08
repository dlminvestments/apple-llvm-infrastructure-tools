"""
  Tests for the monorepo test harness that is used by other tests.
"""

from pathlib import PosixPath
from git_apple_llvm.git_tools import git, git_output


def test_monorepo_simple_test_harness(cd_to_monorepo):
    internal_commits = git_output('rev-list', 'internal/master').splitlines()
    if len(internal_commits) != 16:
        raise AssertionError
    trailers = git_output('show', '--format=%B', internal_commits[0])
    if 'apple-llvm-split-commit:' not in trailers:
        raise AssertionError
    if 'apple-llvm-split-dir: -/' not in trailers:
        raise AssertionError

    if not PosixPath('clang/dir/file2').is_file():
        raise AssertionError

    upstream_commits = git_output('rev-list', 'llvm/master').splitlines()
    if len(upstream_commits) != 9:
        raise AssertionError
    if internal_commits[-1] != upstream_commits[-1]:
        raise AssertionError
    # Verify that each upstream commit is in downstream.
    for commit in upstream_commits:
        git('merge-base', '--is-ancestor', commit, 'internal/master')

    internal_clang_commits = git_output('rev-list', 'split/clang/internal/master').splitlines()
    if len(internal_clang_commits) != 7:
        raise AssertionError

    upstream_clang_commits = git_output('rev-list', 'split/clang/upstream/master').splitlines()
    if len(upstream_clang_commits) != 4:
        raise AssertionError

"""
  Tests for the git tools.
"""

import os
import pytest
from git_apple_llvm.git_tools import git, git_output, get_current_checkout_directory, commit_exists, GitError
from git_apple_llvm.git_tools import read_file_or_none


def test_git_invocation(tmp_path):
    """ Tests for the git/git_output functions. """
    repo_path = tmp_path / 'repo'
    repo_path.mkdir()
    if not repo_path.is_dir():
        raise AssertionError
    repo_dir = str(repo_path)

    git('init', git_dir=repo_dir)

    (repo_path / 'initial').write_text(u'initial')
    git('add', 'initial', git_dir=repo_dir)

    # Check that we can report an error on failure.
    with pytest.raises(GitError) as err:
        git('add', 'foo', git_dir=repo_dir)
    if not err.value.stderr.startswith('fatal'):
        raise AssertionError
    if not repr(err.value).startswith('GitError'):
        raise AssertionError

    # Check that errors can be ignored.
    git('add', 'foo', git_dir=repo_dir, ignore_error=True)

    output = git_output('commit', '-m', 'initial', git_dir=repo_dir)
    if len(output) <= 0:
        raise AssertionError

    # Ensure that the output is stripped.
    output = git_output('rev-list', 'HEAD', git_dir=repo_dir)
    if '\n' in output:
        raise AssertionError
    output = git_output('rev-list', 'HEAD', git_dir=repo_dir, strip=False)
    if '\n' not in output:
        raise AssertionError

    # Ensure that commit exists works only for commit hashes.
    hash = output.strip()
    if not commit_exists(hash):
        raise AssertionError
    if commit_exists('HEAD'):
        raise AssertionError
    if commit_exists(hash + 'abc'):
        raise AssertionError
    if commit_exists('000000'):
        raise AssertionError

    # Ensure that we can get the directory of the checkout even when the
    # working directory is a subdirectory.
    os.chdir(repo_dir)
    dir_a = get_current_checkout_directory()
    (repo_path / 'subdir').mkdir()
    cwd = os.getcwd()
    os.chdir(os.path.join(repo_dir, 'subdir'))
    dir_b = get_current_checkout_directory()
    os.chdir(cwd)
    if dir_a != dir_b:
        raise AssertionError

    if read_file_or_none('HEAD', 'initial') != 'initial':
        raise AssertionError
    if read_file_or_none(hash, 'initial') != 'initial':
        raise AssertionError
    if read_file_or_none('HEAD', 'path/does-not-exist') is not None:
        raise AssertionError
    if read_file_or_none('foo', 'initial') is not None:
        raise AssertionError

"""
  Tests for the zippered merge algorithm.
"""

from git_apple_llvm.am.zippered_merge import BranchIterator, compute_zippered_merge_commits
from typing import Dict


def br(commits, merge_bases, initial_merge_base) -> BranchIterator:
    commit_to_merge_base: Dict[str, str] = {}
    for i in range(0, len(commits)):
        commit_to_merge_base[commits[i]] = merge_bases[i]
    return BranchIterator(commits, lambda commit: commit_to_merge_base[commit], initial_merge_base)


def test_zippered_merge_alg_no_zipper():
    if compute_zippered_merge_commits(br([], [], 'm/A'),
                                          br([], [], 'm/A')) != []:
        raise AssertionError

    # Allow direct merges when merge bases match.
    if compute_zippered_merge_commits(br(['l/A'], ['m/A'], 'm/A'),
                                          br([], [], 'm/A')) != [['l/A']]:
        raise AssertionError

    if compute_zippered_merge_commits(br([], [], 'm/A'),
                                          br(['r/A'], ['m/A'], 'm/A')) != [['r/A']]:
        raise AssertionError

    if compute_zippered_merge_commits(br(['l/A'], ['m/A'], 'm/A'),
                                          br(['r/A'], ['m/A'], 'm/A')) != [['l/A'], ['r/A']]:
        raise AssertionError

    # Mismatching merge bases don't allow direct merges.
    if compute_zippered_merge_commits(br(['l/A'], ['m/A'], 'm/A'),
                                          br([], [], 'm/B')) != []:
        raise AssertionError

    if compute_zippered_merge_commits(br([], [], 'm/B'),
                                          br(['r/A'], ['m/A'], 'm/A')) != []:
        raise AssertionError

    if compute_zippered_merge_commits(br(['l/A', 'l/B'], ['m/A', 'm/B'], 'm/A'),
                                          br(['r/A'], ['m/A'], 'm/A')) != [['l/A'], ['r/A']]:
        raise AssertionError

    if compute_zippered_merge_commits(br(['l/A'], ['m/A'], 'm/A'),
                                          br(['r/A', 'r/B'], ['m/A', 'm/B'], 'm/A')) != [['l/A'], ['r/A']]:
        raise AssertionError


def test_zippered_merge_alg():
    if compute_zippered_merge_commits(br(['l/A'], ['m/B'], 'm/A'),
                                          br(['r/A'], ['m/B'], 'm/A')) != [['l/A', 'r/A']]:
        raise AssertionError
    if compute_zippered_merge_commits(br(['l/A', 'l/B'], ['m/A', 'm/B'], 'm/A'),
                                          br(['r/A'], ['m/B'], 'm/B')) != [['l/B', 'r/A']]:
        raise AssertionError
    if compute_zippered_merge_commits(br(['l/A'], ['m/B'], 'm/B'),
                                          br(['r/A', 'r/B'], ['m/A', 'm/B'], 'm/A')) != [['l/A', 'r/B']]:
        raise AssertionError

    if compute_zippered_merge_commits(br(['l/A', 'l/B'], ['m/B', 'm/C'], 'm/A'),
                                          br(['r/A', 'r/B'], ['m/B', 'm/C'], 'm/A')) != [['l/A', 'r/A'], ['l/B', 'r/B']]:
        raise AssertionError
    if compute_zippered_merge_commits(br(['l/A', 'l/B'], ['m/B1', 'm/C'], 'm/A'),
                                          br(['r/A', 'r/B'], ['m/B2', 'm/C'], 'm/A')) != [['l/B', 'r/B']]:
        raise AssertionError

    # Zippered + direct.
    if compute_zippered_merge_commits(br(['l/A', 'l/B'], ['m/B', 'm/B'], 'm/A'),
                                          br(['r/A', 'r/B'], ['m/B', 'm/B'], 'm/A')) != [['l/A', 'r/A'],
                                                                                         ['l/B'], ['r/B']]:
        raise AssertionError
    if compute_zippered_merge_commits(br(['l/A', 'l/B'], ['m/B', 'm/B'], 'm/A'),
                                          br(['r/A', 'r/B'], ['m/B', 'm/C'], 'm/A')) != [['l/A', 'r/A'], ['l/B']]:
        raise AssertionError
    if compute_zippered_merge_commits(br(['l/A', 'l/B'], ['m/B', 'm/C'], 'm/A'),
                                          br(['r/A', 'r/B'], ['m/B', 'm/B'], 'm/A')) != [['l/A', 'r/A'], ['r/B']]:
        raise AssertionError

    # Direct + zippered.
    if compute_zippered_merge_commits(br(['l/A', 'l/B'], ['m/A', 'm/B'], 'm/A'),
                                          br(['r/B'], ['m/B'], 'm/A')) != [['l/A'], ['l/B', 'r/B']]:
        raise AssertionError
    if compute_zippered_merge_commits(br(['l/B'], ['m/B'], 'm/A'),
                                          br(['r/A', 'r/B'], ['m/A', 'm/B'], 'm/A')) != [['r/A'], ['l/B', 'r/B']]:
        raise AssertionError

"""Git snapshot / rollback / diff, exposed as agent tools.

These operate on the *writable copy* of a repo that the migration works on —
never on the operator's own checkout. `snapshot` before each EDIT batch is what
makes a bad batch revertible (NFR-9); `diff` produces the unified `.patch`
deliverable (FR-10).
"""

from __future__ import annotations

from pathlib import Path

from git import Repo

#: Identity for snapshot commits. The sandbox user has no git config of its own,
#: so committing would fail without this.
ACTOR_NAME = "mra-agent"
ACTOR_EMAIL = "mra-agent@localhost"


def _repo(path: Path | str) -> Repo:
    """Open ``path`` as a git repo, initializing it if it is not one yet."""
    path = Path(path)
    try:
        return Repo(path)
    except Exception:
        repo = Repo.init(path)
        with repo.config_writer() as config:
            config.set_value("user", "name", ACTOR_NAME)
            config.set_value("user", "email", ACTOR_EMAIL)
        return repo


def snapshot(repo_path: Path | str, message: str = "mra snapshot") -> str:
    """Commit the whole working tree and return the new commit SHA.

    Allows an empty commit so that "snapshot before every batch" always yields a
    SHA to roll back to, even when a batch changed nothing.
    """
    repo = _repo(repo_path)
    repo.git.add("-A")
    repo.git.commit("-m", message, "--allow-empty",
                    f"--author={ACTOR_NAME} <{ACTOR_EMAIL}>")
    return repo.head.commit.hexsha


def rollback(repo_path: Path | str, sha: str) -> str:
    """Hard-reset the tree to ``sha`` and drop untracked files; return the SHA."""
    repo = _repo(repo_path)
    repo.git.reset("--hard", sha)
    repo.git.clean("-fd")
    return repo.head.commit.hexsha


def diff(repo_path: Path | str, against: str = "HEAD") -> str:
    """Return a unified diff of the working tree against ``against``.

    Includes untracked files (``--no-index`` cannot, but ``add -N`` can), so a
    newly created module shows up in the patch deliverable.
    """
    repo = _repo(repo_path)
    repo.git.add("-AN")
    patch = repo.git.diff(against)
    # GitPython strips the trailing newline, which `git apply` rejects as a
    # corrupt patch. An empty diff stays empty.
    return f"{patch}\n" if patch else patch

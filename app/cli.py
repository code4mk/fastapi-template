"""CLI commands for the FastAPI template project."""

import subprocess
import sys
from pathlib import Path

# Constants
MIN_ARGS_REQUIRED = 2


def make_revision() -> None:
    """Create a new Alembic migration revision."""
    if len(sys.argv) < MIN_ARGS_REQUIRED:
        print("ERROR: migration message required")  # noqa: T201
        print('Usage: make-revision "add users table"')  # noqa: T201
        sys.exit(1)

    message = sys.argv[1]
    project_root = Path(__file__).parent.parent

    print(f"📦 Creating revision: {message}")  # noqa: T201
    try:
        # Run alembic revision command
        result = subprocess.run(  # noqa: S603
            ["uv", "run", "alembic", "revision", "--autogenerate", "-m", message],  # noqa: S607
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True,
        )
        print(result.stdout)  # noqa: T201
        if result.stderr:
            print(result.stderr, file=sys.stderr)  # noqa: T201
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: Failed to create revision: {e}", file=sys.stderr)  # noqa: T201
        if e.stdout:
            print(e.stdout)  # noqa: T201
        if e.stderr:
            print(e.stderr, file=sys.stderr)  # noqa: T201
        sys.exit(1)
    except FileNotFoundError:
        print("ERROR: 'uv' command not found. Please ensure uv is installed.", file=sys.stderr)  # noqa: T201
        sys.exit(1)


def upgrade() -> None:
    """Upgrade database to the latest migration (head)."""
    project_root = Path(__file__).parent.parent

    print("Upgrading database to head...")  # noqa: T201
    try:
        # Run alembic upgrade head command
        result = subprocess.run(
            ["uv", "run", "alembic", "upgrade", "head"],  # noqa: S607
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True,
        )
        print(result.stdout)  # noqa: T201
        if result.stderr:
            print(result.stderr, file=sys.stderr)  # noqa: T201
        print("Database upgrade completed successfully!")  # noqa: T201
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to upgrade database: {e}", file=sys.stderr)  # noqa: T201
        if e.stdout:
            print(e.stdout)  # noqa: T201
        if e.stderr:
            print(e.stderr, file=sys.stderr)  # noqa: T201
        sys.exit(1)
    except FileNotFoundError:
        print("ERROR: 'uv' command not found. Please ensure uv is installed.", file=sys.stderr)  # noqa: T201
        sys.exit(1)


def lint() -> None:
    """Run pre-commit hooks on all files."""
    project_root = Path(__file__).parent.parent

    print("Running pre-commit on all files...")  # noqa: T201
    try:
        result = subprocess.run(
            ["uv", "run", "pre-commit", "run", "--all-files"],  # noqa: S607
            cwd=project_root,
            check=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        sys.exit(1)
    except FileNotFoundError:
        print("ERROR: 'uv' command not found. Please ensure uv is installed.", file=sys.stderr)  # noqa: T201
        sys.exit(1)


def pre_commit_install() -> None:
    """Install pre-commit hooks into the git repository."""
    project_root = Path(__file__).parent.parent

    print("Installing pre-commit hooks...")  # noqa: T201
    try:
        subprocess.run(
            ["uv", "run", "pre-commit", "install"],  # noqa: S607
            cwd=project_root,
            check=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        sys.exit(1)
    except FileNotFoundError:
        print("ERROR: 'uv' command not found. Please ensure uv is installed.", file=sys.stderr)  # noqa: T201
        sys.exit(1)


if __name__ == "__main__":
    make_revision()

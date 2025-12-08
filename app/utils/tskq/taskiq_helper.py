import importlib
import os
import pkgutil


def discover_and_import_tasks() -> None:
    """Dynamically import all task modules from PROJECT_BASE_PATH/tasks."""
    # Get project base path from environment, default to 'app'
    base_path = os.getenv("PROJECT_BASE_PATH", "app").strip()
    if not base_path:
        base_path = "app"  # Fallback to default

    # Construct project tasks package name
    project_tasks_pkg = f"{base_path}.tasks"

    # Import project tasks package
    try:
        project_pkg = importlib.import_module(project_tasks_pkg)
    except ImportError as e:
        print(f"[WARN] Cannot import project tasks package {project_tasks_pkg}: {e}")  # noqa: T201
        return

    # Recursively import all modules under project tasks
    imported_modules = []
    for module_info in pkgutil.walk_packages(project_pkg.__path__, prefix=f"{project_tasks_pkg}."):
        try:
            importlib.import_module(module_info.name)
            imported_modules.append(module_info.name)
        except ImportError as e:
            print(f"[ERROR] Failed to import task module {module_info.name}: {e}")  # noqa: T201

    # Show summary instead of individual messages
    if imported_modules:
        module_names = [m.split(".")[-1] for m in imported_modules]
        print(  # noqa: T201
            f"Imported {len(imported_modules)} task modules: {', '.join(module_names)}"
        )

import importlib.util
import inspect
import os

def inspect_package(package_name):
    try:
        # Find the package
        spec = importlib.util.find_spec(package_name)
        if spec is None:
            print(f"Package {package_name} not found")
            return

        print(f"Package {package_name} found at: {spec.origin}")

        # Load the package
        package = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(package)

        # Inspect the cli module
        cli_spec = importlib.util.find_spec(f"{package_name}.cli")
        if cli_spec is None:
            print(f"CLI module not found in {package_name}")
            return

        print(f"CLI module found at: {cli_spec.origin}")

        # Load the cli module
        cli = importlib.util.module_from_spec(cli_spec)
        cli_spec.loader.exec_module(cli)

        # List all functions in the cli module
        print("\nFunctions in CLI module:")
        for name, obj in inspect.getmembers(cli, inspect.isfunction):
            print(f"- {name}")

        # Check for the cli group
        if hasattr(cli, 'cli'):
            print("\nCommands in CLI group:")
            for command in cli.cli.commands.values():
                print(f"- {command.name}")
        else:
            print("\nCLI group not found in the module")

    except Exception as e:
        print(f"Error inspecting package: {e}")

inspect_package("llm_client")

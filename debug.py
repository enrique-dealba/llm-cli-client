import sys
import pkg_resources

def main():
    entry_point = pkg_resources.get_entry_info('llm-client', 'console_scripts', 'llm-client')
    if entry_point is None:
        print("Entry point not found")
        return

    print(f"Invoking entry point: {entry_point}")
    cli_function = entry_point.load()
    sys.argv = ['llm-client'] + sys.argv[1:]  # Adjust argv to match expected CLI input
    cli_function()

if __name__ == "__main__":
    main()

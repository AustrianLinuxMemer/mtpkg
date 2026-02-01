import argparse

arg_parser = argparse.ArgumentParser()
subparsers = arg_parser.add_subparsers(dest="command", required=False, help="Command to run")
install_parser = subparsers.add_parser("install", help="Install a package")
install_parser.add_argument("package_name", help="Name of the package to install", nargs="+", type=str)

uninstall_parser = subparsers.add_parser("uninstall", help="Uninstall a package")
uninstall_parser.add_argument("package_name", help="Name of the package to uninstall", nargs="+", type=str)

update_parser = subparsers.add_parser("update", help="Update one, more or all packages")
update_parser.add_argument("package_name", help="Name of the package to update", nargs="*", type=str)

search_parser = subparsers.add_parser("search", help="Search packages")
search_parser.add_argument("query", help="Things to search for", type=str)

arg_parser.add_argument("--detect-engine", help="Detect the engine/protocol version", nargs="?", const=True)
arg_parser.add_argument("--hide-content", help="Hide these types of contents", choices=["mod", "game", "txp"], nargs="+")
arg_parser.add_argument("--ignore_content_flags", help="Ignore these content flags", nargs="+")
arg_parser.add_argument("--config", help="Path to config file", nargs="?")
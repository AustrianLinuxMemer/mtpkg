import os
import sys
from probing import probe_engine
from config import get_config
from args import arg_parser

def main():
    args = arg_parser.parse_args()


    possible_config_files = [
        "/etc/mtpkg/mtpkg.toml",
        os.path.expanduser("~/.mtpkg/mtpkg.toml"),
    ]
    if isinstance(args.config, str):
        possible_config_files.append(os.path.expanduser(args.config))


    config = get_config(possible_config_files)
    if config is None:
        print("None of the config files were valid")
        print(possible_config_files)
        sys.exit(1)


    if args.detect_engine:
        print("Detected engine from: ", probe_engine(cli_path=args.detect_engine if isinstance(args.detect_engine, str) else None, config_path=config["Minetest"].get("engine_location", None) if config else None))
        sys.exit(0)


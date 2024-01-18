import sys
import os
import re
import semver
import logging

logging.basicConfig(filename='bump_version.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_version(text_bloc):
    version_pattern = re.compile(r"version (\d+\.\d+\.\d+|major|minor|patch)")
    matches = version_pattern.findall(text_bloc)
    if matches:
        return matches[-1]
    return None

def compare_versions(current_version, desired_version):
    if desired_version == "major":
        return "major"
    if desired_version == "minor":
        return "minor"
    if desired_version == "patch":
        return "patch"

    current = semver.VersionInfo.parse(current_version)
    desired = semver.VersionInfo.parse(desired_version)

    if desired.major != current.major:
        return "major"
    elif desired.minor != current.minor:
        return "minor"
    else:
        return "patch"

def main(current_version, text_bloc):
    desired_version = parse_version(text_bloc)
    if desired_version is None:
        desired_version = "patch"

    comparison = compare_versions(current_version, desired_version)
    logging.info(f"Comparison: {comparison}")

    current = semver.VersionInfo.parse(current_version)

    if comparison == "major":
        new_version = current.bump_major()
    elif comparison == "minor":
        new_version = current.bump_minor()
    else:  # patch
        new_version = current.bump_patch()

    logging.info(f"New version: {new_version}")
    print(new_version)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 script.py <current_version> <text_bloc>")
        sys.exit(1)

    current_version = sys.argv[1]
    commit_head_env_var = sys.argv[2]

    # Unfortunately env vars need to be parsed from OS to avoid linebreak
    # issues when exporting to Github env variables.

    if commit_head_env_var not in os.environ:
        print(f"Error: Environment variable '{commit_head_env_var}' not found.")
        sys.exit(1)

    text_bloc = os.environ[commit_head_env_var]
    main(current_version, text_bloc)

#!/usr/bin/env python3

from collections import defaultdict
import json
import subprocess
import click
from pick import pick


def list_accounts():
    cmd = ["op", "account", "list", "--format", "json"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)


def list_vaults(account_user_id):
    cmd = ["op", "vault", "list", "--account", account_user_id, "--format", "json"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)


def list_items_in_vault(account_user_id, vault_name):
    cmd = [
        "op",
        "item",
        "list",
        "--vault",
        vault_name,
        "--account",
        account_user_id,
        "--format",
        "json",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)


def find_duplicates(account, vault_name):
    items = list_items_in_vault(account, vault_name)
    item_dict = defaultdict(list)

    for item in items:
        title = item.get("title")
        updated_at = item.get("updated_at")
        item_id = item.get("id")

        if title is None or updated_at is None or item_id is None:
            continue

        key = (title, updated_at)
        item_dict[key].append(item)

    return {k: v for k, v in item_dict.items() if len(v) > 1}


def select_option(options, prompt):
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    selected_option = None
    while not selected_option:
        option_index = input("Enter the number of the option: ")
        if option_index.isdigit() and 1 <= int(option_index) <= len(options):
            selected_option = options[int(option_index) - 1]
        else:
            print("Invalid option. Please try again.")
    return selected_option


@click.command()
@click.argument("vault_name", required=False)
@click.option(
    "--dry", is_flag=True, help="Dry run: just print the commands that would be run."
)
def main(vault_name, dry):
    doc_string = """
    This program finds and archives duplicates in a given vault.
    Use --dry to print the commands that would be run without executing them.
    Use --help for more information.
    """
    print("\n" + doc_string)
    if not vault_name:
        accounts = list_accounts()
        account_options = [(a["url"], a["email"], a["user_uuid"]) for a in accounts]
        account_url, account_email, account_user_id = select_option(
            account_options, "Select an account:"
        )

        vaults = list_vaults(account_user_id)
        vault_options = [v["name"] for v in vaults]
        vault_name = select_option(vault_options, "Select a vault:")

    duplicates = find_duplicates(account_user_id, vault_name)

    if duplicates:
        print(f"{len(duplicates)} duplicates were found:")
        for key, items in sorted(duplicates.items(), key=lambda x: x[0][0]):
            title, updated_at = key
            print(f"  {title}: {len(items)} duplicates")

        if dry:
            archive_option = input(
                f"This is a dry run. The command to archive these {len(duplicates)} duplicates will be printed but not executed. Continue? (y/N): "
            )
        else:
            archive_option = input(
                f"Would you like to archive these {len(duplicates)} duplicates now? (y/N): "
            )
        if archive_option.lower() == "y":
            for key, items in duplicates.items():
                items_to_archive = items[1:]  # Keep one, archive the rest
                for item in items_to_archive:
                    cmd = [
                        "op",
                        "item",
                        "delete",
                        item.get("id"),
                        "--vault",
                        vault_name,
                        "--archive",
                    ]
                    if dry:
                        print(
                            f"To archive item {item.get('title')}, Would run: `"
                            + " ".join(cmd)
                            + "`"
                        )
                    else:
                        print("Archiving dupe of " + item.get("title"))
                        subprocess.run(cmd, capture_output=True, text=True)
    else:
        print("No duplicate items found.")


if __name__ == "__main__":
    main()

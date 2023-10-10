# 1Password Duplicate Item Archiver

1Password used to have a tool to help you find and remove duplicates, but they removed it. This is a simple script that uses the 1Password CLI to find and archive duplicates.

# Getting started:

0. Clone this repo
1. https://developer.1password.com/docs/cli/get-started/#sign-in
2. `pip install -r requirements.txt`
3. `./dupe_finder.py`

Example:

```
❯ ./dupe_finder.py


    This program finds and archives duplicates in a given vault.
    Use --dry to print the commands that would be run without executing them.
    Use --help for more information.

Select an account:
1. ('my.1password.com', '<my-email@my-domain.com>', 'LONGIDHERE')
2. ('another.domain.com', 'another-email@another-domain.com', 'ANOTHER_LONG_ID')
Enter the number of the option: 1
Select a vault:
1. Private
2. 1Password
3. Shared
Enter the number of the option: 1
2 duplicates were found:
  Name of item: 2 duplicates
  Another item: 2 duplicates
Would you like to archive these 220 duplicates now? (y/N): y
Archiving dupe of Name of item
Archiving dupe of Another item
```

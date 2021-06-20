import os
import re
import sys

valid_branch_regex = r"^(feature|bugfix|improvement|hotfix)\/\d+-[a-z0-9._-]+$"

invalid_branch_name_msg = f"""
There is something wrong with your branch name. Branch names in this project must adhere to this contract: 
{valid_branch_regex}. Your commit will be rejected. 
You should rename your branch to a valid name and try again.
Branch name examples:
<feature|improvement|bugfix|hotfix>/<issue-id>-<issue-desc>
feature/1-description
bugfix/1-description
"""


def main():
    branch_name = os.popen('git rev-parse --abbrev-ref HEAD').read()
    if bool(re.match(valid_branch_regex, branch_name)):
        return 0
    sys.stdout.write(invalid_branch_name_msg)
    return 1


if __name__ == '__main__':
    exit(main())

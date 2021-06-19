#!/bin/sh

# To enable this hook, rename this file to "pre-commit".

###############################################################################
# https://gist.github.com/stuntgoat/8800170
# Git pre-commit hook for finding and warning about Python print
# statements.
#

# Set this to 0 to turn off testing.
TESTING=1

# Get the current git HEAD
head=`git rev-parse --verify HEAD`

# BSD regex for finding Python print statements
find_print='\+[[:space:]]*print[[:space:](]*'

# Save output to $out var
out=`git diff ${head} | grep -e ${find_print}`

# Count number of prints
count=`echo "${out}" | grep -e '\w' | wc -l`
if [ $count -gt 0 ];
   then
    echo
    echo "###############################################################################"
    echo "$out"

    echo "###############################################################################"
    echo "       " ${count} "print statement(s) found in commit!"
    echo
    # echo "  Abort : <enter>"
    # echo "  Commit: commit <enter>"
    # echo
    # echo ">>> \c"

    # ## Get stdin from a keyboard:
    # ## http://stackoverflow.com/a/10015707
    # exec < /dev/tty

    # # Let user type option.
    # read command

    # ## Close stdin.
    # exec <&-

    # # Lower input received
    # lowered=`echo ${command} | tr '[:upper:]' '[:lower:]'`

    # if [ "$command" = "commit" ];
    #     then
    #     echo "committing print statement(s)"
    #     exit $TESTING
    # fi
    # echo "aborting"
    exit 1
fi


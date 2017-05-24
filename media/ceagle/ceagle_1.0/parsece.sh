#!/bin/bash

# paste <(cat "$1" | grep '^  [^ ]' | cut -d ' ' -f 4) <(cat "$1" | grep '^    ' | cut -b 5- | rev | cut -b 2- | rev) 

cat $1 | while read l ; do
    if [ "${l}" = "(model" ] || [ "${l}" = ")" ] ; then
        printf "\n"
    fi
    if [[ "${l}" =~ ^\(define-fun ]] ; then
        printf "\n"
        printf "%s\t" "$(printf "%s" "${l}" | cut -d ' ' -f 2)"
    else
        printf "%s " "${l}"
    fi
done | tail -n +3 | head -n -1 | rev | cut -b 3- | rev

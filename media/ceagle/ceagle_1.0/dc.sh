#!/bin/bash
# DW: normally you use dc.sh after ceagle.sh reports a failure

export PATH=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ):$PATH
echo "Current PATH is $PATH"

for filename in "$@" ; do

    if [[ "$filename" == *.c ]] ; then
        base="${filename}"
        #base="$( dirname "${filename}" )/${filename}"
    elif [[ "$filename" == *.i ]] ; then 
        base="${filename}"
        #base="$( dirname "${filename}" )/${filename}"
    else
        printf "%s\t%s\t%s\n" "${filename}" "UNKNOWN" "UNKNOWN_FILE_TYPE"
        continue
    fi

    clang -g -O0 -S -emit-llvm "$filename" -o "${base}.ll"
    
    svie -v svcore "${base}.ll"
done
#done 2>/dev/null

# DW: if you wanna see columne 3 the fail reason, comment out "| cut -f 1-2"
# DW: or use the one below

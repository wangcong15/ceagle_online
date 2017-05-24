#!/bin/bash

if [ "$1" = "--version" ] ; then
    printf "1.0\n"
    exit
fi

#echo $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export PATH=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ):$PATH
#echo $PATH

for filename in "$@" ; do
    begin=$( date +%s )
    
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

    #printf "base[%s], filename[%s]\n" "${base}" "${filename}"

    clang -g -O0 -S -emit-llvm "$filename" -o "${base}.ll" >/dev/null 2>&1
    if [ "$?" -ne 0 ] ; then
        printf "%s\t%s\t%s\n" "${filename}" "UNKNOWN" "CLANG_FAILURE"
        continue
    fi
    if ! [ -f "${base}.ll" ] ; then
        printf "%s\t%s\t%s\n" "${filename}" "UNKNOWN" "CLANG_NO_LL"
        continue
    fi
    
    svie -v svcore "${base}.ll" > "${base}.log" 2>/dev/null
    if [ "$?" -ne 0 ] ; then
        printf "%s\t%s\t%s\n" "${filename}" "UNKNOWN" "IE_FAILURE"
        continue
    fi
    if ! [ -f "${base}.elt" ] ; then
        printf "%s\t\%s\t%s\n" "${filename}" "UNKNOWN" "IE_NO_ELT"
        continue
    fi

    finish=$( date +%s )

    retstr=$( cat "${base}.log" | tail -n 1 )
    if [ "${retstr}" = "TRUE" ] ; then
        printf "%s\t%s\t%ds\n" "${filename}" "TRUE" $(( $finish - $begin ))
    elif [ "${retstr}" = "FALSE" ] ; then
        printf "%s\t%s\t%ds\n" "${filename}" "FALSE" $(( $finish - $begin ))
    elif [ "${retstr}" = "UNKNOWN" ] ; then
        printf "%s\t%s\t%ds\t%s\n" "${filename}" "UNKNOWN" $(( $finish - $begin )) "IS_RET_UNKNOWN"
    else
        printf "%s\t%s\t%ds\t%s\n" "${filename}" "UNKNOWN" $(( $finish - $begin )) "IS_RET_INVALID"
    fi
done 2>/dev/null | cut -f 1-3
#done 2>/dev/null

# DW: if you wanna see columne 3 the fail reason, comment out "| cut -f 1-2"
# DW: or use the one below

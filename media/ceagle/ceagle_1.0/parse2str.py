#!/usr/bin/env python2

import time
import subprocess
import sys
import distutils.spawn

# DW: the main function
def main():
    # DW: this may vary in different systems
    path = distutils.spawn.find_executable("z3")
    if path is None:
        raise Exception("z3 not found")
    #print "Parse script: found z3 in path", path

    # DW: different level of the notion
    str_output_prefix_1 = "Parse script: "
    str_output_prefix_2 = "\t"

    # DW: prepare Z3 binary
    p = subprocess.Popen([path, "-in"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # DW: get .smt2 file name
    if (len(sys.argv) < 4):
        print str_output_prefix_1 + "please specify a file and a string as input"
        sys.exit(0)
    vtype = str(sys.argv[1])
    filename = str(sys.argv[2])
    value = str(sys.argv[3])

    # DW: first input module smt from "; DW: begin" to "; DW: end"
    if vtype == "fp":
        command = "(set-option :pp.decimal true)\n(declare-const from (_ FloatingPoint 8 24))\n(declare-const to Real)\n(assert (= from " + value + "))\n(assert (= to (fp.to_real from)))\n(check-sat)\n"
        #print command
    elif vtype == "fr":
        command = "(set-option :pp.decimal true)\n(declare-const to Real)\n(assert (= to " + value + "))\n(check-sat)\n"
        #print command
    else:
        print str_output_prefix_1 + "unkown type"
        return

    p.stdin.write(command)
    p.stdin.flush()

    # DW: create a file to write verification result
    f = open(filename, "w")

    # DW: get the output of Z3
    output = p.stdout.readline().strip()
    #print str_output_prefix_2 + output

    if output == "unsat":
        print str_output_prefix_1 + "error z3 unsat"
    elif output == "sat":
        # DW: get the value
        strcmd = "(get-value (to))\n"
        p.stdin.write(strcmd)
        p.stdin.flush()

        # DW: print to stdout and file
        output = p.stdout.readline().strip()
        #print value + " -> " + output

        # DW: possibly ((to 0.75)), ((to (- 0.75)))
        arr = output.split(' ')
        if arr[1] == "(-":
            # DW: ((to (- 0.75)))
            output = arr[1].replace('(', '') + arr[2].replace(')', '').replace('?', '')
        else:
            # DW: ((to 0.75))
            output = arr[1].replace(')', '').replace('?', '')

        f.write(output + "\n")
    else:
        print str_output_prefix_1 + output

# DW: run the main function
if __name__ == "__main__": main()

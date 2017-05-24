#!/usr/bin/env python2

import time
import subprocess
import sys
import distutils.spawn
import random
import os

# DW: the main function
def main():
    # DW: record verification time in total
    tstart = time.time()
    tformatstr = "{:.6f}"

    # DW: different level of the notion
    str_output_prefix_1 = "\tDFS script: "
    str_output_prefix_2 = "\t"

    # DW: this may vary in different systems
    path = distutils.spawn.find_executable("z3")
    if path is None:
        raise Exception("z3 not found")
    print str_output_prefix_1 + "found z3 in path", path

    # DW: get .smt2 file name
    if (len(sys.argv) < 2):
        print str_output_prefix_1 + "please specify SMT-LIB 2 file as input"
        sys.exit(0)
    filename = str(sys.argv[1])

    # DW: prepare I/O
    fileIn = open(filename, "r")
    fileInStr = fileIn.read()

    # DW: prepare Z3 binary
    p = subprocess.Popen([path, "-in"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.stdin.write(fileInStr)
    p.stdin.flush()
    output = p.stdout.readline().strip()
    print str_output_prefix_1 + "got result", output

    re = 0
    if output == "unsat":
        # DW: CE not found
        re = 0
    elif output == "sat":
        # DW: found the CE
        p.stdin.write("(get-model)\n")
        p.stdin.flush()

        # DW: only output result if found sat
        # DW: fileIn & filename should be xxx.elt.dfs.0.smt2
        # DW: fileOut should be xxx.elt.dfs.result
        fileOutName = os.path.splitext(os.path.splitext(filename)[0])[0]
        fileOut = open(fileOutName + ".cez3", "w")
        while True :
            # DW: trim \r\n to get better output
            output = p.stdout.readline()[:-1]
            print str_output_prefix_2 + output
            fileOut.write(output + "\n")
            # DW: z3 get-model output is always ended with )
            if output == ")" :
                break
        fileOut.write("\n")
        re = 1
    elif output == "unknown":
        re = 2 

    print str_output_prefix_1 + "returns", re
    sys.exit(re)

# DW: run the main function
if __name__ == "__main__": main()

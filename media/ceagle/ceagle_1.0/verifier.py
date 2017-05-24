#!/usr/bin/env python2

import time
import subprocess
import sys
import distutils.spawn

# DW: define a function to write comments in strcmd to file
def writeToSMTFile(fsmt, strcmd):
    fsmta = strcmd.splitlines()
    #print "strcmd is", strcmd
    for fsmtae in fsmta:
        if (fsmtae.startswith("(")):
            fsmt.write(";" + fsmtae + "\n")
        else:
            fsmt.write("; " + fsmtae + "\n")

    fsmt.write("\n")
    return

# DW: define a function for adding a state, returns whether the transition exists
# DW: true, the transition exists; false, the transition doesn't exist
def reachState(fsmt, p, depth):
    strcmdcore = "(declare-const state" + str(depth) + " Tuple)\n" + "(assert (TransitionExists state" + str(depth - 1) + " state" + str(depth) + "))\n"

    # DW: the assert in unreachable state may affect later smt solving, we use push/pop if necessary
    strcmd = "(push)\n" + strcmdcore + "(check-sat)\n(pop)\n"
    p.stdin.write(strcmd)
    p.stdin.flush()
    writeToSMTFile(fsmt, strcmd)
    
    # DW: we first check whether the new state set has new state(s)
    # DW: i.e., the transition exists
    # DW: if it doesn't, the verification should output TRUE result
    output = p.stdout.readline().strip()
    #return not (output == "unsat")

    if (output == "unsat"):
        # DW: unreachable, we need do nothing
        return False
    else:
        # DW: reachable, write back useful commands
        #strcmd = strcmdcore
        #print "to write :", strcmd
        p.stdin.write(strcmdcore)

        p.stdin.flush()
        writeToSMTFile(fsmt, strcmdcore)
        return True
    

# DW: the main function
def main():
    # DW: record verification time in total
    tstart = time.time()
    tformatstr = "{:.6f}"

    # DW: this may vary in different systems
    path = distutils.spawn.find_executable("z3")
    if path is None:
        raise Exception("z3 not found")
    print "SMT script: found z3 in path", path

    # DW: different level of the notion
    str_output_prefix_1 = "BFS script: "
    str_output_prefix_2 = "\t"

    # DW: prepare Z3 binary
    p = subprocess.Popen([path, "-in"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # DW: get .smt2 file name
    if (len(sys.argv) < 2):
        print str_output_prefix_1 + "please specify SMT-LIB 2 file as input"
        sys.exit(0)
    filename = str(sys.argv[1])

    # DW: first input module smt from "; DW: begin" to "; DW: end"
    command = subprocess.check_output(["/usr/bin/sed", "-n", "/^; DW: system begin/,/^; DW: system end/p", filename]) 
    p.stdin.write(command)
    p.stdin.flush()

    # DW: open the file to append comments
    fsmt = open(filename, "a")
    fsmt.write("\n")

    strcmd = ""

    # DW: create a file to write verification result
    f = open(filename + ".result", "w")

    # DW: find out how many properties to verify
    # DW: sed -n "/(declare-const prop/p" file
    properties = []
    find_prop = False
    with open(filename) as ftmp:
        for line in ftmp.readlines():
            if find_prop:
                properties.append(line.strip('\n'))
                find_prop = False
                continue
            if line.startswith("(declare-const prop"):
                find_prop = True

    ps = properties
    if (len(ps) > 0):
        print str_output_prefix_1 + "properties are"
        print properties
    else:
        print str_output_prefix_1 + "no property to verify"

    # DW: depth, current verification depth for current prop
    # DW: depth_max_last, maximum depth reached during last props' verifications (pick the max one for all last props)
    # DW: depth_max_transition, the maximum depth our module can reach
    depth = 0
    depth_max_last = depth
    depth_max_transition = -1

    # DW: start verification
    for i, prop in enumerate(ps):
        strcmd = str_output_prefix_1 + "verifying " + str(prop)
        print strcmd
        writeToSMTFile(fsmt, strcmd)

        depth = 0
        while True:
            # DW: count verify time per depth begin
            tdbegin = time.time();

            strcmd = str_output_prefix_2 + "step" + str(depth)
            print strcmd,
            writeToSMTFile(fsmt, strcmd)

            # DW: we only have to build the transition assertions for prop0, following props will use its result
            if i == 0:
                # DW: for depth other than 0, we need transition
                if depth != 0:
                    result = reachState(fsmt, p, depth)
                    if not result:
                        # DW: no transition exists anymore, reached depth_max_transition
                        depth_max_transition = depth
                        print str_output_prefix_1 + "property " + str(prop) + " holds\n"

                        # DW: update the depth_max_last if necessary
                        if depth_max_last < depth - 1:
                            depth_max_last = depth - 1
                        break;
            else:
                # DW: use states generated before this prop turn
                if depth > depth_max_last:
                    if not reachState(fsmt, p, depth):
                        # DW: no transition exists anymore, reached depth_max_transition
                        depth_max_transition = depth
                        print str_output_prefix_1 + "property " + str(prop) + " holds\n"

                        # DW: update the depth_max_last if necessary
                        if depth_max_last < depth - 1:
                            depth_max_last = depth - 1
                        break;
                    

            # DW: check-sat
            strcmd = "(push)\n" + "(assert (= prop" + str(i) + " state" + str(depth)+ "))\n" + "(check-sat)\n"
            p.stdin.write(strcmd)
            p.stdin.flush()
            writeToSMTFile(fsmt, strcmd)

            # DW: get the output of Z3
            output = p.stdout.readline().strip()
            print str_output_prefix_2 + output

            # DW: count verify time per depth end 
            tdend = time.time()
            print str_output_prefix_2 + tformatstr.format(tdend - tdbegin) + "s"

            f.write(output + "\n")
            if output == "unsat":
                # DW: the \n is needed for stdin way input
                strcmd = "(pop)\n"
                p.stdin.write(strcmd)
                p.stdin.flush()
                writeToSMTFile(fsmt, strcmd)

                depth += 1

                # DW: output a new line
                #print ""
            elif output == "sat":
                # DW: the \n is needed for stdin way input
                strcmd = "(get-model)\n" + "(pop)\n"
                p.stdin.write(strcmd)
                p.stdin.flush()
                writeToSMTFile(fsmt, strcmd)
                print str_output_prefix_1 + "property doesn't hold, counter-example is"
                while True :
                    # DW: trim \r\n to get better output
                    output = p.stdout.readline()[:-1]
                    print output
                    f.write(output + "\n")
                    # DW: z3 get-model output is always ended with )
                    if output == ")" :
                        break
                f.write("\n")

                # DW: output a new line
                #print ""
    
                # DW: update the depth_max_last if necessary
                if depth_max_last < depth:
                    depth_max_last = depth
                break
            else:
                print str_output_prefix_1 + "error"
                break

    print str_output_prefix_1 + "done"

    # DW: count the time
    tend = time.time()
    print str_output_prefix_1 + "used " + tformatstr.format(tend - tstart) + "s in total"

# DW: run the main function
if __name__ == "__main__": main()

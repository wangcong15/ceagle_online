Ceagle

* This toolset is guaranteed to work with:
Ubuntu  14.04 x64
gcc     4.8.4
clang   3.5 (must)
llvm    3.5 (must)

* Packages needed by this tool:
g++
    sudo apt-get install g++
llvm
	sudo apt-get install llvm
	# in some system, you may have to use the following
	sudo apt-get install llvm-3.5
	sudo update-alternatives --install /usr/bin/opt opt /usr/bin/opt-3.5 100
	sudo update-alternatives --install /usr/bin/llvm-dis llvm-dis /usr/bin/llvm-dis-3.5 100
clang
	sudo apt-get install clang
	# in some system, you may have to use the following
	sudo apt-get install clang-3.5
	sudo update-alternatives --install /usr/bin/clang clang /usr/bin/clang-3.5 100

* This toolset includes (9 files):
README.TXT
    this file
ceagle.sh
    the entry script of this toolset
svie
    the C to ELTS translator
svcore
    the ELTS verifier
dfs.py
parse2str.py
parsece.sh
verifier.py
    scripts required by svcore
z3
    the pre-built Z3 SMT solver, required by svcore

* Usage:
Make sure to use this toolset in SV-COMP 2016 Floats category ONLY.

ceagle.sh foo.c
ceagle.sh foo.i
ceagle.sh *.c *.i

or you can use it in BenchExec (https://github.com/dbeyer/benchexec)

* Download:
Website: http://sts.thss.tsinghua.edu.cn/ceagle/
Executable: http://sts.thss.tsinghua.edu.cn/ceagle/data/1.0/ceagle-1.0.tar.gz
BenchExec wrapper script: http://sts.thss.tsinghua.edu.cn/ceagle/data/1.0/ceagle.py

* Copyright:
Dexi Wang, dx-wang12@mails.tsinghua.edu.cn
2011 - 2015, SV Team, Tsinghua University, China

from pycparser import c_ast, parse_file, c_generator
import os

# get the code of FUNC_NAME 
class mFuncDefVisitor(c_ast.NodeVisitor):
	def __init__(self):
		self.code = ""

	def visit_FuncDef(self, node):
		if node.decl.name == FUNC_NAME:
			self.code = GENERATOR.visit(node)

def get_expr(filename, funcname, recommend_var):
	result_expr = "Unfinished"
	global GENERATOR
	GENERATOR = c_generator.CGenerator()
	global FUNC_NAME
	FUNC_NAME = funcname

	file_ast = parse_file(filename, use_cpp=True)
	func_visitor = mFuncDefVisitor()
	func_visitor.visit(file_ast)

	# print "----------func_visitor.code----------"
	# print func_visitor.code
	# print "----------func_visitor.code----------"

	steps = 1000
	minNum = -1000
	step_length = 100
	while steps >= 0:
		new_code = add_asser(func_visitor.code, recommend_var + '>=' + str(minNum))

		file_object = open('media/test.c', 'w')
		file_object.write(new_code)
		file_object.close()

		if quick_verify('media/test.c'):
			minNum += step_length
		else:
			minNum -= step_length
			step_length /= 2.0
			if step_length <= 0.001:
				break
		steps -= 1

	steps = 1000
	maxNum = 1000
	step_length = 100
	while steps >= 0:
		new_code = add_asser(func_visitor.code, recommend_var + '<=' + str(maxNum))

		file_object = open('media/test.c', 'w')
		file_object.write(new_code)
		file_object.close()

		if quick_verify('media/test.c'):
			maxNum -= step_length
		else:
			maxNum += step_length
			step_length /= 2.0
			if step_length <= 0.001:
				break
		steps -= 1
	
	print maxNum
	print minNum
	print maxNum - minNum
	print (maxNum - minNum) < 0.01
	
	if minNum >= 9100 or maxNum <= -9100:
		print "False"
		result_expr = "False"
	elif minNum == -1000 and maxNum == 1000:
		print "True"
		result_expr = "True"
	elif (maxNum - minNum) < 0.01:
		print recommend_var + "==" + str(maxNum)
		result_expr = recommend_var + "==" + str(maxNum)
	elif minNum == -1000:
		print recommend_var + "<=" + str(maxNum)
		result_expr = recommend_var + "<=" + str(maxNum)
	elif maxNum == 1000:
		print recommend_var + ">=" + str(minNum)
		result_expr = recommend_var + ">=" + str(minNum)
	else:
		print recommend_var + ">=" + str(minNum) + " && " + recommend_var + "<=" + str(maxNum)
		result_expr = recommend_var + ">=" + str(minNum) + " && " + recommend_var + "<=" + str(maxNum)

	return result_expr

def add_asser(code, asser):
	stmt_array = code.strip().split('\n')
	for i in range(len(stmt_array)):
		if(stmt_array[i].strip().startswith('return ')):
			stmt_array[i] = ''
	stmt_array.insert(0,'extern void __VERIFIER_error() __attribute__ ((__noreturn__));\ndouble __VERIFIER_nondet_double();\nvoid __VERIFIER_assert(int cond) { if (!(cond)) { ERROR: __VERIFIER_error(); } return; }\n')
	stmt_array.insert(len(stmt_array)-1, '__VERIFIER_assert(' + asser + ");")
	result = "\n".join(stmt_array)

	return result

def quick_verify(file_name):
    line1 = "media/ceagle/ceagle_1.0/dc.sh " + file_name
    os.system(line1)
    line2 = file_name + ".graphml"
    if os.path.exists(line2):
        line3 = "rm " + file_name + ".*"
        os.system(line3)
        return 0
    else:
        line3 = "rm " + file_name + ".*"
        os.system(line3)
        return 1
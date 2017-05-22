# Cong Wang @2016
# Version 1.0
# save the times every kind of statements appears

# different type of parent node
INDEX_PARENT_TYPE = {
"<class 'pycparser.c_ast.UnaryOp'>": 0, 
"<class 'pycparser.c_ast.Assignment'>": 1, 
"<class 'pycparser.c_ast.If'>": 2, 
"<class 'pycparser.c_ast.Decl'>": 3, 
"<class 'pycparser.c_ast.Cast'>": 4, 
"<class 'pycparser.c_ast.ExprList'>": 5, 
"<class 'pycparser.c_ast.Return'>": 6, 
"<class 'pycparser.c_ast.BinaryOp'>": 7,
"<class 'pycparser.c_ast.ArrayRef'>": 8
}

from pycparser import c_ast, parse_file, c_generator
import sys
import os

PARENT_ARRAY = {}
CURRENT_FILE = ""

def find_parent(root_node, var_list):
	global PARENT_ARRAY
	root_type = str(type(root_node))
	child_nodes = root_node.children()
	if len(child_nodes) == 0:
		return
	else:
		for child_node in child_nodes:
			if isinstance(child_node[1], c_ast.ID) and child_node[1].name in var_list:
				if INDEX_PARENT_TYPE.has_key(root_type):
					PARENT_ARRAY[child_node[1].name][INDEX_PARENT_TYPE[root_type]] += 1
			else:
				find_parent(child_node[1], var_list)
	return PARENT_ARRAY
# different visit function, corresponding to different kinds of statements
class ArrayDeclVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_ArrayDecl(self, node):
		self.count += 1


class ArrayRefVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_ArrayRef(self, node):
		self.count += 1


class AssignmentVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_Assignment(self, node):
		self.count += 1


class BinaryOpVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_BinaryOp(self, node):
		self.count += 1


class BreakVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_Break(self, node):
		self.count += 1


class CaseVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_Case(self, node):
		self.count += 1


class CastVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_Cast(self, node):
		self.count += 1


class CompoundVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_Compound(self, node):
		self.count += 1


class CompoundLiteralVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_CompoundLiteral(self, node):
		self.count += 1


class ConstantVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_Constant(self, node):
		self.count += 1


class ContinueVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_Continue(self, node):
		self.count += 1


class DeclVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0
		self.param_list = []

	def visit_Decl(self, node):
		if not isinstance(node.type, c_ast.FuncDecl):
			self.param_list.append(node.name)
		self.count += 1


class DeclListVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_DeclList(self, node):
		self.count += 1


class DefaultVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_Default(self, node):
		self.count += 1


class DoWhileVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_DoWhile(self, node):
		self.count += 1


class EllipsisParamVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_EllipsisParam(self, node):
		self.count += 1


class EmptyStatementVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_EmptyStatement(self, node):
		self.count += 1


class EnumVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_Enum(self, node):
		self.count += 1


class EnumeratorVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_Enumerator(self, node):
		self.count += 1


class EnumeratorListVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_EnumeratorList(self, node):
		self.count += 1


class ExprListVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_ExprList(self, node):
		self.count += 1


class FileASTVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_FileAST(self, node):
		self.count += 1


class ForVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_For(self, node):
		self.count += 1


class FuncCallVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0
		self.asser = 0
		self.id_arr = []

	def visit_FuncCall(self, node):
		if isinstance(node.name, c_ast.ID) and (node.name.name.endswith("assert") or node.name.name == "ASSERT"):
			self.asser = 1		
			ID_visitor2 = IDVisitor2()
			ID_visitor2.visit(node.args)
			self.id_arr += ID_visitor2.id_arr
		else:
			self.count += 1

class FuncDeclVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_FuncDecl(self, node):
		self.count += 1


class FuncDefVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_FuncDef(self, node):
		self.count += 1


class GotoVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_Goto(self, node):
		self.count += 1


class IDVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_ID(self, node):
		self.count += 1

class IDVisitor2(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.id_arr = []

	def visit_ID(self, node):
		if not node.name in self.id_arr:
			self.id_arr.append(node.name)

class IdentifierTypeVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_IdentifierType(self, node):
		self.count += 1


class IfVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0
		self.id_arr = []

	def visit_If(self, node):
		if (generator.visit(node.iftrue).find('__VERIFIER_error') > 0) or (generator.visit(node.iffalse).find('__VERIFIER_error') > 0):
			ID_visitor2 = IDVisitor2()
			ID_visitor2.visit(node.cond)
			self.id_arr = ID_visitor2.id_arr
		self.count += 1


class InitListVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_InitList(self, node):
		self.count += 1


class LabelVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_Label(self, node):
		self.count += 1


class NamedInitializerVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_NamedInitializer(self, node):
		self.count += 1


class ParamListVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0
		self.param_list = []

	def visit_ParamList(self, node):
		for param_a in node.params:
			if not isinstance(param_a, c_ast.Typename):
				self.param_list.append(param_a.name)
		self.count += 1


class PtrDeclVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_PtrDecl(self, node):
		self.count += 1


class ReturnVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_Return(self, node):
		self.count += 1


class StructVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_Struct(self, node):
		self.count += 1


class StructRefVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_StructRef(self, node):
		self.count += 1


class SwitchVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_Switch(self, node):
		self.count += 1


class TernaryOpVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_TernaryOp(self, node):
		self.count += 1


class TypeDeclVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_TypeDecl(self, node):
		self.count += 1


class TypedefVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_Typedef(self, node):
		self.count += 1


class TypenameVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_Typename(self, node):
		self.count += 1


class UnaryOpVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_UnaryOp(self, node):
		self.count += 1


class UnionVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_Union(self, node):
		self.count += 1


class WhileVisitor(c_ast.NodeVisitor):

	# the init function
	def __init__(self):
		self.count = 0

	def visit_While(self, node):
		self.count += 1


# the file visitor of abstract syntax tree
class mFuncDefVisitor(c_ast.NodeVisitor):
	
	# the init function, to initialize the dictionary for functions
	def __init__(self):
		self.result = []

	def visit_FuncDef(self, node):
		func_name = node.decl.name
		func_array = [0] * 46
		# ArrayDecl
		ArrayDecl_visitor = ArrayDeclVisitor()
		ArrayDecl_visitor.visit(node)
		func_array[0] = ArrayDecl_visitor.count

		# ArrayRef
		ArrayRef_visitor = ArrayRefVisitor()
		ArrayRef_visitor.visit(node)
		func_array[1] = ArrayRef_visitor.count

		# Assignment
		Assignment_visitor = AssignmentVisitor()
		Assignment_visitor.visit(node)
		func_array[2] = Assignment_visitor.count

		# BinaryOp
		BinaryOp_visitor = BinaryOpVisitor()
		BinaryOp_visitor.visit(node)
		func_array[3] = BinaryOp_visitor.count

		# Break
		Break_visitor = BreakVisitor()
		Break_visitor.visit(node)
		func_array[4] = Break_visitor.count

		# Case
		Case_visitor = CaseVisitor()
		Case_visitor.visit(node)
		func_array[5] = Case_visitor.count

		# Cast
		Cast_visitor = CastVisitor()
		Cast_visitor.visit(node)
		func_array[6] = Cast_visitor.count

		# Compound
		Compound_visitor = CompoundVisitor()
		Compound_visitor.visit(node)
		func_array[7] = Compound_visitor.count

		# CompoundLiteral
		CompoundLiteral_visitor = CompoundLiteralVisitor()
		CompoundLiteral_visitor.visit(node)
		func_array[8] = CompoundLiteral_visitor.count

		# Constant
		Constant_visitor = ConstantVisitor()
		Constant_visitor.visit(node)
		func_array[9] = Constant_visitor.count

		# Continue
		Continue_visitor = ContinueVisitor()
		Continue_visitor.visit(node)
		func_array[10] = Continue_visitor.count

		# Decl
		Decl_visitor = DeclVisitor()
		Decl_visitor.visit(node)
		func_array[11] = Decl_visitor.count

		# DeclList
		DeclList_visitor = DeclListVisitor()
		DeclList_visitor.visit(node)
		func_array[12] = DeclList_visitor.count

		# Default
		Default_visitor = DefaultVisitor()
		Default_visitor.visit(node)
		func_array[13] = Default_visitor.count

		# DoWhile
		DoWhile_visitor = DoWhileVisitor()
		DoWhile_visitor.visit(node)
		func_array[14] = DoWhile_visitor.count

		# EllipsisParam
		EllipsisParam_visitor = EllipsisParamVisitor()
		EllipsisParam_visitor.visit(node)
		func_array[15] = EllipsisParam_visitor.count

		# EmptyStatement
		EmptyStatement_visitor = EmptyStatementVisitor()
		EmptyStatement_visitor.visit(node)
		func_array[16] = EmptyStatement_visitor.count

		# Enum
		Enum_visitor = EnumVisitor()
		Enum_visitor.visit(node)
		func_array[17] = Enum_visitor.count

		# Enumerator
		Enumerator_visitor = EnumeratorVisitor()
		Enumerator_visitor.visit(node)
		func_array[18] = Enumerator_visitor.count

		# EnumeratorList
		EnumeratorList_visitor = EnumeratorListVisitor()
		EnumeratorList_visitor.visit(node)
		func_array[19] = EnumeratorList_visitor.count

		# ExprList
		ExprList_visitor = ExprListVisitor()
		ExprList_visitor.visit(node)
		func_array[20] = ExprList_visitor.count

		# FileAST
		FileAST_visitor = FileASTVisitor()
		FileAST_visitor.visit(node)
		func_array[21] = FileAST_visitor.count

		# For
		For_visitor = ForVisitor()
		For_visitor.visit(node)
		func_array[22] = For_visitor.count

		# FuncCall
		FuncCall_visitor = FuncCallVisitor()
		FuncCall_visitor.visit(node)
		func_array[23] = FuncCall_visitor.count

		# FuncDecl
		FuncDecl_visitor = FuncDeclVisitor()
		FuncDecl_visitor.visit(node)
		func_array[24] = FuncDecl_visitor.count

		# FuncDef
		FuncDef_visitor = FuncDefVisitor()
		FuncDef_visitor.visit(node)
		func_array[25] = FuncDef_visitor.count

		# Goto
		Goto_visitor = GotoVisitor()
		Goto_visitor.visit(node)
		func_array[26] = Goto_visitor.count

		# ID
		ID_visitor = IDVisitor()
		ID_visitor.visit(node)
		func_array[27] = ID_visitor.count

		# IdentifierType
		IdentifierType_visitor = IdentifierTypeVisitor()
		IdentifierType_visitor.visit(node)
		func_array[28] = IdentifierType_visitor.count

		# If
		If_visitor = IfVisitor()
		If_visitor.visit(node)
		func_array[29] = If_visitor.count

		# InitList
		InitList_visitor = InitListVisitor()
		InitList_visitor.visit(node)
		func_array[30] = InitList_visitor.count

		# Label
		Label_visitor = LabelVisitor()
		Label_visitor.visit(node)
		func_array[31] = Label_visitor.count

		# NamedInitializer
		NamedInitializer_visitor = NamedInitializerVisitor()
		NamedInitializer_visitor.visit(node)
		func_array[32] = NamedInitializer_visitor.count

		# ParamList
		ParamList_visitor = ParamListVisitor()
		ParamList_visitor.visit(node)
		func_array[33] = ParamList_visitor.count

		# PtrDecl
		PtrDecl_visitor = PtrDeclVisitor()
		PtrDecl_visitor.visit(node)
		func_array[34] = PtrDecl_visitor.count

		# Return
		Return_visitor = ReturnVisitor()
		Return_visitor.visit(node)
		func_array[35] = Return_visitor.count

		# Struct
		Struct_visitor = StructVisitor()
		Struct_visitor.visit(node)
		func_array[36] = Struct_visitor.count

		# StructRef
		StructRef_visitor = StructRefVisitor()
		StructRef_visitor.visit(node)
		func_array[37] = StructRef_visitor.count

		# Switch
		Switch_visitor = SwitchVisitor()
		Switch_visitor.visit(node)
		func_array[38] = Switch_visitor.count

		# TernaryOp
		TernaryOp_visitor = TernaryOpVisitor()
		TernaryOp_visitor.visit(node)
		func_array[39] = TernaryOp_visitor.count

		# TypeDecl
		TypeDecl_visitor = TypeDeclVisitor()
		TypeDecl_visitor.visit(node)
		func_array[40] = TypeDecl_visitor.count

		# Typedef
		Typedef_visitor = TypedefVisitor()
		Typedef_visitor.visit(node)
		func_array[41] = Typedef_visitor.count

		# Typename
		Typename_visitor = TypenameVisitor()
		Typename_visitor.visit(node)
		func_array[42] = Typename_visitor.count

		# UnaryOp
		UnaryOp_visitor = UnaryOpVisitor()
		UnaryOp_visitor.visit(node)
		func_array[43] = UnaryOp_visitor.count

		# Union
		Union_visitor = UnionVisitor()
		Union_visitor.visit(node)
		func_array[44] = Union_visitor.count

		# While
		While_visitor = WhileVisitor()
		While_visitor.visit(node)
		func_array[45] = While_visitor.count
		
		# result
		func_dic = {'func_array': func_array}
		if FuncCall_visitor.asser == 1:
			func_dic['asser_flag'] = 1
		else:
			func_dic['asser_flag'] = 0
		
		var_array = ParamList_visitor.param_list + Decl_visitor.param_list
		var_asser = []
		for var_a in var_array:
			if var_a in If_visitor.id_arr + FuncCall_visitor.id_arr:
				var_asser.append(var_a)
		func_dic['asser_var'] = var_asser

		# DEBUG
		if len(var_asser) == 0 and FuncCall_visitor.asser == 1:
			return

		global PARENT_ARRAY
		PARENT_ARRAY = {}
		for var_a in var_array:
			PARENT_ARRAY[var_a] = [0] * 9
		func_dic['all_var'] = find_parent(node, var_array)
		global CURRENT_FILE
		func_dic['src_name'] = CURRENT_FILE
		func_dic['func_name'] = func_name
		if func_name != '__VERIFIER_assert' and func_name != '__VERIFIER_assume' and func_name != '__VERIFIER_nondet_float' and func_name != '__VERIFIER_nondet_int':
			self.result.append(func_dic)

# code entrance of this version
def gen_feat(file_name):
	global generator
	generator = c_generator.CGenerator()
	global CURRENT_FILE
	CURRENT_FILE = file_name
	file_ast = parse_file(file_name, use_cpp=True)
	func_visitor = mFuncDefVisitor()
	func_visitor.visit(file_ast)
	return func_visitor.result

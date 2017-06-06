from pycparser import c_ast, parse_file, c_generator
import re

def serial_func(ast):
    if ast.__class__.__name__ == 'Compound':
        result = ""
        body_items = ast.block_items
        for body_item in body_items:
            result += serial_func(body_item)
    else:
        result = ast.__class__.__name__ + "("
        if ast.__class__.__name__ == 'FileAST':
            if c_generator.CGenerator().visit(ast.ext[0].decl.type).startswith('unsigned'):
                result += "{unsigned}"
            result += serial_func(ast.ext[0].body)
        elif ast.__class__.__name__ == 'If':
            result += "[" + serial_func(ast.cond) + "]" + "{" + serial_func(ast.iftrue) + "}" + "{" + serial_func(ast.iffalse) + "}"
        elif ast.__class__.__name__ == 'FuncCall':
            result += ast.name.name
            if ast.name.name == "strncpy" or ast.name.name == "memcpy":
                result += "(" + c_generator.CGenerator().visit(ast.args.exprs[0]) + "," + c_generator.CGenerator().visit(ast.args.exprs[1]) + "," + c_generator.CGenerator().visit(ast.args.exprs[2]) + ")"
            if ast.name.name == "memset":
                result += "(" + ast.args.exprs[0].name + ")"
            if ast.name.name == "printf":
                result += "("
                temp_exprs = ast.args.exprs
                for temp_expr in temp_exprs:
                    if temp_expr.__class__.__name__ == "ArrayRef":
                        array_name = temp_expr.name.name
                        array_offset = c_generator.CGenerator().visit(temp_expr.subscript)
                        result += "ArrayRef([" + array_name + "," + array_offset + "])"
                result += ")"
        elif ast.__class__.__name__ == 'Decl':
            result += "[" + serial_func(ast.type) + "[init](" + ast.name + ")" + "]"
        elif ast.__class__.__name__ == 'PtrDecl':
            result += "["
            if ast.type.__class__.__name__  == "FuncDecl":
                result += "FuncDecl(" + ast.type.type.declname + ")"
            result += "]"
        elif ast.__class__.__name__ == 'Assignment':
            result += c_generator.CGenerator().visit(ast)
        elif ast.__class__.__name__ == 'For':
            result += serial_func(ast.stmt)
        elif ast.__class__.__name__ == 'Switch':
            temp_stmts = ast.stmt.block_items
            flag_has_default = False
            for temp_stmt in temp_stmts:
                if temp_stmt.__class__.__name__ == "Default":
                    flag_has_default = True
                    break
            result += ast.cond.name + "," + serial_func(ast.stmt)
            if not flag_has_default:
                result += "NoDefault"
        elif ast.__class__.__name__ == 'Case':
            result += c_generator.CGenerator().visit(ast.expr) + ","
            temp_stmts = ast.stmts
            flag_has_break = False
            for temp_stmt in temp_stmts:
                if temp_stmt.__class__.__name__ == "Break":
                    flag_has_break = True
                    break
            if not flag_has_break:
                result += "NoBreak"
        elif ast.__class__.__name__ == 'Return':
            result += c_generator.CGenerator().visit(ast.expr)
        result += ")"
    return result

pattern1 = 'Decl\(\[PtrDecl\(\[FuncDecl\(.*?\)\]\)\[init\]\((.*?)\)\]\)'
pattern2 = 'If\(\[Assignment\((.*?)\]'
pattern3 = 'malloc\((.*?)\)'
pattern4 = '(strncpy|memcpy)\((.*?),.*?,(.*?)\)'
pattern5 = 'Decl\(\[ArrayDecl\(.*?\((.*?)\).*?For\(.*?Assignment\((.*?)\[(.*?)]'
pattern6 = 'ArrayRef\(\[(.*?),(.*?)\]\)'
pattern7 = 'Case\((.*?)\)'
pattern8 = 'Case\(.*?,NoBreak\)'
pattern9 = '\{unsigned\}.*?Return\((.*?)\)'
pattern10 = '(strncpy|memcpy)\((.*?),(argc|argv.*),.*?\)'

def expression_generation(file_name):
    file_ast = parse_file(file_name)
    serial = serial_func(file_ast)
    print serial
    result = ""
    ##[No.1] Assignment of a fixed address to a pointer
    if len(re.findall(pattern1, serial))>0:
        result += "assert(strcmp(init_"+re.findall(pattern1, serial)[0][0]+", final_"+re.findall(pattern1, serial)[0][0]+")==0);"
    ##[No.2] Assigning instead of Comparing
    if len(re.findall(pattern2, serial))>0:
        tempstr = "assert("+re.findall(pattern2, serial)[0]+");"
        result += tempstr.replace('=','==')
    ##[No.3] Wrap-around Error
    if len(re.findall(pattern3, serial))>0:
        result += "assert("+re.findall(pattern3, serial)[0][0]+"<10000000000);"
    ##[No.4] Buffer Access with Incorrect Length Value 
    if len(re.findall(pattern4, serial))>0:
        result += "assert("+re.findall(pattern4, serial)[0][1]+"<=sizeof("+re.findall(pattern4, serial)[0][0]+");" 
    ##[No.5] Deletion of Data Structure Sentinel
    if len(re.findall(pattern5, serial))>0:
        result += "assert("+re.findall(pattern5, serial)[0][2]+"&lt;sizeof("+re.findall(pattern5, serial)[0][0]+")-1;"
    ##[No.6] Improper Restriction of Operations within the Bounds 
    if len(re.findall(pattern6, serial))>0:
        result += "assert("+re.findall(pattern6, serial)[0][1]+"&lt;sizeof("+re.findall(pattern6, serial)[0][0]+")&&"+re.findall(pattern6, serial)[0][1]+"&gt;= 0);"
        print result
    ##[No.7] Missing Default Case in Switch Statement
    if len(re.findall(pattern7, serial))>0 and serial.find("NoDefault")>=0:
        result += "assert(switch_variable==0||switch_variable==1);"
    ##[No.8] Omitted Break Statement in Switch
    if len(re.findall(pattern8, serial))>0:
        result += "assert(true);"
    ##[No.9] Signed to Unsigned Conversion Error
    if len(re.findall(pattern9, serial))>0:
        result += "assert("+re.findall(pattern9, serial)[0]+"> 0);"
    ##[No.10] Use of Externally-Controlled Format String
    if len(re.findall(pattern10, serial))>0:
        result += "assert("+re.findall(pattern10, serial)[0][1]+");"
    return result
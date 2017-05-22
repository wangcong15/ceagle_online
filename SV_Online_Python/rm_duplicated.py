def rm_dup(fea_arr):
	return_arr = []
	for fea_i in fea_arr:
		if fea_i not in return_arr:
			return_arr.append(fea_i)
	return return_arr 

def rm_dup2(fea_arr):
	return_arr = []
	func_array = []
	for fea_i in fea_arr:
		if fea_i['func_array'] not in func_array:
			return_arr.append(fea_i)
			func_array.append(fea_i['func_array'])
	return return_arr
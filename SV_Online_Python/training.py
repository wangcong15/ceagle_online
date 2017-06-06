# Cong Wang @2016
# sv-comp:training
# cprover:testing
# ast-possible files with properties
# rm the duplicated features

import sys
from feature4 import feature as fea_train, index_flag
from rm_duplicated import rm_dup2
from pro_rec3 import gen_feat
import math
from models import user_coefficient
from serial import expression_generation

preHandled = 0

def distance(left_data, right_data, efficient):
	temp_sum_left = left_data['func_array'].pop()
	temp_sum_right = right_data['func_array'].pop()
	if abs(temp_sum_right - temp_sum_left) <= 130:
		total_dis = 0.0
	else:
		total_dis = 10.0
	for i in range(len(left_data['func_array'])):
		total_dis += (left_data['func_array'][i] - right_data['func_array'][i]) * (left_data['func_array'][i] - right_data['func_array'][i])
	left_data['func_array'].append(temp_sum_left)
	right_data['func_array'].append(temp_sum_right)
	# print total_dis
	return total_dis / efficient

def basic_dis(left_data, right_data):
	total_dis = 0.0
	for i in range(len(left_data)):
		total_dis += (left_data[i] - right_data[i]) * (left_data[i] - right_data[i])
	return total_dis

# pre-handle the data
def pre_handle():
	if preHandled == 0:
		global fea_train
		fea_train = rm_dup2(fea_train)
		for i in range(len(fea_train)):
			feature_sum = 0.0
			for j in range(len(fea_train[i]['func_array'])):
				feature_sum += float(fea_train[i]['func_array'][j])
			for j in range(len(fea_train[i]['func_array'])):
				fea_train[i]['func_array'][j] = float(fea_train[i]['func_array'][j]) / feature_sum
			fea_train[i]['func_array'].append(feature_sum)
	global fea_test
	for i in range(len(fea_test)):
		feature_sum = 0.0
		for j in range(len(fea_test[i]['func_array'])):
			feature_sum += float(fea_test[i]['func_array'][j])
		for j in range(len(fea_test[i]['func_array'])):
			fea_test[i]['func_array'][j] = float(fea_test[i]['func_array'][j]) / feature_sum
		fea_test[i]['func_array'].append(feature_sum)

def get_most(result_arr):
	return_result = ""
	max_num = 0
	for result_a in result_arr.keys():
		if result_arr[result_a] > max_num:
			max_num = result_arr[result_a]
			return_result = result_a
	return return_result

def get_var_rec(train_vars, test_data):
	result = {}
	for train_var in train_vars:
		if train_var['asser_flag'] == 0:
			continue
		train_all_var = train_var['all_var']
		train_asser_var = train_var['asser_var']
		test_all_var = test_data['all_var']
		test_all_var_list = test_all_var.keys()
		min_dis = 10000
		min_test_var = ""
		for test_var_i in test_all_var_list:
			temp_dis = 0.0
			for train_asser_var_i in train_asser_var:
				temp_dis += basic_dis(test_all_var[test_var_i], train_all_var[train_asser_var_i])
			if temp_dis < min_dis:
				min_dis = temp_dis
				min_test_var = test_var_i
		if result.has_key(min_test_var):
			result[min_test_var] += 1
		else:
			result[min_test_var] = 1
	return get_most(result)

def predict_flag(test_data, user_name):
	# Coefficient
	select_uc = user_coefficient.objects.filter(ucuser=user_name)
	current_efficient = [1] * 7386
	# Still no efficient for this user
	if len(select_uc) == 0:
		new_uc = user_coefficient(ucuser=user_name,ucefficient=str([1]*7386))
		new_uc.save()
	else:
		current_efficient = select_uc[0].ucefficient
		current_efficient = current_efficient.replace("[","")
		current_efficient = current_efficient.replace("]","")
		current_efficient = current_efficient.split(", ")
		for i in range(len(current_efficient)):
			current_efficient[i] = float(current_efficient[i])
	index_temp_array = [-1] * 3
	flag_temp_array = [2] * 3
	close_temp_array = [100] * 3
	func_temp_array = [{}] * 3
	for i, train_a in enumerate(fea_train):
		temp_index_stack = []
		temp_flag_stack = []
		temp_close_stack = []
		temp_func_array = []
		temp_dis = distance(test_data, train_a, current_efficient[i])
		if temp_dis >= close_temp_array[2]:
			continue
		for temp_close_a in reversed(close_temp_array):
			if temp_close_a > temp_dis:
				temp_index_stack.append(index_temp_array.pop())
				temp_flag_stack.append(flag_temp_array.pop())
				temp_close_stack.append(close_temp_array.pop())
				temp_func_array.append(func_temp_array.pop())
		index_temp_array.append(i)
		flag_temp_array.append(train_a['asser_flag'])
		close_temp_array.append(temp_dis)
		func_temp_array.append(train_a)
		while(not len(close_temp_array) == 3):
			index_temp_array.append(temp_index_stack.pop())
			flag_temp_array.append(temp_flag_stack.pop())
			close_temp_array.append(temp_close_stack.pop())
			func_temp_array.append(temp_func_array.pop())
	result = 0
	for flag_a in flag_temp_array:
		if flag_a == 0:
			result -= 1
		elif flag_a == 1:
			result += 1
	if result >= 0:
		return 1, index_temp_array
	else:
		return 0, index_temp_array

def propertyRecommendation(filename, username):

	global fea_test
	fea_test = gen_feat(filename)
	pre_handle()
	global preHandled
	preHandled = 1

	final_result = []
	for key in fea_test:
		assertion_flag, common_index_array = predict_flag(key, username)

		if assertion_flag:
			expr, caption = expression_generation(filename)
			final_result.append({'function':key['func_name'], 'needAssertion':'Need','expr': expr, 'common_index_array': common_index_array,'caption':caption})
		else:
			final_result.append({'function':key['func_name'], 'needAssertion':'No Need', 'expr': "", 'common_index_array': common_index_array,'caption':''})
	return final_result

# -*- coding: utf-8 -*-
def convert_filter_keys(result, keys):
	response_object = {}
	for key in keys:
		response_object[key] = result[key]
	return response_object
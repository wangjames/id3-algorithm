import math

class Node(object):

	def __init__(self):
		self.iteration_index = []
		self.children_nodes = []
		self.instance_dict = {}
		self.node_attribute = ""
		self.node_value = ""

	
	def set_iteration_index(self, index_list):
		self.iteration_index = index_list

	def set_children_nodes(self, children_list):
		self.children_nodes = children_list

	def set_instances(self, instances):
		self.instance_dict = instances

	def set_node_attribute(self, attribute):
		self.node_attribute = attribute

	def set_node_value(self, value):
		self.node_value = value

	def get_node_value(self):
		return self.node_value

	def get_iteration_attributes(self):
		return self.iteration_index

	def get_instances(self):
		return self.instance_dict

	def get_node_attribute(self):
		return self.node_attribute

	def get_children_nodes(self):
		return self.children_nodes


class ID3Instance(object):

	def __init__(self):
		self.attribute_names = []
		self.attribute_values = []
		self.attribute_indexes = []
		self.root = Node()
		self.class_index = 0
		self.class_values = []

	# def generateCounts(attribute_check_list, instances):
	# 	count_list = []
	# 	for number in range(len(attribute_check_list)):
	# 		count_list.append([])
	# 	for key in instances:
	# 		if (key[0] == 1):

	def calculate_entropy(self, instances):
		
		# initiate counts for classifying instances
		class_1_count = 0
		class_2_count = 0

		# for all instances, check class_index of string to see if instance belongs to class 1 or class 2
		for key in instances:
			if int(key[self.class_index]) == 0:
				class_1_count += instances[key]
			elif int(key[self.class_index]) == 1:
				class_2_count += instances[key]

		# add up counts for both and put counts into list for processing
		total_count = class_1_count + class_2_count
		count_list = [class_1_count, class_2_count]
		
		# create list to hold intermediate entropy values
		count_perc_list = []
		count_log_list = []
		count_perc = 0.0
		count_log = 0.0
		# perform same entropy calculations on both counts
		for count in count_list:
			
			if count != 0:

				count_perc = float(count) / float(total_count)
				count_perc_list.append(count_perc)

				count_log = math.log(count_perc, 2)
				count_log_list.append(count_log)

			elif count == 0:
				count_perc_list.append(0)
				count_log_list.append(0)

		# sum up entropy calculations and return the negative form of the entropy calculation
		result_entropy = 0.0
		for index in range(len(count_list)):
			entropy_contribution = count_perc_list[index]
			entropy_contribution *= count_log_list[index]
			result_entropy += entropy_contribution

		return -result_entropy

	def get_subset(self, attribute_index, attribute_value_index, instances):
		
		result_dict = {}

		for key in instances:
			if int(key[attribute_index]) == attribute_value_index:
				result_dict[key] = instances[key]
		
		return result_dict


	def return_count(self, instance_dict):
		count = 0

		for element in instance_dict:
			count += instance_dict[element]

		return count

	def generate_children(self, input_node):
		

		# first step, retrieve instances and attribute indexes to iterate through from input node
		node_instances = input_node.get_instances()
		attribute_iteration_list = input_node.get_iteration_attributes()

		# if node has no more attributes to iterate through then return
		if (len(attribute_iteration_list) == 0):
			print "hi"
			return

		# calculate root entropy
		root_entropy = self.calculate_entropy(node_instances)
		
		# if root entropy is 0 then node is leaf so return
		if (root_entropy == 0.0):
			return

		# initiate variables that will hold top entropy attribute
		top_entropy = 100.0
		top_attribute_index = 0
		
		# iterate through every attribute and calculate entropy
		for index in attribute_iteration_list:

			# retrieve values_list for each attribute
			values_list = self.attribute_values[index]
			attribute_entropy = 0.0
			
			# iterate through every value of the attribute
			# get the subset of instances that has that value
			# calculate weighted entropy
			# add to the total attribute entropy 
			for value_index in range(len(values_list)):
				subset = self.get_subset(index, value_index, node_instances)
				subset_count = self.return_count(subset)
				subset_entropy = self.calculate_entropy(subset)

				subset_entropy *= subset_count

				attribute_entropy += subset_entropy
			
			# if attribute entropy is greatest, then set as the top
			if attribute_entropy < top_entropy:
				top_entropy = attribute_entropy
				top_attribute_index = index

	
		# with top attribute chosen, create children nodes for each value and the set of instances
		top_attribute_values = self.attribute_values[top_attribute_index]
		attribute_iteration_list.remove(top_attribute_index)
		attribute_name = self.attribute_names[top_attribute_index]
		
		child_list = []
		
		for value_index in range(len(top_attribute_values)):
			child_node = Node()
			
			child_instances = self.get_subset(top_attribute_index, value_index, node_instances)
			child_node.set_instances(child_instances)
			
			child_node.set_iteration_index(attribute_iteration_list)
			child_node.set_node_attribute(attribute_name)
			
			value_name = top_attribute_values[value_index]
			child_node.set_node_value(value_name)

			child_list.append(child_node)

		# for every child node, call generate_children function to create children nodes for the children nodes
		for child_node in child_list:
			self.generate_children(child_node)
		
		input_node.set_children_nodes(child_list)

		return input_node

	def read_data(self):
		
		# prompt user for file name
		filename = str(raw_input("Input your filename: "))
		class_index = int(raw_input("Enter class index (usually 0): "))

		input_file = open(filename, 'r')
		
		# take first list of file to draw in names
		
		attributes_string = input_file.next()
		self.attribute_names = attributes_string.split(" ")

		# create lists to hold attribute values and attribute indexes
		
		for number in range(len(self.attribute_names)):
			self.attribute_values.append([])
			self.attribute_indexes.append(number)

		self.root.set_iteration_index(self.attribute_indexes[1:])

		# iterate through all instances in file
		# create a string with each character serving as the index number for the attribute value
		# character position of the string corresponds to attribute_index
		# for example, string 00 corresponds to instance with the values that exist at the 0 index of the 0th and 1st attribute
		# place these strings into string_dict
		string_dict = {}

		for line in input_file:
			hashed_string = ""
			
			line_values = line.split(" ")

			try:
				line_values.remove("")
			except:
				pass

			for index in range(len(line_values)):
				selected_attribute = self.attribute_values[index]
				value = line_values[index]
				try:
					hashed_string += str(selected_attribute.index(value))
				except:
					selected_attribute.append(value)
					hashed_string += str(selected_attribute.index(value))
		
			try:
				string_dict[hashed_string] += 1
			except:
				string_dict[hashed_string] = 1
		
		# set the instance dict for the root and the attribute values
		self.root.set_instances(string_dict)
		# self.root.set_iteration_index(self.attribute_values)

		# set the class values
		class_values = self.attribute_values[class_index]

	def get_class_index(self, instance_dict):
		
		# count up the class counts in the instances
		# if the number is split, pick the highest number

		class_count_1 = 0
		class_count_2 = 0

		for key in instance_dict:
			if int(key[self.class_index]) == 0:
				class_count_1 += instance_dict[key]
			elif int(key[self.class_index]) == 1:
				class_count_2 += instance_dict[key]

		count_list = [class_count_1, class_count_2]
		bigger_count = max(count_list)

		return count_list.index(bigger_count)

	def print_tree(self, node, space):
		child_list = node.get_children_nodes()

		node_instances = node.get_instances()
		
		node_value = node.get_node_value()
		node_attribute = node.get_node_attribute()
		node_class_value = self.get_class_index(node_instances)

		print "Node's attribute is " + node_attribute
		print "Node's value is " + node_value
		print "Node's class value is " + self.attribute_values[self.class_index][node_class_value]

		if (len(child_list) != 0):
			print "This node has the following children."
			space += "       "

			for child in child_list:
				self.print_tree(child, space)

		return






	def create_skeleton(self):
		# read in data
		self.read_data()

		# #tree generation process
		# self.root = self.generate_children(self.root)

		# # # print the tree
		# self.print_tree(self.root, "")

if __name__ == "__main__":


	id1 = ID3Instance()
	id1.create_skeleton()

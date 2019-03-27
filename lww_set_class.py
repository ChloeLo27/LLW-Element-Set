""" IMPORT LIBRARIES """
from datetime import datetime
from typing import List

__all__ = ["LWW_Set"]

class _LWW_Set__LWW_Element(object):
	"""docstring for _LWW_Set__LWW_Element"""
	def __init__(self, element):
		self.element = element
		self.__timestamps = [datetime.now()]

	def __repr__(self):
		return "(element: {}, timestamps: {})".format(self.element, self.__timestamps)

	def update_timestamp(self):
		self.__timestamps.append(datetime.now())

	@property
	def last_timestamp(self):
		return max(self.__timestamps)
	
		

class LWW_Set():
	"""docstring for LWW_Set"""
	def __init__(self, debug=False):
		self.__add_set = []
		self.__remove_set = []
		self.__debug = debug

	def __repr__(self):
		return "LWW Set\n=======\nADD SET: {}\n\nREMOVE SET: {}\n=======\n".format(self.__add_set, self.__remove_set)

	def exist(self, element, timestamp=None):
		""" check whether an element exists in the LWW set of not """
		element_in_add_set = [x for x in self.__add_set if x.element == element]
		element_in_remove_set = [x for x in self.__remove_set if x.element == element]
		if not element_in_add_set:
			return False
		if not element_in_remove_set:
			return True
		if timestamp is None:
			return element_in_remove_set[0].last_timestamp <= element_in_add_set[0].last_timestamp
		# TODO: look up the existence of the element before the given timestamp

	def get(self, timestamp=None) -> List[__LWW_Element]:
		"""
		return a list contianing the elements which should be in the set right before the given timestamp;
		return the most updated state if no timestamp given
		"""
		if timestamp is None:
			return [x.element for x in self.__add_set if self.exist(x.element)]
		# TODO: return the set at the state right before the given timestamp
		
	def add(self, element) -> LWW_Set:
		""" add element to the set """
		if not self.exist(element):
			self.__add_set.append(__LWW_Element(element))
		else:
			[x for x in self.__add_set if x.element == element][0].update_timestamp()
		if self.__debug:
			print(self)
		return self

	def remove(self, element) -> LWW_Set:
		""" remove element from the set """
		if self.exist(element):
			element_in_remove_set = [x for x in self.__remove_set if x.element == element]
			if element_in_remove_set:
				element_in_remove_set[0].update_timestamp()
			else:
				self.__remove_set.append(__LWW_Element(element))
		if self.__debug:
			print(self)
		return self
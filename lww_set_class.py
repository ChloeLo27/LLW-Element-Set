""" IMPORT LIBRARIES """
from datetime import datetime
from typing import List, TypeVar
from collections import Hashable

LWW_Set = TypeVar('LWW_Set')

class _LWW_Set__LWW_Element(object):
	"""docstring for _LWW_Set__LWW_Element"""
	def __init__(self, element):
		self.element = element
		self.__timestamps = [datetime.now()]

	def __repr__(self):
		return "(element: {}, timestamps: {})".format(self.element, self.__timestamps)

	def update_timestamp(self):
		self.__timestamps.append(datetime.now())

	def last_timestamp_before(self, timestamp):
		timestamps_before = [t for t in self.__timestamps if t <= timestamp]
		if timestamps_before:
			return max(timestamps_before)
		else:
			return None

	@property
	def last_timestamp(self):
		return max(self.__timestamps)

	@property
	def first_timestamp(self):
		return min(self.__timestamps)
	
		

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

		if timestamp is None:
			element_in_add_set = [x for x in self.__add_set if x.element == element]
			element_in_remove_set = [x for x in self.__remove_set if x.element == element]
		else:
			element_in_add_set = [x for x in self.__add_set if x.element == element and x.last_timestamp_before(timestamp) is not None]
			element_in_remove_set = [x for x in self.__remove_set if x.element == element and x.last_timestamp_before(timestamp) is not None]

		if not element_in_add_set:
			return False
		if not element_in_remove_set:
			return True
		if timestamp is None:
			return element_in_remove_set[0].last_timestamp < element_in_add_set[0].last_timestamp

	def get(self, timestamp=None) -> List[__LWW_Element]:
		"""
		return a list contianing the elements which should be in the set right before the given timestamp;
		return the most updated state if no timestamp given
		"""
		return set([x.element for x in self.__add_set if self.exist(x.element, timestamp)])
		
	def add(self, element) -> LWW_Set:
		"""
		add element to the set
		NOTE: cannot accept unhashable types
		"""

		if not isinstance(element, Hashable):
			raise TypeError("LWW element set accepts only hashable types.")

		element_in_add_set = [x for x in self.__add_set if x.element == element]
		if not element_in_add_set:
			self.__add_set.append(__LWW_Element(element))
		else:
			element_in_add_set[0].update_timestamp()
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

	# TODO: merge method, updating both copies
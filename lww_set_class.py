""" IMPORT LIBRARIES """
from datetime import datetime
from typing import List, TypeVar
from collections import Hashable

LWW_Set = TypeVar('LWW_Set')

class _LWW_Set__LWW_Element(object):
	"""docstring for _LWW_Set__LWW_Element"""
	def __init__(self, element, with_timestamps=None):
		self.element = element
		if with_timestamps is None:
			self.__timestamps = [datetime.now()]
		else:
			self.__timestamps = with_timestamps

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

	def merge_timestamps(self, element2):
		if self.element != element2.element:
			raise ValueError("Elements mismatch.  First: {}, second: {}.".format(self.element, element2.element))
		timestamps_1 = set(self.__timestamps)
		timestamps_2 = set(element2.__timestamps)
		union_timestamp = sorted(list(timestamps_1.union(timestamps_2)))
		self.__timestamps = union_timestamp
		element2.__timestamps = union_timestamp

	@property
	def last_timestamp(self):
		return max(self.__timestamps)

	@property
	def first_timestamp(self):
		return min(self.__timestamps)

	@property
	def timestamps(self):
		return self.__timestamps


class LWW_Set():
	"""docstring for LWW_Set"""
	def __init__(self, debug=False):
		self.__add_set = []
		self.__remove_set = []
		self.__debug = debug

	def __repr__(self):
		return "LWW Set\n=======\nADD SET: {}\n\nREMOVE SET: {}\n=======\n".format(self.__add_set, self.__remove_set)

	def _element_in_add_set(self, element, timestamp=None):
		if timestamp is None:
			result = [x for x in self.__add_set if x.element == element]
		else:
			result = [x for x in self.__add_set if x.element == element and x.last_timestamp_before(timestamp) is not None]
		if result:
			return result[0]
		return None

	def _element_in_remove_set(self, element, timestamp=None):
		if timestamp is None:
			result = [x for x in self.__remove_set if x.element == element]
		else:
			result = [x for x in self.__remove_set if x.element == element and x.last_timestamp_before(timestamp) is not None]
		if result:
			return result[0]
		return None

	@property
	def _add_set_elements(self):
		return [x.element for x in self.__add_set]

	@property
	def _remove_set_elements(self):
		return [x.element for x in self.__remove_set]
	

	def exist(self, element, timestamp=None):
		""" check whether an element exists in the LWW set of not """

		element_in_add_set = self._element_in_add_set(element, timestamp=timestamp)
		element_in_remove_set = self._element_in_remove_set(element, timestamp=timestamp)

		if element_in_add_set is None:
			return False
		if element_in_remove_set is None:
			return True
		if timestamp is None:
			return element_in_remove_set.last_timestamp < element_in_add_set.last_timestamp

	def get(self, timestamp=None) -> List[__LWW_Element]:
		"""
		return a list contianing the elements which should be in the set right before the given timestamp;
		return the most updated state if no timestamp given
		"""
		return set([x.element for x in self.__add_set if self.exist(x.element, timestamp)])
		
	def add(self, element, with_timestamps=None) -> LWW_Set:
		"""
		add element to the set
		NOTE: cannot accept unhashable types
		"""

		if not isinstance(element, Hashable):
			raise TypeError("LWW element set accepts only hashable types.")

		element_in_add_set = self._element_in_add_set(element)
		if element_in_add_set is None:
			self.__add_set.append(__LWW_Element(element, with_timestamps))
		else:
			element_in_add_set.update_timestamp()
		if self.__debug:
			print(self)
		return self

	def remove(self, element, with_timestamps=None) -> LWW_Set:
		""" remove element from the set """

		element_in_remove_set = self._element_in_remove_set(element)
		if element_in_remove_set is not None:
			element_in_remove_set.update_timestamp()
		else:
			self.__remove_set.append(__LWW_Element(element, with_timestamps))
		if self.__debug:
			print(self)
		return self

	def merge(self, lww_set_2) -> LWW_Set:
		""" merge with another set """

		# add set merge
		add_set_1 = set(self._add_set_elements)
		add_set_2 = set(lww_set_2._add_set_elements)
		union_of_add_sets = add_set_1.union(add_set_2)
		intersection_of_add_sets = add_set_1.intersection(add_set_2)
		for element in union_of_add_sets:
			if element in intersection_of_add_sets:
				self._element_in_add_set(element).merge_timestamps(lww_set_2._element_in_add_set(element))
			elif element in add_set_1:
				lww_set_2.add(element, with_timestamps=self._element_in_add_set(element).timestamps)
			else:
				self.add(element, with_timestamps=lww_set_2._element_in_add_set(element).timestamps)

		# remove set merge
		remove_set_1 = set(self._remove_set_elements)
		remove_set_2 = set(lww_set_2._remove_set_elements)
		union_of_remove_sets = remove_set_1.union(remove_set_2)
		intersection_of_remove_sets = remove_set_1.intersection(remove_set_2)
		for element in union_of_remove_sets:
			if element in intersection_of_remove_sets:
				self._element_in_remove_set(element).merge_timestamps(lww_set_2._element_in_remove_set(element))
			elif element in remove_set_1:
				lww_set_2.remove(element, with_timestamps=self._element_in_remove_set(element).timestamps)
			else:
				self.remove(element, with_timestamps=lww_set_2._element_in_remove_set(element).timestamps)

		return self


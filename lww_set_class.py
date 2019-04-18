""" IMPORT LIBRARIES """
from datetime import datetime
from typing import List, TypeVar
from collections import Hashable

LWW_Set = TypeVar('LWW_Set')

class _LWW_Set__LWW_Element(object):
	"""Private class for the LWW element

	Keyword arguments:
	element -- the element to be added to the set
	with_timestamps -- the initial set of timestamps to be used (default None)
	"""
	def __init__(self, element, with_timestamps=None):
		self.element = element
		if with_timestamps is None:
			self.__timestamps = [datetime.now()]
		else:
			self.__timestamps = with_timestamps

	def __repr__(self):
		return "(element: {}, timestamps: {})".format(self.element, self.__timestamps)

	def update_timestamp(self):
		"""Add the timestamp of the instance when this is called."""
		self.__timestamps.append(datetime.now())

	def last_timestamp_before(self, timestamp):
		"""Retrieve the last timestamp before the given timestamp; return None if there is none."""
		timestamps_before = [t for t in self.__timestamps if t <= timestamp]
		if timestamps_before:
			return max(timestamps_before)
		else:
			return None

	def merge_timestamps(self, element2):
		"""Merge the timestamps of this element and the other one, and update the stored timestamps of both copies."""
		if self.element != element2.element:
			raise ValueError("Elements mismatch.  First: {}, second: {}.".format(self.element, element2.element))
		timestamps_1 = set(self.__timestamps)
		timestamps_2 = set(element2.__timestamps)
		union_timestamp = sorted(list(timestamps_1.union(timestamps_2)))
		self.__timestamps = union_timestamp
		element2.__timestamps = union_timestamp

	def add_timestamps(self, timestamps):
		"""Merge the timestamps of this element with the given list of timestamps."""
		union_timestamp = sorted(list(set(self.__timestamps).union(set(timestamps))))
		self.__timestamps = union_timestamp

	@property
	def last_timestamp(self):
		"""Return the last timestamp of the element."""
		return max(self.__timestamps)

	@property
	def first_timestamp(self):
		"""Return the first timestamp of the element."""
		return min(self.__timestamps)

	@property
	def timestamps(self):
		"""Return the list of timestamps of the element."""
		return self.__timestamps


class LWW_Set():
	"""LWW Set class.

	Keyword arguments:
	debug -- set debug mode (default False)
	"""
	def __init__(self, debug=False):
		self.__add_set = []
		self.__remove_set = []
		self.__debug = debug

	def __repr__(self):
		return "LWW Set\n=======\nADD SET: {}\n\nREMOVE SET: {}\n=======\n".format(self.__add_set, self.__remove_set)

	def _element_in_add_set(self, element, timestamp=None):
		"""Retrieve the element with the timestamps in the add set.

		Keyword arguments:
		timestamp -- retrieve only the element that is added before the given timestamp (default None)
		"""
		if timestamp is None:
			result = [x for x in self.__add_set if x.element == element]
		else:
			result = [x for x in self.__add_set if x.element == element and x.last_timestamp_before(timestamp) is not None]
		if result:
			return result[0]
		return None

	def _element_in_remove_set(self, element, timestamp=None):
		"""Retrieve the element with the timestamps in the remove set.

		Keyword arguments:
		timestamp -- retrieve only the element that is added before the given timestamp (default None)
		"""
		if timestamp is None:
			result = [x for x in self.__remove_set if x.element == element]
		else:
			result = [x for x in self.__remove_set if x.element == element and x.last_timestamp_before(timestamp) is not None]
		if result:
			return result[0]
		return None

	@property
	def _add_set_elements(self):
		"""Retrieve the elements without the timestaps in the add set."""
		return [x.element for x in self.__add_set]

	@property
	def _remove_set_elements(self):
		"""Retrieve the elements without the timestaps in the remove set."""
		return [x.element for x in self.__remove_set]
	

	def exist(self, element, timestamp=None):
		"""Check whether an element exists in the LWW set of not.

		Keyword arguments:
		timestamp -- the given timestamp (default None)"""

		element_in_add_set = self._element_in_add_set(element, timestamp=timestamp)
		element_in_remove_set = self._element_in_remove_set(element, timestamp=timestamp)

		if element_in_add_set is None:
			return False
		if element_in_remove_set is None:
			return True
		if timestamp is None:
			return element_in_remove_set.last_timestamp < element_in_add_set.last_timestamp
		return element_in_remove_set.last_timestamp_before(timestamp) < element_in_add_set.last_timestamp_before(timestamp)

	def get(self, timestamp=None) -> List[__LWW_Element]:
		"""Return a list contianing the elements which should be in the set right before the given timestamp;
		return the most updated state if no timestamp given.

		Keyword argument:
		timestamp -- the given timestamp (default None)
		"""
		return set([x.element for x in self.__add_set if self.exist(x.element, timestamp)])
		
	def add(self, element, with_timestamps=None) -> LWW_Set:
		"""Add element to the set; cannot accept unhashable types.

		Keyword argument:
		with_timestamps -- the timestamps to be associated with the element.
		"""

		if not isinstance(element, Hashable):
			raise TypeError("LWW element set accepts only hashable types.")

		element_in_add_set = self._element_in_add_set(element)
		if element_in_add_set is None:
			self.__add_set.append(__LWW_Element(element, with_timestamps))
		elif with_timestamps is None:
			element_in_add_set.update_timestamp()
		else:
			element_in_add_set.add_timestamps(with_timestamps)
		if self.__debug:
			print(self)
		return self

	def remove(self, element, with_timestamps=None) -> LWW_Set:
		"""Remove element from the set; cannot accept unhashable types.

		Keyword argument:
		with_timestamps -- the timestamps to be associated with the element.
		"""

		element_in_remove_set = self._element_in_remove_set(element)
		if element_in_remove_set is None:
			self.__remove_set.append(__LWW_Element(element, with_timestamps))
		elif with_timestamps is None:
			element_in_remove_set.update_timestamp()
		else:
			element_in_remove_set.add_timestamps(with_timestamps)
		if self.__debug:
			print(self)
		return self

	def merge(self, lww_set_2) -> LWW_Set:
		"""Merge with another LWW set."""

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


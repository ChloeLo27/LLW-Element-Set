""" IMPORT LIBRARIES """
import unittest
from datetime import datetime
from lww_set_class import LWW_Set

class TestLWWSetBasicMethods(unittest.TestCase):

	def setUp(self):
		self.new_set = LWW_Set()
		self.new_set.add("test")

	def test_add_single(self):
		self.assertEqual(self.new_set.get(), set(["test"]))
		self.assertEqual(self.new_set.exist("test"), True)
		self.assertEqual(self.new_set.exist(34), False)

	def test_add_multiple(self):
		self.new_set.add("another")
		self.new_set.add(34)
		self.new_set.add("another")
		self.assertEqual(self.new_set.get(), set(["test", "another", 34]))
		self.assertEqual(self.new_set.exist("test"), True)
		self.assertEqual(self.new_set.exist(34), True)

	def test_hashable(self):
		with self.assertRaises(TypeError):
			self.new_set.add(["item"])

	def test_remove_single(self):
		self.new_set.add("another")
		self.new_set.remove("test")
		self.assertEqual(self.new_set.get(), set(["another"]))

	def test_remove_multiple(self):
		self.new_set.add("another")
		self.new_set.add(34)
		self.new_set.add(12345)
		self.new_set.remove(34)
		self.new_set.remove(12345)
		self.assertEqual(self.new_set.get(), set(["test", "another"]))
		self.assertEqual(self.new_set.exist(34), False)

	def test_remove_nonexistent(self):
		self.new_set.add("another")
		self.new_set.add(34)
		self.new_set.add(12345)
		self.new_set.remove(345)
		self.new_set.remove(123)
		self.assertEqual(self.new_set.get(), set(["test", "another", 34, 12345]))

	def test_remove_and_add(self):
		self.new_set.add("another")
		self.new_set.add(34)
		self.new_set.add(12345)
		self.new_set.remove(34)
		self.new_set.remove(12345)
		self.new_set.add(34)
		self.assertEqual(self.new_set.get(), set(["test", "another", 34]))

	def test_chain_add(self):
		self.new_set.add("another").add("and another")
		self.assertEqual(self.new_set.get(), set(["test", "another", "and another"]))

	def test_chain_remove(self):
		self.new_set.add("another").add(34).add(12345)
		self.new_set.remove(34).remove(12345)
		self.assertEqual(self.new_set.get(), set(["test", "another"]))
		self.assertEqual(self.new_set.exist(34), False)


class TestTimeMachineMethods(unittest.TestCase):

	def setUp(self):
		self.new_set = LWW_Set()

	def test_existence_in_given_time(self):
		self.new_set.add("a")
		self.new_set.add("b")
		self.new_set.add("c")
		retrieval_time = datetime.now()
		self.new_set.add("d")
		self.new_set.add("e")
		self.new_set.add("f")
		self.assertEqual(self.new_set.exist("a", retrieval_time), True)
		self.assertEqual(self.new_set.exist("b", retrieval_time), True)
		self.assertEqual(self.new_set.exist("c", retrieval_time), True)
		self.assertEqual(self.new_set.exist("d", retrieval_time), False)
		self.assertEqual(self.new_set.exist("e", retrieval_time), False)
		self.assertEqual(self.new_set.exist("f", retrieval_time), False)
		self.assertEqual(self.new_set.exist("a"), True)
		self.assertEqual(self.new_set.exist("b"), True)
		self.assertEqual(self.new_set.exist("c"), True)
		self.assertEqual(self.new_set.exist("d"), True)
		self.assertEqual(self.new_set.exist("e"), True)
		self.assertEqual(self.new_set.exist("f"), True)

	def test_retrieval_in_given_time(self):
		self.new_set.add("a")
		self.new_set.add("b")
		self.new_set.add("c")
		retrieval_time = datetime.now()
		self.new_set.add("d")
		self.new_set.add("e")
		self.new_set.add("f")
		self.assertEqual(self.new_set.get(retrieval_time), set(["a", "b", "c"]))
		self.assertEqual(self.new_set.get(), set(["a", "b", "c", "d", "e", "f"]))

	def test_existence_in_given_time_after_remove(self):
		self.new_set.add("a")
		self.new_set.add("b")
		self.new_set.add("c")
		retrieval_time = datetime.now()
		self.new_set.add("d")
		self.new_set.remove("a")
		self.new_set.add("e")
		self.assertEqual(self.new_set.exist("a", retrieval_time), True)
		self.assertEqual(self.new_set.exist("b", retrieval_time), True)
		self.assertEqual(self.new_set.exist("c", retrieval_time), True)
		self.assertEqual(self.new_set.exist("d", retrieval_time), False)
		self.assertEqual(self.new_set.exist("e", retrieval_time), False)
		self.assertEqual(self.new_set.exist("a"), False)
		self.assertEqual(self.new_set.exist("b"), True)
		self.assertEqual(self.new_set.exist("c"), True)
		self.assertEqual(self.new_set.exist("d"), True)
		self.assertEqual(self.new_set.exist("e"), True)

	def test_retrieval_in_given_time_after_removeal(self):
		self.new_set.add("a")
		self.new_set.add("b")
		self.new_set.add("c")
		retrieval_time = datetime.now()
		self.new_set.add("d")
		self.new_set.remove("a")
		self.new_set.add("e")
		self.assertEqual(self.new_set.get(retrieval_time), set(["a", "b", "c"]))
		self.assertEqual(self.new_set.get(), set(["b", "c", "d", "e"]))
		

# merge behavkour
class TestLWWSetMergeBehaviour(unittest.TestCase):

	def setUp(self):
		self.set_1 = LWW_Set()
		self.set_1.add("a")
		self.set_1.add("b")
		self.set_1.add("c")
		self.timestamp_before_first_add = datetime.now()
		self.set_2 = LWW_Set()
		self.set_2.add("c")
		self.set_2.add("d")
		self.set_2.add("e")
		self.timestamp_before_first_remove = datetime.now()
		self.set_2.remove("a")
		self.timestamp_before_second_add = datetime.now()
		self.set_2.add("a")
		self.set_1.merge(self.set_2)

	def test_merge_2_sets(self):
		self.assertEqual(self.set_1.get(), set(["a", "b", "c", "d", "e"]))

	def test_merge_2_sets_with_time(self):
		self.assertEqual(self.set_1.get(self.timestamp_before_first_add), set(["a", "b", "c"]))
		self.assertEqual(self.set_1.get(self.timestamp_before_first_remove), set(["a", "b", "c", "d", "e"]))
		self.assertEqual(self.set_1.get(self.timestamp_before_second_add), set(["b", "c", "d", "e"]))

	def test_merge_convergence(self):
		self.assertEqual(self.set_1.get(), self.set_2.get())

if __name__ == '__main__':
	unittest.main(verbosity=2)
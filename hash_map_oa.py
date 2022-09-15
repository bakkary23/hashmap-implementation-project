# Name: Bashar Akkary
# OSU Email: akkaryb@oregonstat.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/9/22
# Description: This program implements a hash map data structure using open addressing. The main
# HashMap class contains functions to put and remove a key/value pair in the map, clear the map, return the
# load capacity, and return the number of empty buckets. It also contains functions for resizing the map,
# and returning the key/values in a DynamicArray object. Functions for returning the value from a key,
# returning the DynamicArray object the map is based on, and checking whether a key is contained in the
# hashmap are also included.


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the HashMap. If the passed key already exists,
        the passed value will replace the original value. If the key doesn't exist, a new
        key/value pair is inserted.
        """
        if self.table_load() >= 0.5:  # Resizes if necessary
            self.resize_table(self._capacity * 2)
        if self.contains_key(key):  # If the key is present
            index = self._hash_function(key) % self._capacity
            init_index = self._hash_function(key) % self._capacity
            new_entry = HashEntry(key, value)  # Prepares new entry for addition
            j = 0
            while self._buckets.get_at_index(index).key != key or self._buckets.get_at_index(index).is_tombstone:
                index = (init_index + j ** 2) % self._capacity  # Iterates through HashMap
                j += 1
            self._buckets.set_at_index(index, new_entry)
        else:  # If key is not present
            new_entry = HashEntry(key, value)
            index = self._hash_function(key) % self._capacity
            init_index = self._hash_function(key) % self._capacity
            j = 0
            while self._buckets.get_at_index(index) and not self._buckets.get_at_index(index).is_tombstone:
                index = (init_index + j ** 2) % self._capacity  # Iterates through HashMap
                j += 1
            self._buckets.set_at_index(index, new_entry)
            self._size += 1

    def table_load(self) -> float:
        """
        Returns the load capacity of the HashMap object as a floating point value
        """
        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the table as an integer value
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes as a parameter an integer value and resizes the HashMap to have that capacity
        """
        if new_capacity < 1 or new_capacity < self._size:
            return
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)
        data = self.get_keys_and_values()  # Stores key/value pairs in DynamicArray object
        count = self._capacity
        self.clear()
        if new_capacity < self._capacity:  # Adjusts size if new capacity is less than current capacity
            while count > new_capacity:
                self._buckets.pop()
                count -= 1
        else:  # Adjusts size if new capacity is more than current capacity
            while count < new_capacity:
                self._buckets.append(None)
                count += 1
        self._capacity = new_capacity
        for index in range(data.length()):  # Re-puts key/value pairs to resized array
            element = data.get_at_index(index)
            self.put(element[0], element[1])

    def get(self, key: str) -> object:
        """
        Takes as a parameter a key and returns the object associated with that key or returns
        nothing if the key doesn't have an object or doesn't exist
        """
        if not self.get_size():
            return None
        else:
            index = self._hash_function(key) % self._capacity
            init_index = self._hash_function(key) % self._capacity
            j = 0
            while self._buckets.get_at_index(index) and self._buckets.get_at_index(index).key != key:
                index = (init_index + j ** 2) % self._capacity  # Iterates through HashMap
                j += 1
            if self._buckets.get_at_index(index) and not self._buckets.get_at_index(index).is_tombstone:
                value = self._buckets.get_at_index(index).value  # Ensures tombstone is not returned
            else:
                value = None
            return value

    def contains_key(self, key: str) -> bool:
        """
        Returns true if the passed key is in the HashMap and false otherwise
        """
        if not self.get_size():
            return False
        else:
            index = self._hash_function(key) % self._capacity
            init_index = self._hash_function(key) % self._capacity
            j = 0
            while self._buckets.get_at_index(index) and self._buckets.get_at_index(index).key != key:
                index = (init_index + j ** 2) % self._capacity  # Iterates through HashMap
                j += 1
            if self._buckets.get_at_index(index) and not self._buckets.get_at_index(index).is_tombstone:
                return True  # Ensures True is not returned if key is on a tombstone
            else:
                return False

    def remove(self, key: str) -> None:
        """
        Takes as a parameter a key and removes the key and its value from the HashMap
        """
        if self.get_size() == 0:
            return
        else:
            if self.contains_key(key):
                index = self._hash_function(key) % self._capacity
                init_index = self._hash_function(key) % self._capacity
                j = 0
                while (self._buckets.get_at_index(index).key != key
                       or self._buckets.get_at_index(index).is_tombstone) is True:
                    index = (init_index + j ** 2) % self._capacity  # Iterates through HashMap
                    j += 1
                self._buckets.get_at_index(index).is_tombstone = True  # Sets tombstone
                self._size -= 1
            return

    def clear(self) -> None:
        """
        Clears contents of HashTable object without changing the capacity
        """
        for index in range(self._capacity):  # Iterates through DynamicArray storage and sets every value to None
            self._buckets.set_at_index(index, None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a DynamicArray object of tuples for each key, value pair
        in the HashMap object
        """
        arr = DynamicArray()
        if not self._size:
            return arr
        else:
            for index in range(self._capacity):
                if self._buckets.get_at_index(index) and not self._buckets.get_at_index(index).is_tombstone:
                    element = self._buckets.get_at_index(index)  # Ensures tombstone isn't appended
                    arr.append((element.key, element.value))
            return arr


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))
    #
    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

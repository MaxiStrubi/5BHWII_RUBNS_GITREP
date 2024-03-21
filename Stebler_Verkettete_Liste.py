import random


class Node:
    def __init__(self, value=None):
        self.value = value
        self.next_node = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        if not isinstance(value, int):
            raise ValueError("Nur Ganzzahlwerte sind erlaubt.")

        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            current_node = self.head
            # So lange durchgehen bis nächste node null ist
            # z.B Current = 5 und next 3 wenn next leer dann schluss
            while current_node.next_node:
                current_node = current_node.next_node
            # Am Ende nach durchlaufen hinzufügen
            current_node.next_node = new_node

    def length(self):
        count = 0
        for c in self:
            count += 1
        return count

    def display(self):
        elements = []
        for node_value in self:
            elements.append(node_value)
        print("Liste:", elements)

    # um List durch zugehen
    def __iter__(self):
        self._current = self.head
        return self

    def __next__(self):
        if self._current is None:
            raise StopIteration
        value = self._current.value
        self._current = self._current.next_node
        return value


if __name__ == '__main__':
    my_list = LinkedList()

    for X in range(19):
        my_list.append(random.randint(1, 100))

    my_list.display()
    print("Länge der Liste:", my_list.length())

    print("Elemente der Liste über Iterator:")
    for element in my_list:
        print(element)

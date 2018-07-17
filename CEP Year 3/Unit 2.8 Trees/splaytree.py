from splaynode import SplayNode
import gc

class SplayBST:
    '''
    Binary splay tree, where a node is splayed to the top of the tree when it is added to the tree or accessed
    through a binary search. When a node is deleted, the parent of the deleted node is splayed instead.

    Keeping the more frequently accessed nodes near the top of the tree allows for extremely fast access speeds
    when accessing the same few nodes over and over, resulting in possibly O(1) search time complexity.

    Nodes are created with key-value pairs, the value being returned when a node with the corresponding key is found.
    While duplicate key are not allowed, the value of an existing key can be overwritten with a new value.

    To reduce the memory burden that the linked nodes cause, the class instructs Python to only use a static amount
    of memory for our fixed number of variables, reducing RAM usage drastically
    '''

    #allocate static amount of memory to variables instead of a dynamic dictionary
    #this can reduce up to 40% of RAM
    __slots__ = ('root', 'length')

    def __init__(self, key, value):
        '''
        Initializes root node with the given key and value, and starts the length of the tree at 1

        Time complexity: O(1)

        E.g:
        >>> a = SplayBST(1, 2)
        >>> print(a.root)
        (1, 2)
        >>> print(a.length)
        1
        '''
        assert value is not None, "Value cannot be None"
        self.root = Node(key, value)
        self.length = 1

    def __len__(self):
        '''
        Returns length of tree when len() is called

        Time complexity: O(1)

        E.g:
        >>> a = SplayBST(1, 2)
        >>> print(len(a))
        1
        '''
        return self.length

    def __str__(self):
        '''
        Returns string of all nodes in pre-order

        Time complexity: O(1)

        E.g:
        >>> a = SplayBST(1, 2)
        >>> a.add(2, 1)
        >>> a.add(1.5, 3)
        >>> print(a)
        [(1.5, 3), (1, 2), (2, 1)]
        '''
        string = '['
        for i in self._preOrderGen(self.root): string += str(i) + ", "
        return string[:-2] + ']'

    def __iter__(self):
        '''
        Iterates through list of tuples of the key-value pairs of all nodes in ascending order

        Time complexity: O(n^2)

        E.g:
        >>> a = SplayBST(1, 2)
        >>> a.add(2, 1)
        >>> a.add(1.5, 3)
        >>> for i in a:
        >>>     print(i)
        (1, 2)
        (1.5, 3)
        (2, 1)
        '''
        return iter(self._inOrderGen(self.root))

    def __reversed__(self):
        '''
        Returns a list of tuples of the key-value pairs of all nodes in descending order

        Time complexity: O(n)

        >>> a = SplayBST(1, 2)
        >>> a.add(2, 1)
        >>> a.add(1.5, 3)
        >>> b = reversed(a)
        >>> print(b)
        [(2, 1), (1.5, 3), (1, 2)]
        >>> print(type(b))
        list
        '''
        return self._inOrderReverse(self.root)

    def __contains__(self, key):
        '''
        Returns whether key is present in the splay tree

        Time complexity(Average): O(log n)
        Time complexity(Amortized): O(log n)
        Time complexity(Worst-case): O(n)

        E.g:
        >>> a = SplayBST(1, 2)
        >>> print(1 in a)
        True
        >>> print(2 in a)
        False
        '''
        return self.search(key) is not None

    def __setitem__(key, value):
        '''Same as self.add(key, value):''' + self.add.__doc__
        return self.add(key, value)

    def __getitem__(self, key):
        '''Same as self.search(key, value):''' + self.search.__doc__
        return self.search(key)

    def __delitem__(key):
        '''Same as self.delete(key, value):''' + self.delete.__doc__
        return self.delete(key)

    __repr__ = __str__

    def add(self, key, value):
        '''
        Adds a node with the given key and value to the tree and splays it to the top of the tree

        Time complexity(Average): O(log n)
        Time complexity(Amortized): O(log n)
        Time complexity(Worst-case): O(n)

        >>> a = SplayBST(1, 2)
        >>> a.add(2, 3)
        >>> print(a)
        [(2, 3), (1, 2)]
        >>> a.add(1.5, 0)
        [(1.5, 0), (1, 2), (2, 3)]
        '''
        assert value is not None, "Value cannot be None"
        b = self.addNode(self.root, key, value)
        self.root = self.splayNode(self.root, b)

    def search(self, key):
        '''
        Searches for the node with the given key and returns its corresponding value
        If the node does not exist, None is returned. If it does exist, it is splayed to the top of the tree

        Time complexity(Average): O(log n)
        Time complexity(Amortized): O(log n)
        Time complexity(Worst-case): O(n)

        >>> a = SplayBST(1, 2)
        >>> print(a.search(1))
        2
        >>> print(a.search(2))
        None

        '''
        node = self.searchNode(self.root, key)
        self.root = self.splayNode(self.root, node)
        return node.val

    def delete(self, key, pop=False):
        '''
        Searches for the node and removes it from the tree. If pop is set as True, the value of the node is also returned.
        If the node is not present in the tree and pop is True however, None is returned.
        Then, the parent of the deleted node is splayed to the top of the tree.

        Time complexity(Average): O(log n)
        Time complexity(Amortized): O(log n)
        Time complexity(Worst-case): O(n)

        >>> a = SplayBST(1, 2)
        >>> a.add(2, 3)
        >>> a.add(1.5, 0)
        >>> print(a)
        [(1.5, 0), (1, 2), (2, 3)]
        >>> a.delete(1.5)
        >>> print(a)
        [(2, 3), (1, 2)]
        >>> print(a.delete(1, pop=True))
        2
        '''
        deleted = self.delNode(self.root, key)
        self.root = self.splayNode(self.root, deleted[0])
        if pop: return deleted[1]

    def addNode(self, root, key, value):
        '''
        Function that inserts a new node into the tree if a new key is specified, and updates value if an existing key is given

        The position is determined by the key (left if it is less than a node, right if it is more than a node)
        '''
        def _insert(root, node):
            #updates value if new value is given
            if root.key == node.key:
                root.val = node.val
                return root
            #when key is more than node's key, inserts node if right of node is empty, continues moving right otherwise
            else:
                if root.key < node.key:
                    if root.right is None: root.right = node
                    else: return _insert(root.right, node)
            #when key is less than node's key, inserts node if left of node is empty, continues moving left otherwise
                if root.key > node.key:
                    if root.left is None: root.left = node
                    else: return _insert(root.left, node)
                self.length += 1
            #return newly inserted node to be splayed later on
            return node
        return _insert(root, Node(key, value))

    def searchNode(self, root, key):
        '''
        Function that binary searches for the node with the given key based on the key's value

        If the key cannot be found, None is returned
        '''
        def _search(root, key):
            #if node's key matches given key, the node is found and returned
            if root.key == key: return root
            #if they do not match, search continues right if the key is more than node's key
            if root.key < key and root.right is not None: return _search(root.right, key)
            #if they do not match, search continues left if the key is less than node's key
            if root.key > key and root.left is not None: return _search(root.left, key)
            #if the search cannot proceed left/right, it is assumed the node does not exist, and None is returned
            return None
        return _search(root, key)

    def delNode(self, root, key):
        '''
        Function that deletes node, clears the memory it takes up, and replaces it with a successor

        If the key cannot be found, (None, None) is returned
        '''
        def _findMinNode(node):
            #keeps moving left until it finds the leftmost node
            if node.left is not None: return _findMinNode(node.left)
            else: return node
        def _replace(node):
            #finds node with key closest to given node (leftmost of right node)
            successor = _findMinNode(node.right)
            #subs in new key-value
            node.key, node.val = successor.key, successor.val
            #adds 1 since the length will be subtracted by 1 later
            self.length += 1
            #removes successor
            _delete(successor)
        def _delete(node):
            #does not bother if node was not found
            if node is not None:
                #stores parent and value to return later
                parent = self._parent(self.root, node.key)
                value = node.val
                #replaces node with its child if it has 0/1 child and is not root
                if (node.left is None or node.right is None) and parent is not None:
                    if parent.left == node: parent.left = node.left or node.right
                    else: parent.right = node.right or node.right
                    del node
                #replaces node with child if it has 0/1 children and is root
                elif (node.left is None or node.right is None):
                    successor = node.left or node.right
                    node.key, node.val, node.left, node.right = successor.key, successor.val, successor.left, successor.right
                    parent = node
                    del successor
                #replaces node with leftmost of right child if it has 2 children
                else: _replace(node)
                #updates length and returns parent and value
                self.length -= 1
                return parent, value
            return None, None
        #garbage collects 'deleted' nodes
        gc.collect()
        return _delete(self.searchNode(root, key))

    def splayNode(self, root, node):
        '''
        Function that splays the node up the tree until it becomes root while maintaining the priority and order of previously splayed nodes
        '''
        #right rotation(zig)
        def _zig(node, parent, grandnode=None):
            parent.left = node.right
            node.right = parent
            if grandnode is not None:
                if grandnode.left == parent: grandnode.left = node
                if grandnode.right == parent: grandnode.right = node
        #left rotation(zag)
        def _zag(node, parent, grandnode=None):
            parent.right = node.left
            node.left = parent
            if grandnode is not None:
                if grandnode.left == parent: grandnode.left = node
                if grandnode.right == parent: grandnode.right = node
        #no need to splay if node is already root
        if root == node or node == None: return root
        #if node is left child of root, a right rotation (or zig) is performed
        if root.left == node:
            _zig(node, root)
            return node
        #if node is right child of root, a left rotation (or zag) is performed
        if root.right == node:
            _zag(node, root)
            return node
        if root.left is not None:
        #if node is left-left grandchild of root, a zig needs to be performed between the parent and grandparent to maintain order
        #this makes the step zig-zig
            if root.left.left == node:
                temp = root.left
                _zig(root.left, root)
                _zig(node, temp)
                return node
        #if node is left-right grandchild of root, the node needs to zag up(while maintaining a connection to root), and then zig up
        #this step is called zig-zag
            elif root.left.right == node:
                _zag(node, root.left, grandnode=root)
                _zig(node, root)
                return node
        #mirrorred version of zig zig (it's now zag zag)
        if root.right is not None:
            if root.right.right == node:
                temp = root.right
                _zag(root.right, root)
                _zag(node, temp)
                return node
        #mirrored version of zig-zag(zag-zig)
            elif root.right.left == node:
                _zig(node, root.right, grandnode=root)
                _zag(node, root)
                return node
        #if the grandparent of the node is not root, the grandparent and great-grandparent are searched
        #with some steps to make sure the program does not spit out ugly errors when the parent is not found
        p = self._parent(self.root, node.key)
        if p is not None: gp = self._parent(self.root, p.key)
        else: return None
        if gp is not None: gpp = self._parent(self.root, gp.key)
        else: return None
        #moves the node up by two levels based on our 4 cases
        if gp.left is not None:
        #zig-zig
            if gp.left.left == node:
                temp = gp.left
                _zig(gp.left, gp, grandnode=gpp)
                _zig(node, temp, grandnode=gpp)
        #zig-zag
            elif gp.left.right == node:
                _zag(node, gp.left, grandnode=gp)
                _zig(node, gp, grandnode=gpp)
        #zag-zag
        if gp.right is not None:
            if gp.right.right == node:
                temp = gp.right
                _zag(gp.right, gp, grandnode=gpp)
                _zag(node, temp, grandnode=gpp)
        #zag-zig
            elif gp.right.left == node:
                _zig(node, gp.right, grandnode=gp)
                _zag(node, gp, grandnode=gpp)

        #loops splay operation until node is root
        return self.splayNode(root, node)

    def _parent(self, root, key):
        '''
        Returns parent of node with given key
        If parent is not found, None is returned
        '''
        if root.left is not None:
            if root.left.key == key: return root
            elif root.key > key: return self._parent(root.left, key)
        if root.right is not None:
            if root.right.key == key: return root
            elif root.key < key: return self._parent(root.right, key)
        return None

    def _inOrderGen(self, root):
        '''Returns inorder generator of all nodes'''
        if root.left:
            for node in self._inOrderGen(root.left):
                yield node
        yield root
        if root.right:
            for node in self._inOrderGen(root.right):
                yield node

    def _inOrderReverseGen(self, root):
        '''Returns reverse inorder generator of all nodes'''
        if root.right:
            for node in self._inOrderReverseGen(root.right):
                yield node
        yield root
        if root.left:
            for node in self._inOrderReverseGen(root.left):
                yield node

    def _preOrderGen(self, root):
        '''Returns preorder generator of all nodes'''
        yield root
        if root.left:
            for node in self._preOrderGen(root.left):
                yield node
        if root.right:
            for node in self._preOrderGen(root.right):
                yield node

    def _postOrderGen(self, root):
        '''Returns postorder generator of all nodes'''
        if root.left:
            for node in self._postOrderGen(root.left):
                yield node
        if root.right:
            for node in self._postOrderGen(root.right):
                yield node
        yield root

    def _levelOrderGen(self, root, start=0):
        '''Returns levelorder generator of all nodes'''
        if start == 0: yield root
        if root.left: yield root.left
        if root.right: yield root.right
        if root.left:
            for node in self._levelOrderGen(root.left, start=1):
                yield node
        if root.right:
            for node in self._levelOrderGen(root.right, start=1):
                yield node

    def inOrder(self):
        '''Returns inorder list of all nodes'''
        return list(self._inOrderGen(self.root))

    def inOrderReverse(self):
        '''Returns reverse inorder list of all nodes'''
        return list(self._inOrderReverseGen(self.root))

    def preOrder(self):
        '''Returns preorder list of all nodes'''
        return list(self._preOrderGen(self.root))

    def postOrder(self):
        '''Returns postorder list of all nodes'''
        return list(self._postOrderGen(self.root))

    def levelOrder(self):
        '''Returns levelorder list of all nodes'''
        return list(self._levelOrderGen(self.root))

a = SplayBST(1, 2)
print(a)
print(len(a))
a.add(2, 3)
print(a)
print(len(a))
a.add(1.5, 0)
print(a)
print(len(a))
a.add(10, 2342)
print(a)
print(len(a))
a.add(0.1, 3294)
print(a)
print(len(a))
a.add(11, 132)
print(a)
print(len(a))
a.add(12, 132)
print(a)
print(len(a))
a.add(101923, 1392)
print(a)
print(len(a))
print(a.delete(11, pop=True))
print(a)
print(len(a))
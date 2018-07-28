from splaynode import Node
from dyarray import DyArray

class SplayBST:
    '''
    Binary splay tree, where a node is splayed to the top of the tree when it is added to the tree or accessed
    through a binary search. When a node is deleted, the parent of the deleted node is splayed instead.

    Keeping the more frequently accessed nodes near the top of the tree allows for extremely fast access speeds
    when accessing the same few nodes over and over, resulting in possibly O(1) search time complexity.

    Nodes are created with key-value pairs, the value being returned when a node with the corresponding key is found.
    While duplicate keys are not allowed, the value of an existing key can be overwritten with a new value.

    To reduce the memory burden that the linked nodes cause, the class instructs Python to only use a static amount
    of memory for our fixed number of variables, reducing RAM usage drastically
    '''

    #allocate static amount of memory to variables instead of a dynamic dictionary
    #this can reduce up to 40% of RAM
    __slots__ = ('root', 'length')

    def __init__(self, key=None, value=None):
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
        if key:
            self.root = Node(key, value)
            self.length = 1
        else:
            self.root = None
            self.length = 0

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

        Time complexity: O(n)

        E.g:
        >>> a = SplayBST(1, 2)
        >>> a.add(2, 1)
        >>> a.add(1.5, 3)
        >>> print(a)
        [(1.5, 3), (1, 2), (2, 1)]
        '''
        string = ''
        for i in self._preOrderGen(self.root): string += str(i) + ", "
        return '[' + string[:-2] + ']'

    def __iter__(self):
        '''
        Iterates through list of all nodes in ascending order

        Time complexity: O(n)

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
        Returns a list of all nodes in descending order

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
        Time complexity(Worst-case): O(n)

        >>> a = SplayBST(1, 2)
        >>> a.add(2, 3)
        >>> print(a)
        [(2, 3), (1, 2)]
        >>> a.add(1.5, 0)
        [(1.5, 0), (1, 2), (2, 3)]
        '''
        assert key is not None, "Key cannot be None"
        if self.length > 0: self.root = self._splayNode(self.root, self._addNode(self.root, key, value))
        else:
            self.root = Node(key, value)
            self.length = 1

    def search(self, key):
        '''
        Searches for the node with the given key and returns its corresponding value
        If the node does not exist, None is returned. If it does exist, it is splayed to the top of the tree

        Time complexity(Average): O(log n)
        Time complexity(Worst-case): O(n)

        >>> a = SplayBST(1, 2)
        >>> print(a.search(1))
        2
        >>> print(a.search(2))
        None

        '''
        assert key is not None, "Key cannot be None"
        node = self._searchNode(self.root, key)
        self.root = self._splayNode(self.root, node)
        return node.val if node else None

    def delete(self, key, pop=False):
        '''
        Searches for the node and removes it from the tree. If pop is set as True, the value of the node is also returned.
        If the node is not present in the tree and pop is True however, None is returned.
        Then, the parent of the deleted node is splayed to the top of the tree.

        Time complexity(Average): O(log n)
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
        self.root = self._splayNode(self.root, self._searchNode(self.root, key))
        if pop: value = self.root.val
        self.root = self._delNode(self.root, key)
        if pop: return value

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

    def _addNode(self, root, key, value):
        '''
        Function that inserts a new node into the tree if a new key is specified, and updates value if an existing key is given
        The position is determined by the key (left if it is less than a node, right if it is more than a node)
        '''
        def _insert(root, node):
            #updates value if new value is given
            if root.key == node.key:
                if type(root.val) is not DyArray:
                    temp = root.val
                    root.val = DyArray(1)
                    root.val[0] = temp
                root.val.append(node.val)
                return root
            #when key is more than node's key, inserts node if right of node is empty, continues moving right otherwise
            if root.key < node.key:
                if root.right is None: root.right = node
                else: return _insert(root.right, node)
                #when key is less than node's key, inserts node if left of node is empty, continues moving left otherwise
            else:
                if root.left is None: root.left = node
                else: return _insert(root.left, node)
            self.length += 1
            #return newly inserted node to be splayed later on
            return node
        return _insert(root, Node(key, value))

    def _searchNode(self, root, key):
        '''
        Function that binary searches for the node with the given key based on the key's value
        If the key cannot be found, None is returned
        '''
        def _search(root, key):
            if root:
                #if node's key matches given key, the node is found and returned
                if root.key == key: return root
                #if they do not match, search continues right if the key is more than node's key (left if less than)
                if root.key < key: return _search(root.right, key)
                if root.key > key: return _search(root.left, key)
            #if the search cannot proceed left/right, it is assumed the node does not exist, and nothing(or None) is returned
        return _search(root, key)

    def _delNode(self, root, key):
        '''
        Function that deletes node, clears the memory it takes up, and replaces it with a successor
        If the key cannot be found, (None, None) is returned
        '''
        def _findMinNode(node):
            #keeps moving left until it finds the leftmost node
            return _findMinNode(node.left) if node.left else node
        def _delete(root, key):
            #if keys do not match, it shows the splay was unsuccessful, meaning the key was not found
            if key != root.key:
                return root
            #if the root has no right node, the left node can replace it as the new root
            if root.right is None:
                temp = root
                root = root.left
            # if it does have a right node, the minimum of its right node is splayed, and then its position is replaced by its left node
            else:
                temp = root
                root = self._splayNode(root, _findMinNode(root.right))
                root.left = temp.left
            #memory is freed to be garbage collected later
            del temp
            self.length -= 1
            return root
        if root: return _delete(root, key)

    def _splayNode(self, root, node):
        '''
        Function that splays the node up the tree until it becomes root while maintaining the priority and order of previously splayed nodes
        '''
        #right rotation(zig)
        def _zig(node, parent, grandnode=None):
            parent.left = node.right
            node.right = parent
            if grandnode:
                if grandnode.left == parent: grandnode.left = node
                if grandnode.right == parent: grandnode.right = node
        #left rotation(zag)
        def _zag(node, parent, grandnode=None):
            parent.right = node.left
            node.left = parent
            if grandnode:
                if grandnode.left == parent: grandnode.left = node
                if grandnode.right == parent: grandnode.right = node
        #no need to splay if node is already root
        if root == node or node is None or root is None: return root
        #if node is left child of root, a right rotation (or zig) is performed
        if root.left == node:
            _zig(node, root)
            return node
        #if node is right child of root, a left rotation (or zag) is performed
        if root.right == node:
            _zag(node, root)
            return node
        if root.left:
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
        if root.right:
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
        if p: gp = self._parent(self.root, p.key)
        else: return None
        if gp: gpp = self._parent(self.root, gp.key)
        else: return None
        #moves the node up by two levels based on our 4 cases
        if gp.left:
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
        if gp.right:
            if gp.right.right == node:
                temp = gp.right
                _zag(gp.right, gp, grandnode=gpp)
                _zag(node, temp, grandnode=gpp)
        #zag-zig
            elif gp.right.left == node:
                _zig(node, gp.right, grandnode=gp)
                _zag(node, gp, grandnode=gpp)

        #loops splay operation until node is root
        return self._splayNode(root, node)

    def _parent(self, root, key):
        '''
        Returns parent of node with given key
        If parent is not found, None is returned
        '''
        if key:
            if root.left:
                if root.left.key == key: return root
                elif root.key > key: return self._parent(root.left, key)
            if root.right:
                if root.right.key == key: return root
                elif root.key < key: return self._parent(root.right, key)

    def _inOrderGen(self, root):
        '''Returns inorder generator of all nodes'''
        if root:
            for node in self._inOrderGen(root.left): yield node
            yield root
            for node in self._inOrderGen(root.right): yield node

    def _inOrderReverseGen(self, root):
        '''Returns reverse inorder generator of all nodes'''
        if root:
            for node in self._inOrderReverseGen(root.right): yield node
            yield root
            for node in self._inOrderReverseGen(root.left): yield node

    def _preOrderGen(self, root):
        '''Returns preorder generator of all nodes'''
        if root:
            yield root
            for node in self._inOrderReverseGen(root.right): yield node
            for node in self._inOrderReverseGen(root.left): yield node

    def _postOrderGen(self, root):
        '''Returns postorder generator of all nodes'''
        if root:
            for node in self._inOrderReverseGen(root.right): yield node
            for node in self._inOrderReverseGen(root.left): yield node
            yield root

    def _levelOrderGen(self, root, start=0):
        '''Returns levelorder generator of all nodes'''
        if start == 0: yield (root, start)
        if root:
            if root.left: yield (root.left, start+1)
            if root.right: yield (root.right, start+1)
            for node in self._levelOrderGen(root.left, start=start+1): yield node
            for node in self._levelOrderGen(root.right, start=start+1): yield node

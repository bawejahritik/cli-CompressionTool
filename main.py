class Node:
    def __init__(self, data = None) -> None:
        self.left = None
        self.right = None
        self.val = data

def frequencies(text: str):
    freq = {}
    for c in text:
        freq[c] = 1 + freq.get(c, 0)

    freq = sorted(freq.items(), key=lambda x:x[1])
    return freq

def create_huffman_tree(f):
    while len(f) > 1:
        root = Node()
        node1 = f[0]
        node2 = f[1]

        f = f[2:]

        root.val = node1[1] + node2[1]
        root.left = node1[0]
        root.right = node2[0]

        f.append((root, root.val))
        f = sorted(f, key=lambda x:x[1])

    return f[0][0]

def build_huffman_table(root, path):
    
    if type(root) is str:
        # print(f'{root} -> {path}')
        return {root: path}
    
    binary_table = {}

    binary_table.update(build_huffman_table(root.left, path + '0'))
    # print(root.val)
    binary_table.update(build_huffman_table(root.right, path + '1'))
    
    return binary_table

def build_huffman_tree(binary_table):
    root = Node()

    for key, value in binary_table:
        node = root
        for v in value:
            if v == '0':
                if not node.left:
                    node.left = Node()
                node = node.left
            else:
                if not node.right:
                    node.right = Node()
                node = node.right
            
        node.val = key
    
    return root


text = "c" * 32
text += ("d" * 42)
text += ("e" * 120)
text += ("k" * 7)
text += ("l" * 42)
text += ("m" * 24)
text += ("u" * 37)
text += ("z" * 2)

def compression(text):
    freq = frequencies(text)
    root = create_huffman_tree(freq)

    binary_table = build_huffman_table(root, '')

    res = ""

    for c in text:
        res += binary_table[c]

    print(len(res))
    msg_len = len(res)
    res = int(res, 2).to_bytes((len(res) + 7)//8, byteorder='big')
    print(len(res))
    return res, binary_table, msg_len

# {'e': '0', 'u': '100', 'd': '101', 'l': '110', 'c': '1110', 'z': '111100', 'k': '111101', 'm': '11111'}

def decompression(compressed, binary_table, msg_len):
    res = ''
    compressed = str(bin(int(compressed.hex(), 16))).replace('0b', '')
    if len(compressed) != msg_len:
        compressed = (msg_len-len(compressed))*'0' + compressed
    
    root = build_huffman_tree(binary_table)

    current = root

    for i in range(msg_len):
        if compressed[i] == '0':
            current = current.left
        elif compressed[i] == '1':
            current = current.right
        
        if not current.left and not current.right:
            res += current.val
            current = root

    print(res)

compressed, binary_table, msg_len = compression(text)
binary_table = sorted(binary_table.items(), key=lambda x:x[1])
print(binary_table)

decompression(compressed, binary_table, msg_len)
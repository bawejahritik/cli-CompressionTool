import click
import sys

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


def compression(text):
    freq = frequencies(text)
    root = create_huffman_tree(freq)

    binary_table = build_huffman_table(root, '')

    res = ""

    for c in text:
        res += binary_table[c]
    msg_len = len(res)
    res = int(res, 2).to_bytes((len(res) + 7)//8, byteorder='big')
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
    return res

# compressed, binary_table, msg_len = compression(text)
# binary_table = sorted(binary_table.items(), key=lambda x:x[1])
# print(binary_table)

# decompression(compressed, binary_table, msg_len)

@click.command()
@click.argument('filename', nargs=-1, type=click.Path(exists=True))
@click.option('-e', '--encode', 'encode', is_flag=True, help="To Compress the file")
@click.option('-d', '--decode', 'decode', is_flag=True, help="To Decompress the file")
def main(filename, encode, decode):
    if not filename:
        sys.stdout.write("Please provide the file to compress/decompress")
        exit(1)

    if encode:
        lines = ""
        with open(filename[0], "r", encoding="utf-8") as f:
            data = f.readlines()
            for line in data:
                lines += line
        
        compressed, binary_table, msg_len = compression(lines)
        binary_table = sorted(binary_table.items(), key=lambda x:x[1])

        with open(filename[0]+".compressed", "wb") as f1:
            f1.write(str(binary_table).encode())
            f1.write(b'\n')
            f1.write(str(msg_len).encode())
            f1.write(b'\n')
            f1.write(compressed)
            
    
    if decode:
        with open(filename[0], 'rb') as file:
            binary_table = eval(file.readline().decode())
            msg_len = int(file.readline().decode())
            compressed = file.read()
            # compressed = str(bin(int(compressed.hex(), 16))).replace('0b', '')
            decompressed = decompression(compressed, binary_table, msg_len)
            print("decom", decompressed)
            with open(filename[0][:-11] + ".decompressed", 'w') as file:
                file.write(decompressed)

if __name__ == '__main__':
    main()
import sys

file = path1 = sys.argv[1]
if __name__ == '__main__':
    l = []
    with open(file, 'r') as f:
        for i in f:
            l.append(i)
    s = set(l)
    with open(file, 'w') as f:
        for i in s:
            f.write(i)

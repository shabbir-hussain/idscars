import sys

log_file = open(sys.argv[1])

data = []
for line in log_file:
    line = line.rstrip('\n')
    data.append([item for item in line.split(" ")])

log_file.close()

keys = [[item.rstrip(':') for item in line[1::2]] for line in data]
values = [line[2::2] for line in data]

list_of_dict = []
for k, z in zip(keys, values):
    list_of_dict.append(dict(zip(k, z)))

print list_of_dict[:5]

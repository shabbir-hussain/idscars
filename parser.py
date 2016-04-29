#parses a trace and gives a dictionary output
def parseTrace(log_file):
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

    return list_of_dict

if(__name__=='__main__'):

    import sys

    log_file = open(sys.argv[1])
    list_of_dict = parseTrace(log_file)
    print list_of_dict[:5]

#Example output
#[{'': 'forward:0', 'Sensor': '1', 'ID': '3', 'Time': '1085511168'}, {'': 'forward:0', 'Sensor': '2', 'ID': '3', 'Time': '1087057152'}, {'': 'forward:0', 'Sensor': '3', 'ID': '3', 'Time': '1087784832'}, {'': 'forward:0', 'Sensor': '4', 'ID': '3', 'Time': '1087964032'}, {'': 'forward:0', 'Sensor': '5', 'ID': '3', 'Time': '1088436160'}]


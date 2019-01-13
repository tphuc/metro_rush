def parseLineStations(file):
    metrodict = {}
    status = {}
    n = 0
    color = None
    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                if line.startswith('#'):
                    metrodict.setdefault(line[1:], [])
                    color = line[1:]
                elif line[0].isdigit():
                    metrodict[color].append(line[line.find(':')+1:])
                elif line.startswith("START"):
                    status.setdefault('START', line[line.find('=')+1:].split(':'))
                elif line.startswith("END"):
                    status.setdefault('END', line[line.find('=')+1:].split(':'))
                elif line.startswith("TRAINS"):
                    n = int(line[line.find('=')+1:])
    return metrodict, status, n

def parseLocationStations(file):
    dic = {}
    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                if line.startswith('#'):
                    color = line[1:]
                    dic.setdefault(color, [])
                else:
                    ls = line.split(',')
                    dic[color].append((int(ls[-2]), int(ls[-1])))
    return dic



if __name__ == '__main__':
    print(parseLineStations('delhi-metro-stations'))
    print(parseLocationStations('stations.csv'))

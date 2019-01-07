def parseLineStations(file):
    metrodict = {}
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
    return metrodict



if __name__ == '__main__':
    print(parseLineStations('delhi-metro-stations'))
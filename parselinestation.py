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
                    status.setdefault('START', line[6:].split(':'))
                elif line.startswith("END"):
                    status.setdefault('END', line[4:].split(':'))
                elif line.startswith("TRAINS"):
                    n = int(line[7:])
    return metrodict, status, n

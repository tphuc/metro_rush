from parseline import parseLineStations


def main():
    for k,v in parseLineStations('delhi-metro-stations').items():
        print(k+'--------------------')
        for i in v:
            print(i)
    pass

if __name__ == "__main__":
    main()
    pass
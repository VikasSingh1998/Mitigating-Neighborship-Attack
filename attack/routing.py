def printRoutingTable(table):
    print('Routing Table')
    print('--------------------------------')
    print('|     NAME   | ADDRESS | HOPS')
    print('--------------------------------')
    for row in table:
        print('|   ',row[0],'|',row[1],'     |',row[2])
    print('--------------------------------')
def compareReports(oldRep, newRep):
    print("Comparing raports...")
    commonFailures = []
    failureIndex = 0
    for x in range(len(oldRep) - 1):
        for y in range(len(newRep) - 1):
            if (oldRep[x][0] == newRep[y][0] and oldRep[x][2] == newRep[y][2]):
                print('Fails in old raport: ' +
                      str(len(oldRep[x]) - 4) + '\nFails in new raport: ' + str(len(newRep[y]) - 4))
                howManySameFailuresNeeded = len(oldRep[x]) - 4
                for z in range(4, len(oldRep[x])):
                    print("index: " + str(z - 3))
                    try:
                        if(oldRep[x][z] == newRep[y][z]):
                            print(
                                str(oldRep[x][0]) + " has the same failure #" + str(z - 3))
                            howManySameFailuresNeeded -= 1
                        elif(oldRep[x][z] == newRep[y][z + 1] or oldRep[x][z] == newRep[y][z - 1]):
                            print("This error has switched places: " +
                                  oldRep[x][z])
                            howManySameFailuresNeeded -= 1
                        else:
                            print("These are not the same:\n" +
                                  oldRep[x][z] + "\nand: \n" + newRep[y][z])
                    except Exception as e:
                        print(e)
                        print('Jest error,hehe jedziemy')
                        pass
                print(str(howManySameFailuresNeeded) +
                      " fail(s) is not the same!")
                if howManySameFailuresNeeded == 0:
                    commonFailures.insert(
                        failureIndex, ([oldRep[x][0], oldRep[x][1]]))
                    failureIndex += 1
    seen = set()
    newlist = []
    for item in commonFailures:
        t = tuple(item)
        if t not in seen:
            newlist.append(item)
            seen.add(t)
    return newlist

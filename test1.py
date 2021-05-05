for i in range(0, 1000000000):
    with open('log22.txt', 'a') as f:
        f.write("{}\n".format(i))
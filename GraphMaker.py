import matplotlib.pyplot as plt


class GraphMaker:

    def __init__(self):
        print("Initialized graph_maker!");

    def makeGraph(self):
        # x axis values
        x = [1, 2, 3]
        # corresponding y axis values
        y = [2, 4, 1]
        # plotting the points
        plt.plot(x, y)
        # naming the x axis
        plt.xlabel('x - axis')
        # naming the y axis
        plt.ylabel('y - axis')
        # giving a title to my graph
        plt.title('My first graph!')
        # function to show the plot
        # plt.show()
        print("testing")
        time.sleep(4)
        print("Testing! again")
        plt.savefig('demo.png', bbox_inches='tight')
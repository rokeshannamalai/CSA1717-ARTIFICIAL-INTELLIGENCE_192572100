import heapq

graph = {
    'A': [('B',2),('C',4)],
    'B': [('A',2),('C',3),('D',7),('E',2)],
    'C': [('A',4),('B',3),('E',3)],
    'D': [('B',7),('E',2),('G',2)],
    'E': [('B',2),('C',3),('D',2)],
    'G': []
}

heuristic = {
    'A':7,
    'B':6,
    'C':4,
    'D':3,
    'E':2,
    'G':0
}

def a_star(start, goal):

    open_list = []
    heapq.heappush(open_list,(heuristic[start],0,start,[start]))

    closed = []
    iteration = 1

    while open_list:

        f,g,node,path = heapq.heappop(open_list)

        if node in closed:
            continue

        print("\n======================================")
        print("Iteration :",iteration)
        print("Current Node :",node)

        print("Open List :",[(n,fc) for fc,gc,n,p in open_list])
        print("Closed List :",closed)

        print("g(n) =",g)
        print("h(n) =",heuristic[node])
        print("f(n) =",f)

        if node==goal:

            print("\nGoal Reached")
            print("Optimal Path :"," -> ".join(path))
            print("Total Cost :",g)
            return

        closed.append(node)

        for neighbour,cost in graph[node]:

            if neighbour not in closed:

                new_g=g+cost
                new_f=new_g+heuristic[neighbour]

                heapq.heappush(open_list,(new_f,new_g,neighbour,path+[neighbour]))

        iteration+=1


while True:

    start=input("\nEnter Start Node : ").upper()
    goal=input("Enter Goal Node : ").upper()

    a_star(start,goal)

    ch=input("\nSearch Again?(y/n): ")

    if ch.lower()!='y':
        break

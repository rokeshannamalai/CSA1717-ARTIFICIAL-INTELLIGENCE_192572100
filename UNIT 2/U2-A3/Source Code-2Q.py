import math

while True:

    print("\nEnter the leaf node values")

    l1=int(input("Leaf 1 : "))
    l2=int(input("Leaf 2 : "))
    l3=int(input("Leaf 3 : "))
    r1=int(input("Leaf 4 : "))
    r2=int(input("Leaf 5 : "))
    r3=int(input("Leaf 6 : "))

    tree=[[l1,l2,l3],[r1,r2,r3]]

    alpha=-math.inf

    values=[]

    iteration=1

    for i in range(2):

        beta=math.inf
        minimum=math.inf

        print("\n====================================")
        print("Iteration :",iteration)
        print("MIN Node",i+1)

        for j in range(3):

            value=tree[i][j]

            print("\nEvaluating :",value)

            minimum=min(minimum,value)
            beta=min(beta,minimum)

            print("Alpha =",alpha)
            print("Beta =",beta)

            if beta<=alpha:

                print("Pruned Nodes :",tree[i][j+1:])
                break

        print("Selected Value =",minimum)

        values.append(minimum)

        alpha=max(alpha,minimum)

        iteration+=1

    answer=max(values)

    print("\n====================================")
    print("Values returned to MAX :",values)
    print("Final Minimax Value :",answer)

    if answer==values[0]:
        print("Best Move : Left Subtree")
    else:
        print("Best Move : Right Subtree")

    ch=input("\nRun Again?(y/n): ")

    if ch.lower()!='y':
        break

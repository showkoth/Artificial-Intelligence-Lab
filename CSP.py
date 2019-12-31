#import networkx as nx
import random
import time
import numpy as np
from fractions import gcd
import sympy
import math
from queue import *
import copy
from collections import deque
from copy import deepcopy
# # importing the matplotlib library for plotting the graph 
import matplotlib.pyplot as plt

'''
****************************************Generating graph as Object*****************************************
'''

class CSP(object):
        
        def __init__(self,n):
                self.num_of_nodes = n
                self.Variables = list(range(self.num_of_nodes))
                self.adjacency = self.create_graph()
                #self.printGraph(self.adjacency)
                self.Domains = self.setDomains()
                #self.printDomain()
                self.ConstraintGraph = self.setConstraints()
                self.neighbours = self.setNeighbours()
                self.arcs = self.getArcs()
                print("edge: ",int(len(self.arcs)/2))
        
                


        def printGraph(self,g):
                for i in range(self.num_of_nodes):
                        for j in range(self.num_of_nodes):
                                print(g[i][j], end = " ")
                        print()

        def printDomain(self):
                print("Domains are as belows: ")
                for i in range(self.num_of_nodes):
                        print(self.Domains[i])

        def getArcs(self):
                q = []
                for xi in self.Variables:
                        for xj in self.Variables:
                                if self.ConstraintGraph[xi][xj] != 0:
                                        tuple = (xi,xj)
                                        q.append(tuple)
                return q


        def setNeighbours(self):
                nei = []
                for xi in range(self.num_of_nodes):
                        nb = []
                        for xj in range(self.num_of_nodes):
                                if self.ConstraintGraph[xi][xj] != 0:
                                        nb.append(xj)
                        nei.append(nb)
                return nei


        def setConstraints(self):
                adj = self.adjacency
                cnt = 0
                degree = {}
                for x in self.Variables:
                        degree[x] = 0
                for i in self.Variables:
                        edge = 0
                        for j in self.Variables:
                                  
                                if adj[i][j] ==1 or adj[i][j] ==2 or adj[i][j]==3 or adj[i][j] == 4:
                                        continue
                                elif i == j:
                                        adj[i][j] = 0

                                elif (degree[i] < 2 and adj[i][j] == -1):
                                        cnt = random.randint(0,1)
                                        c = (i) % 4 + 1
                                        adj[i][j] = c
                                        adj[j][i] = c
                                        degree[i] += 1
                                        degree[j] += 1
                                          
                                else:
                                      
                                        adj[i][j] = 0
                                        adj[j][i] = 0
                                
                        
                        
                return adj

        def setDomains(self):
                domain = []
                ds = list(range(120, 200))
                
                for j in self.Variables:

                        dsize = random.choice(ds)
                        #print("dsize", dsize)
                        k = np.random.randint(1, 100, dsize)
                        i = np.unique(k)
                        domain.append(i.tolist())
                       
        
                return domain


        def create_graph(self):
                
                adjacency = np.random.randint(-2,0,(self.num_of_nodes,self.num_of_nodes))
                #print("Type is : ", type(adjacency))
                return adjacency

        

def satisfy(csp,Xi,x,Xj,val):
        cons = csp.ConstraintGraph[Xi][Xj]
        if cons == 1:
                if math.gcd(x,val) == 1:
                        return True
        elif cons == 2:
                
                if x == val:
                        return True
        elif cons == 3:
                if (Xi < Xj) :
                        if x > val:
                                return True
                else:
                        if x < val:
                                return True

        elif cons == 4:
                if (x + val) < 100:
                        return True

        return False


def isSatisfied(csp,Xi,x,Xj):
        cons = csp.ConstraintGraph[Xi][Xj]
        if cons == 1:
                for y in csp.Domains[Xj]:
                        #print("gcd ",math.gcd(12,42))
                        if math.gcd(x,y) == 1:
                                return True
        elif cons == 2:
                y = x
                if y in csp.Domains[Xj]:
                        return True
        elif cons == 3:
                for y in csp.Domains[Xj]:
                        if Xi < Xj:
                                if x > y:
                                        return True
                        else: 
                                if x < y:
                                        return True
        elif cons == 4:
                for y in csp.Domains[Xj]:
                        if (x + y) <100:
                                return True

        return False


def Revise(csp,Xi,Xj):
        revised = False
        removal = []
        for x in csp.Domains[Xi]:
                if not isSatisfied(csp,Xi,x,Xj):
                        #print(type(csp.Domains[Xi]))
                        #csp.Domains[Xi].remove(x)
                        removal.append(x)
                        revised = True
        for i in removal:
                csp.Domains[Xi].remove(i)
        return revised

'''
****************************************AC1*****************************************
'''
def AC1(csp):
        startTime = time.time()
        edge_list = csp.getArcs() 
        flag = True
        while flag:
                flag = False
                for (Xi,Xj) in edge_list:
                        if Revise(csp,Xi,Xj):
                                if len(csp.Domains[Xi]) == 0:
                                        timeTaken = time.time() - startTime
                                        return (False,timeTaken)
                                flag = True
                #csp.printDomain()
        timeTaken = time.time() - startTime
        return (True,timeTaken)

'''
****************************************AC2*****************************************
'''
def AC2(csp):
        #csp.printGraph(csp.ConstraintGraph)
        startTime = time.time()
        q1 = deque()
        q2 = deque()
        for i in csp.Variables:
                for j in csp.Variables:
                        if csp.ConstraintGraph[i][j] != 0 and i < j :
                                q1.append((i,j))
                                q2.append((j,i))

        while q1:
                while q1:
                        (Xi,Xj) = q1.pop()
                       # csp.printDomain()
                        if Revise(csp,Xi,Xj):
                                if len(csp.Domains[Xi]) == 0:
                                        timeTaken = time.time() - startTime                      
                                        return (False,timeTaken)
                                for Xk in csp.neighbours[Xi]:
                                        if Xk < Xi and Xk != Xj:
                                                q2.append((Xk,Xi))
                while q2:
                        q1.append(q2.pop())
        timeTaken = time.time() - startTime                      
        return (True,timeTaken)

'''
****************************************AC3*****************************************
'''

def AC3(csp):
        startTime = time.time()
        arc_list = csp.arcs
        q = deque(arc_list)
        while q:
                (Xi, Xj) = q.popleft()
                
                if Revise(csp,Xi,Xj):
                        #print("one item revised")
                        if not csp.Domains[Xi]:
                                timeTaken = time.time() - startTime
                                return (False,timeTaken)
                        for Xk in csp.neighbours[Xi]:
                                if Xk != Xj:
                                        q.append((Xk,Xi))
                                        
        timeTaken = time.time() - startTime                      
        return (True,timeTaken)

'''
****************************************AC4*****************************************
'''

def AC4(csp):
        startTime = time.time()
        S = {}
        Counter = {}
        li = deque()
        removal = []
        for Xi in csp.Variables:
                for x in csp.Domains[Xi]:
                        
                        value = []
                        for Xj in csp.neighbours[Xi]:
                                cnt = 0
                                for y in csp.Domains[Xj]:
                                        if satisfy(csp,Xi,x,Xj,y):
                                                cnt += 1
                                                value.append((Xj,y))
                                                #S[(Xi,x)].append((Xj,y))
                                Counter[(Xi,x,Xj)] = cnt
                                if cnt == 0:
                                        li.append((Xi,x))
                        S[(Xi,x)] = value

        
        while li:
                rm = li.pop()
                if rm not in removal:
                        removal.append(rm)
                pairlist = S[rm]

                for pair in pairlist:
                        #print(type(pair))
                        x = pair[0]
                        y = pair[1]
                        if (x,y) in removal:
                                continue
                        z = rm[0]
                        Counter[(x,y,z)]-=1
                        if Counter[(x,y,z)] == 0:
                                li.append((x,y))
        #removal = list(set(removal))
        for (Xi,x) in removal:
                if x in csp.Domains[Xi]:
                        csp.Domains[Xi].remove(x)
                        if len(csp.Domains[Xi]) == 0:
                                timeTaken = time.time() - startTime                      
                                return (False,timeTaken)


                        
        timeTaken = time.time() - startTime                      
        return (True,timeTaken)

'''
****************************************Main*****************************************
'''   

def main():
        number_of_nodes = [10,20,30,40,60,80,100,120,160,200,220,260,280,310]
        ac1_time = []
        ac2_time = []
        ac3_time = []
        ac4_time = []
        for n in number_of_nodes:
                print("number of nodes: ", n)
                csp1 = CSP(n)
                csp2 = deepcopy(csp1)
                csp3 = deepcopy(csp1)
                csp4 = deepcopy(csp1)

                (isSatisfiable1,time1) = AC1(csp1)
                ac1_time.append(time1)
                print("The graph is satisfiable: " ,isSatisfiable1)
                print("Time taken: ",time1)

                (isSatisfiable2,time2) = AC2(csp2)
                ac2_time.append(time2)
                print("The graph is satisfiable: " ,isSatisfiable2)
                print("Time taken: ",time2)

                (isSatisfiable3,time3) = AC3(csp3)
                ac3_time.append(time3)
                print("The graph is satisfiable: " ,isSatisfiable3)
                print("Time taken: ",time3)

                (isSatisfiable4,time4) = AC4(csp4)
                ac4_time.append(time4)
                print("The graph is satisfiable: " ,isSatisfiable4)
                print("Time taken: ",time4)

        plt.plot(number_of_nodes,ac1_time)
        plt.plot(number_of_nodes,ac2_time)
        plt.plot(number_of_nodes,ac3_time)
        plt.plot(number_of_nodes,ac4_time)
        
        plt.title("Performance Comparison")
        plt.xlabel("Number of Nodes")
        plt.ylabel("Avg Run Time of Algorithms")
        plt.legend(["AC1","AC2","AC3","AC4"])
        plt.show()


    


if __name__=="__main__":
    main()
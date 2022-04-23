import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

def csvStrtoList(csv_data):
    csv_data = csv_data.replace(' ', '')
    csv_data = csv_data.split(',')
    return csv_data

def createNode(Artist_List, Producer_List):
    Artist_List = sum(Artist_List, [])
    Producer_List = sum(Producer_List, [])
    Node_List = Artist_List + Producer_List
    Node_set = set(Node_List)
    Node_List = list(Node_set)
    return Node_List

def createEdge(Artist_List, Producer_List, Month_List, Rank_List):
    Edge_List = []
    for i in range(0, len(Artist_List)):
        for j in range(0, len(Artist_List[i])):
            for k in range(0, len(Producer_List[i])):
                Edge_List.append((Artist_List[i][j], Producer_List[i][k], Month_List[i], Rank_List[i]))
    return Edge_List

def calculateEdgeWeight(Edge_List):
    Edge_List.sort()
    monthWeightList = []
    returnEdge_List = []
    weight = (1-Edge_List[0][3]/100)*100
    for i in range(0, len(Edge_List)):
        if(i == len(Edge_List)-1):
            temp = 0
            monthWeightList.append(weight)
            for j in range(0, len(monthWeightList)):
                temp += monthWeightList[j]
            temp /= len(monthWeightList)
            returnEdge_List.append([Edge_List[i][0], Edge_List[i][1], temp])
            break;
        if(Edge_List[i][0] == Edge_List[i+1][0] and Edge_List[i][1] == Edge_List[i+1][1]):
            if(Edge_List[i][2] == Edge_List[i+1][2]):
                weight += (1-Edge_List[i+1][3]/100)*100
            elif(Edge_List[i][2] != Edge_List[i+1][2]):
                monthWeightList.append(weight)
                weight = (1-Edge_List[i+1][3]/100)*100
        elif(Edge_List[i][0] != Edge_List[i+1][0] or Edge_List[i][1] != Edge_List[i+1][1]):
            temp = 0
            monthWeightList.append(weight)
            for j in range(0, len(monthWeightList)):
                temp += monthWeightList[j]
            temp /= len(monthWeightList)
            returnEdge_List.append([Edge_List[i][0], Edge_List[i][1], temp])
            monthWeightList = []
            weight = (1-Edge_List[i+1][3]/100)*100
    return returnEdge_List


ArtistList = ProducerList = NodeList = EdgeList = MonthList = RankList = weightList = []

df = pd.read_csv("MelonCrollingResult.csv", encoding='cp949')

ArtistList = df['Artist'].apply(csvStrtoList)
ProducerList = df['Producer'].apply(csvStrtoList)
MonthList = df['Month']
RankList = df['Rank']
NodeList = createNode(ArtistList, ProducerList)
EdgeList = createEdge(ArtistList, ProducerList, MonthList, RankList)
weightList = calculateEdgeWeight(EdgeList)

GraphResult = nx.Graph()
GraphResult.add_nodes_from(NodeList)
for i in range(0, len(weightList)):
    GraphResult.add_edge(weightList[i][0], weightList[i][1], weight = weightList[i][2])
nx.write_gexf(GraphResult, "WeightedDegree.gexf")
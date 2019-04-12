import numpy as np
import random
from scipy.spatial import distance as scipy
import matplotlib.pyplot as plt 

fname=input("file")
with open(fname) as f:
    Datafile = f.read().splitlines()

DataMatrix=[]
for line in Datafile:
     features = [] 
     feature=line.split(",")
     for i in range(1,11):
        features.append(int(feature[i]))
     DataMatrix.append(features)

k=3


def AssignCluster(k, DataMatrix, centroids):
    #Clusters
    clusters=[]
    for example in DataMatrix:
        distance=[]
        for c in centroids:
            d=scipy.euclidean(c,example,)
            distance.append(d)
        cluster=np.argmin(distance)
        clusters.append(cluster)
    return clusters

#Split largest cluster when a cluster is empty to maintain total K clusters.
def SplitCluster(k, maxCluster, size,clusterToReplace,clusters):
    half=int(size/2)
    for i in range(len(clusters)):
        if half>0:
            if clusters[i]==maxCluster:
                clusters[i]=clusterToReplace
                half=half-1
    return clusters





def Recenter(k, DataMatrix, clusters, centers_old):
    centers_new=[]
    MaxclusterSize=0
    for i in range(k):
        points = [DataMatrix[j] for j in range(len(DataMatrix)) if clusters[j] == i]
        if len(points)>MaxclusterSize:
            MaxclusterSize=len(points)
            maxCluster=i
        if len(points)==0:
            newClusters= SplitCluster(k,maxCluster,MaxclusterSize,i,clusters)
            points = [DataMatrix[j] for j in range(len(DataMatrix)) if newClusters[j] == i]
            pointsBigCluster=[DataMatrix[j] for j in range(len(DataMatrix)) if newClusters[j] == maxCluster]
            centers_new[maxCluster]=(np.mean(pointsBigCluster, axis=0))
        centers_new.append(np.mean(points, axis=0))
    return centers_new

def Error(centers_new, centers_old):
         error=0
         for i in range(k):
             error= error + scipy.euclidean(centers_new[i], centers_old[i])
         if error<0.01:
            return False
         else:
             return True

def PotentialFun(k, DataMatrix, centroid, clusters):
    distance=0
    for i in range(k):
        points = [DataMatrix[j] for j in range(len(DataMatrix)) if clusters[j] == i]
        for p in points:
            eucDistance=scipy.euclidean(centroid[i], p)
            squaredDistance= eucDistance*eucDistance
            distance=distance+squaredDistance
    return distance

         


def KMeans( k, DataMatrix):
    
    #centroid init
    centroids = []
    population=len(DataMatrix)
    seq=[i for i in range(population)]
    num= random.sample(seq, k)
    for i in num:
         centroids.append(DataMatrix[i])
    centers_old=centroids
    error=True
    
    while(error):
         clusters= AssignCluster(k, DataMatrix, centers_old)
         newCenters= Recenter(k, DataMatrix,clusters,centers_old)
         error= Error(newCenters, centers_old)
         centers_old=newCenters

    potF=PotentialFun(k,DataMatrix,newCenters,clusters)
    return potF

kArray=[2,3,4,5,6,7,8]
potf=[]

for k in kArray:
     potf.append(KMeans(k, DataMatrix))   
      

# plotting the points  
plt.plot(kArray, potf) 
plt.xlabel('K Values') 
plt.ylabel('Pot F') 
plt.title('KMeans') 
plt.show() 
    






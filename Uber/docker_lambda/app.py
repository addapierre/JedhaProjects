import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import json


def handler(event, context):

    body = json.loads(event['body'])
    month = body['month']
    hour1 = body['hour1']
    hour2 = body['hour2']
    day = body['day']

    res = {}
    content = {}
    res['headers'] = {'Content-Type' : 'json'}

    #load the month and select the lines for the day and the time window
    coords = np.load(month+'.npy', allow_pickle = True)
    index = np.where((coords[:,2] >= hour1) & (coords[:,2] <= hour2) & (coords[:,3] == day))[0]
    coords = coords[index]
    coords = coords[:, :2]

    # begin clustering
        # elbow:
    kmean_list = []
    elbow = []
    for i in range(2,14):
        kmeans = KMeans(n_clusters=i, random_state=0)
        kmeans.fit(coords)
        kmean_list.append(kmeans.labels_.tolist())
        elbow.append(kmeans.inertia_)

    content['elbow'] = elbow
    
        # best elbow
    elbow_d = []
    for i in range(1,len(elbow)-1):
        d1 = elbow[i-1]-elbow[i]
        d2 = elbow[i]-elbow[i+1]
            # d2 should always be >0 but let's put a test just in case
        if d2!=0 :
            elbow_d.append((d1-d2)/(d1+d2))
        else:
            elbow_d.append(-1)
            break
    elbow_d = np.array(elbow_d)

            # if at some point d2==0, the loop breaks, so we will take the last element of elbow_d
    if np.isin(-1, elbow_d):
        best_elbow = elbow_d.shape[0]+1
            #else take max(elbow_d)
    else:
        best_elbow = np.where(elbow_d==elbow_d.max())[0][0]+3 # +3 because kmeans begins at n=2 and elbows begin at n=3

    content['elbow_d'] = elbow_d.tolist()
    content['best_elbow'] = int(best_elbow)

        # silhouette:
    silhouette = []

    for i in range(best_elbow, min(best_elbow + 5, 14) ):
        silhouette.append(silhouette_score(coords, kmean_list[i-2]))

    content['silhouette'] = silhouette

        # best_silhouette
    sil = np.array(silhouette)
    best_silhouette = np.where(sil == sil.max())[0][0]
    best_silhouette += best_elbow

    content['best_silhouette'] = int(best_silhouette)

    labels = kmean_list[best_silhouette-1] #-1 because it begins at n=2
    content['labels'] = labels
    content['index'] = index.tolist()

    res['statusCode'] =  200

    res['body'] = json.dumps(content)

    return res
    
        


    

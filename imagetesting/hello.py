from flask import Flask, render_template, request, jsonify, send_file, make_response
import atexit
import os
import json
from flask_cors import CORS
import base64
from io import BytesIO
from PIL import Image
from werkzeug import FileStorage
import numpy as np
from skimage import io, color, segmentation, transform
from sklearn.cluster import MeanShift, estimate_bandwidth, DBSCAN
from sklearn.datasets.samples_generator import make_blobs
import os
import zipfile
from zipfile import ZipFile
from watson_developer_cloud import VisualRecognitionV3 as VisualRecognition
import json
from matplotlib import pyplot as plt
from skimage.filters import roberts, sobel, scharr, prewitt
import scipy.cluster.hierarchy as hcluster
from sklearn import metrics
from base64 import b64encode
import scipy

app = Flask(__name__)

db_name = 'mydb'
client = None
db = None
CORS(app)

#takes in a list of ingredients, returns list of possible recipes
def threshold(fileName):

    rgb = scipy.misc.imread(fileName, mode='RGB')
    aspect_ratio = len(rgb) / len(rgb[1])
    img = color.rgb2lab(rgb)
    thresholded = np.logical_and(*[img[..., i] > t for i, t in enumerate([40, 0, 0])])
    if (np.sum(thresholded) > (thresholded.size / 2)):
        thresholded = np.invert(thresholded)
    
    plt.imshow(thresholded); 
    plt.axis('off')
    
    if os.path.exists('thresh.png'):
        os.remove('thresh.png')
    plt.savefig('thresh.png', bbox_inches='tight')
    




#takes in an image file and returns a list of ingredients in the image
def cluster(fileName):

    rgb = scipy.misc.imread(fileName, mode='RGB')
    
    aspect_ratio = len(rgb) / len(rgb[1])
    img = color.rgb2lab(rgb)
    thresholded = np.logical_and(*[img[..., i] > t for i, t in enumerate([40, 0, 0])])
    if (np.sum(thresholded) > (thresholded.size / 2)):
        thresholded = np.invert(thresholded)
        
    X = np.argwhere(thresholded)[::5]
    X = np.fliplr(X)


    db = DBSCAN(eps=25, min_samples=200).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print('Estimated number of clusters: %d' % n_clusters_)


    # #############################################################################
    # Plot result

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = X[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=14)

        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=6)

    plt.axis('off')
    if os.path.exists('clust.png'):
        os.remove('clust.png')
    plt.savefig('clust.png', bbox_inches='tight')

def full(fileName):
    vr = VisualRecognition(version='2016-05-20', api_key='7b851fccf7f17a35fc7569a5dad6e1eb4f650f70')

    rgb = scipy.misc.imread(fileName, mode='RGB')
    aspect_ratio = len(rgb) / len(rgb[1])
    rgb = transform.resize(rgb, [int(1000*aspect_ratio), 1000])
    img = color.rgb2lab(rgb)
    thresholded = np.logical_and(*[img[..., i] > t for i, t in enumerate([40, 0, 0])])
    if (np.sum(thresholded) > (thresholded.size / 2)):
        thresholded = np.invert(thresholded)
        
    X = np.argwhere(thresholded)[::5]
    X = np.fliplr(X)


    db = DBSCAN(eps=25, min_samples=200).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print('Estimated number of clusters: %d' % n_clusters_)



    unique_labels = set(labels)


    cropped_images = []
    unique_labels.remove(-1)
    col=0

    for k in unique_labels:
        #my_members = labels == k
        #members = X[my_members, 0]
        left = min(X[labels==k][:,0])
        right = max(X[labels==k][:,0])
        padding = 20
        if left > padding:
            left = left - padding
        if right < len(img[1]) - padding:
            right = right + padding
        cropped_images.append(rgb[0:len(img), left:right])	

    # save each cropped image by its index number
    myzip = ZipFile('test.zip', 'w',zipfile.ZIP_DEFLATED)
    for c, cropped_image in enumerate(cropped_images):
        io.imsave(str(c) + ".png", cropped_image)
        myzip.write(str(c) + ".png")    

    myzip.printdir()
    myzip.close()  

    for c, cropped_image in enumerate(cropped_images):
        os.remove(str(c) + ".png")

    classes = []
    with open('test.zip', 'rb') as img:
        param = {'classifier_ids':"foodtest_1606116153"}
        params = json.dumps(param)
        response = vr.classify(images_file=img, parameters=params)

        for image in response['images']:
            max_score = 0
            max_class = ""
            for classifier in image['classifiers']:
                for classif in classifier['classes']:
                    if (classif['score'] > max_score):
                        max_class = classif['class']
            
            
            if max_class:
                max_class = max_class.replace('_', ' ')
                if (max_class) not in classes:
                    classes.append(max_class)
                    
        
        
        
    os.remove('test.zip')
    return(classes)




# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 443))

@app.route('/image1', methods=['POST'])
def image1t():
    if os.path.exists('testpic.png'):
        os.remove('testpic.jpg')
    FileStorage(stream=request.files['image']).save('testpic.jpg')
    return jsonify({'done':'done'})
	
@app.route('/image2', methods=['GET'])
def image2t():
    threshold('testpic.jpg')
    #return send_file('thresh.png')

    with open("thresh.png", "rb") as image_file:
        encoded_string = b64encode(image_file.read())
    response1 = make_response(encoded_string)
    response1.headers['Content-Type'] = 'image/png'
    response1.headers['Content-Disposition'] = 'attachment; filename=img.png'
    return response1

	
@app.route('/image3', methods=['GET'])
def image3t():
    cluster('testpic.jpg')
    with open("clust.png", "rb") as image_file:
        encoded_string = b64encode(image_file.read())
    response1 = make_response(encoded_string)
    response1.headers['Content-Type'] = 'image/png'
    response1.headers['Content-Disposition'] = 'attachment; filename=img.png'
    return response1
    
@app.route('/image4', methods=['GET'])
def image4t():
    ingList = full('testpic.jpg')
    return jsonify({'ingredients':ingList})

@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

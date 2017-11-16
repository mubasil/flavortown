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

class ImageClassifier:

    def __init__(self): 
        self.vr = VisualRecognition(version='2016-05-20', api_key='7b851fccf7f17a35fc7569a5dad6e1eb4f650f70')

    def classify(self, imgFile):
        rgb = io.imread(imgFile)
        aspect_ratio = len(rgb) / len(rgb[1])
        rgb = transform.resize(rgb, [int(1000*aspect_ratio), 1000])
        img = color.rgb2lab(rgb)
        thresholded = np.logical_and(*[img[..., i] > t for i, t in enumerate([40, 0, 0])])
        '''
        fig, ax = plt.subplots(ncols=2)
        ax[0].imshow(rgb);         ax[0].axis('off')
        ax[1].imshow(thresholded); ax[1].axis('off')
        plt.show()
        '''

        X = np.argwhere(thresholded)[::5]
        X = np.fliplr(X)


        db = DBSCAN(eps=50, min_samples=200).fit(X)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_

        # Number of clusters in labels, ignoring noise if present.
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

        print('Estimated number of clusters: %d' % n_clusters_)
        unique_labels = set(labels)

        '''
        # #############################################################################
        # Plot result
        import matplotlib.pyplot as plt

        # Black removed and is used for noise instead.
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

        plt.title('Estimated number of clusters: %d' % n_clusters_)
        plt.show()



        x = edge_roberts.sum(axis=0)
        x = x - np.min(x[np.nonzero(x)])
        averageVal = x.mean()
        x = x - 5
        x[x < (averageVal / 6)] = 0

        y = range(len(img[1]))
        plt.plot(y, x)


        X = np.array(list(zip(x,np.zeros(len(x)))), dtype=np.int)
        bandwidth = estimate_bandwidth(X, quantile=0.25)
        ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
        ms.fit(X)
        labels = ms.labels_
        cluster_centers = ms.cluster_centers_

        labels_unique = np.unique(labels)
        n_clusters_ = len(labels_unique)
        '''


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
        myzip = ZipFile('cutimgs.zip', 'w',zipfile.ZIP_DEFLATED)
        for c, cropped_image in enumerate(cropped_images):
            io.imsave(str(c) + ".png", cropped_image)
            myzip.write(str(c) + ".png")    

        myzip.printdir()
        myzip.close()  

        for c, cropped_image in enumerate(cropped_images):
            os.remove(str(c) + ".png")
            
        with open('cutimgs.zip', 'rb') as img:
            param = {'classifier_ids':"foodtest_843163904"}
            params = json.dumps(param)
            response = self.vr.classify(images_file=img, parameters=params)
            classes = []
            for image in response['images']:
                if (image['classifiers'][0]['classes'][0]['class']) not in classes:
                    classes.append((image['classifiers'][0]['classes'][0]['class']))
                    
              
        os.remove('cutimgs.zip')
        
        return classes

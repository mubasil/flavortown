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
import scipy

vr = VisualRecognition(version='2016-05-20', api_key='7b851fccf7f17a35fc7569a5dad6e1eb4f650f70')

rgb = scipy.misc.imread('testpic.jpg', mode='RGB')
aspect_ratio = len(rgb) / len(rgb[1])
img = color.rgb2lab(rgb)
thresholded = np.logical_and(*[img[..., i] > t for i, t in enumerate([40, 0, 0])])
    
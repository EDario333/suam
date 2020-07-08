#!/usr/bin/env python 

# https://www.machinecurve.com/index.php/2020/04/16/how-to-perform-k-means-clustering-with-python-in-scikit/#
# https://machinelearningmastery.com/clustering-algorithms-with-python/
# https://scikit-learn.org/stable/auto_examples/cluster/plot_color_quantization.html#sphx-glr-auto-examples-cluster-plot-color-quantization-py
# https://scikit-learn.org/stable/modules/clustering.html

'''
Parallel 4 loops:
https://joblib.readthedocs.io/en/latest/parallel.html

from joblib import parallel_backend

with parallel_backend('threading', n_jobs=2):
    # Your scikit-learn code here
'''

'''
Strategies to scale computationally: bigger data:
https://scikit-learn.org/stable/modules/computing.html#parallelism
'''

'''
Principal Component Analysis (PCA)
https://www.youtube.com/watch?v=FgakZw6K1QQ
https://youtu.be/AniiwysJ-2Y
'''

'''
Uncompress zlib data
https://unix.stackexchange.com/questions/22834/how-to-uncompress-zlib-data-in-unix

"gzip" is often also used to refer to the gzip file format, which is: a 10-byte header, 
containing 

a magic number ( 1f 8b ), the compression method 
( 08 for DEFLATE), 1-byte of header flags, a 4-byte timestamp, compression flags and the operating system ID.
'''

'''
Get eigenvectors:
https://stackoverflow.com/questions/31909945/obtain-eigen-values-and-vectors-from-sklearn-pca

n_samples = X.shape[0]
# We center the data and compute the sample covariance matrix.
X -= np.mean(X, axis=0)
cov_matrix = np.dot(X.T, X) / n_samples
for eigenvector in pca.components_:
    print(np.dot(eigenvector.T, np.dot(cov_matrix, eigenvector)))
'''
# https://www.educaedu.com.mx/doctorado-en-ciencias-fisico-matematicas-doctorado-38869.html#form-info
# http://www.udg.mx/es/oferta-academica/posgrados/doctorados/doctorado-en-fisico-matematicas
import os

from . import AbstractRunner
THIS_FILE_NAME=os.path.basename(__file__)

class Scikit(AbstractRunner):
	def run(self,**kwargs):
		super().run(**kwargs)

		import matplotlib.pyplot as plt
		import numpy as np
		from sklearn.cluster import KMeans

		x=np.array(self._data)

		# Configuration options
		num_samples_total = len(x)
		cluster_centers = []
		for cluster in self._cf_tool.clusters:
			cluster_centers.append(tuple(cluster["center"]))

		num_classes = len(cluster_centers)

		# np.save('./clusters.npy', X)
		# X = np.load('./clusters.npy')

		# Fit K-means with Scikit
		kmeans = KMeans(init='k-means++', n_clusters=num_classes, n_init=self._cf_tool.times)
		kmeans.fit(x)

		# Predict the cluster for all the samples
		P = kmeans.predict(x)

		# Generate scatter plot for training data
		# colors = list(map(lambda x: '#3b4cc0' if x == 1 else '#b40426', P))
		colors = list(map(lambda x: self._cf_tool.clusters[x]["color"], P))
		plt.scatter(x[:,0], x[:,1], c=colors, marker=self._cf_tool.plot["marker"], picker=True)
		plt.title(self._cf_tool.plot["title"])
		plt.xlabel(self._cf_tool.plot['x']["label"])
		plt.ylabel(self._cf_tool.plot['y']["label"])
		if "file" in self._cf_tool.plot:
			plt.savefig(self._cf_tool.plot["file"])
		else:
			plt.show()
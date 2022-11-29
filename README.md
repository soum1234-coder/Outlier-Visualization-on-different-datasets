# Outlier-Visualization-on-different-datasets

We will use outlier visualization as the theme to get you started. And we’ll use several variants, by using different datasets, embedding methods, and clustering methods, to cover a wide range of techniques.

The overall flow will be as follows:
Get an image dataset
Featurize this dataset so you can use any ML technique, as opposed to fancy CNN-based techniques specific to image tasks
Embed the feature representations to a 2d space so you can visualize the data
Cluster the data points, either after step (2) or step (3)
Select points with lowest cluster probabilities as outliers
Plot the clustering, with the outliers highlighted
Display images corresponding to some of these outliers

#Datasets and featurization

Use make_blobs to generate a simple dataset. This isn’t an image dataset.
If we use this, we don’t have to featurize further. You already have a vector representation for each datapoint.
Get the digits dataset provided by scikit-learn. Or, download MNIST-Digits. The latter is preferable.
For digits from scikit-learn, the simplest feature representation is to just flatten the 8x8 grayscale images.
Additionally, you can do a PCA on the flattened images (using n_components=16 should suffice). For MNIST-Digits, which has 28x28 images, it’s recommended to flatten the 28x28 images to 784 dimensional vectors, and then do PCA to get to 16-d or 24-d feature representations.
Get a proper image classification dataset, start with CIFAR-10
This needs proper featurization before we can do any embedding or clustering. Use a simple CNN model for this.
For instance, use MobilenetV2; or see this tutorial. These featurizers take an image as input, and produce a 1280-dimensional feature vector. The feature vector can be used for 2d embedding, clustering, etc.




#Embedding
For these tasks, we use ‘embedding’ to mean a 2d embedding of a feature vector so that we can visualize data points in a simple scatter plot. That is, given a 1280-dimensional feature vector (or some other m-dimensional feature vector) for some data point, we calculate a 2-dimensional representation for the same data point such that:
Data points that are close to each other in the original feature space must be close to each other in the 2-d space.

There are several techniques for this. For these tasks, try out the following two:
PCA (from scikit-learn)
UMAP


#Clustering

From the previous step, we have two representations available for the data:
The full feature representation after the featurization
The 2d representation after the embedding

We can do clustering using either of these. It’s recommended to try both and see what happens.

Try the following two clustering techniques:
KMeans (from scikit-learn)
HDBSCAN
This is a density based clustering algorithm that works when data points are grouped in any shapes, sizes, and densities; KMeans assumes that the data has nice spherical groups of nearly uniform sizes
You don’t have to provide ‘k’, the number of clusters. It will calculate this for you.
It is recommended that you read how this method works to build intuition on similar clustering methods.



In addition to visualizing just the embeddings, you can also look at what images correspond to these outlying points.


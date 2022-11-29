# -*- coding: utf-8 -*-
"""Internship Task.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1byNxEUxpzVAIFMbZnG_70-TJkd1OQ8lA

#ML Intro task
The overall flow will be as follows:

1.Get an image dataset

2.Featurize this dataset so you can use any ML technique, as opposed to fancy CNN-based techniques specific to image tasks

3.Embed the feature representations to a 2d space so you can visualize the data

4.Cluster the data points, either after step (2) or step (3)

5.Select points with lowest cluster probabilities as outliers

6.Plot the clustering, with the outliers highlighted

7.Display images corresponding to some of these outliers

#Importing Libraries
"""

"""Importing Libraries"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod


import hdbscan
from sklearn.datasets import make_blobs
from keras.datasets import mnist
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from hdbscan.flat import (HDBSCAN_flat,
                          approximate_predict_flat,
                          membership_vector_flat,
                          all_points_membership_vectors_flat)

import tensorflow as tf
import tensorflow_hub as hub
from tensorflow import keras
from tensorflow.keras.datasets import cifar10 
from tensorflow.keras.utils import to_categorical
from keras.applications.imagenet_utils import decode_predictions
from keras.applications.mobilenet_v2 import preprocess_input

"""#Main Class

Datasets used:

1.MNIST dataset

2.CIFAR10 dataset

3.Make_blobs dataset(it doesnt need any featurization,it already have a vector representation)
"""

class Outlier_Visualization(ABC):

  """
  This class is defined to declare all the abstract methods that
  will be used by different datasets. The methods include technqiues
  like the PCA and UMAP embedding, Kmeans training, HDBSCAN and 
  plotting scatter plots.

  """
  

  def __init__(self,input_data='cifar10',embedding_technique='pca',clustering_technique='kmeans'):
    self.input_data=input_data
    self.embedding_technique = embedding_technique
    self.clustering_technique = clustering_technique

  
  @abstractmethod
  def display_data(self):
    """ abstract method for visualizing different datasets before any featurization,
    embedding and clustering.

    """
    pass


  @abstractmethod
  def featurize(self):
    """ abstract method for featurizing datasets if needed """
    pass

  """ Cifar10 dataset needs proper featurization before we can do any embedding or clustering. 
  So we implement a simple CNN model for this.(Mobilenetv2 model)
 These featurizers take an image as input, and produce a 1280-dimensional feature vector. 
 The feature vector can be used for 2d embedding, clustering, etc."""

  


  def pca_embedding(self,h,z):
    
    """ Method performs pca embedding on different datasets to have a 16d or 24d representation

    PARAMETERS:
    h:numpy.ndarray
    dummy variable for the data that has to be embedded

    z:numpy.ndarray
    dummy variable for the labels of data through which it can be visualize
    
    """

    if len(h[0])==2:
      self.X_embed =h
      print("The shape of data after PCA",self.X_embed.shape)
    #Using matplotlib visualization
      scatter_classes=plt.scatter(self.X_embed[:,0],self.X_embed[:,1],c=z)
      plt.legend(*scatter_classes.legend_elements(),
                    loc="upper right", title="Classes")
      plt.title('PCA projection  \n', fontsize=24);
      plt.show()

    else:   

      pca = PCA(n_components=2)
      self.X_embed = pca.fit_transform(h)

      print("The shape of data after PCA",self.X_embed.shape)
    #Using matplotlib visualization
      scatter_classes=plt.scatter(self.X_embed[:,0],self.X_embed[:,1],c=z)
      plt.legend(*scatter_classes.legend_elements(),
                    loc="upper right", title="Classes")
      plt.title('PCA projection  \n', fontsize=24);
      plt.show()
      return


  def umap_embedding(self,h,z):
    """ Method performs umap embedding on different datasets to have a 2d representation

    PARAMETERS:
    h:numpy.ndarray
    dummy variable for the data that has to be embedded

    z:numpy.ndarray
    dummy variable for the labels of data through which it can be visualize
    
    """
    reducer = umap.UMAP()
    
    embedding=reducer.fit_transform(h)
    self.map=umap.UMAP().fit(h)

    self.emb=embedding
    

    print("The shape of data after UMAP  \n",embedding.shape)

    #2D Visualization of MNIST data using umap
    scatter_classes=plt.scatter(embedding[:, 0], embedding[:, 1], c=z, s=5)
    plt.legend(*scatter_classes.legend_elements(),
                    loc="upper right", title="Classes")

    plt.gca().set_aspect('equal', 'datalim')
    plt.colorbar(boundaries=np.arange(11)-0.5).set_ticks(np.arange(10))
    plt.title('UMAP projection ', fontsize=24);
  @abstractmethod
  def embedding(self):
    

    """abstract method to perform embedding on different datasets 
    so that we can visualize data points in a simple scatter plot.
    """
    pass

  def k_Clustering(self,z):
    """ Method performs kmeans clustering 

    PARAMETERS:

    z:numpy.ndarray
    dummy variable for the labels of data through which it can be visualize

    """

    if self.embedding_technique=='umap':
      n = len(np.unique(z))
      self.n=n
      print("Number of clusters: \n",n)
      kmeans=KMeans(n_clusters=n,random_state=0)
      kmeans.fit(self.emb)
      y_pred=kmeans.predict(self.emb)
      self.y_pred=y_pred
      cluster_classes=plt.scatter(self.emb[:, 0], self.emb[:, 1], c=y_pred, cmap='viridis')
      centers = kmeans.cluster_centers_
      plt.scatter(centers[:, 0], centers[:, 1], c='blue', s=100, alpha=0.9)
      plt.legend(*cluster_classes.legend_elements(),
                    loc="upper right", title="Classes")
      plt.show()
      data=kmeans.labels_[0:100]
      print("Labels of data :\n",data)
      dist=kmeans.transform(self.emb)
      self.dist=dist
    elif self.embedding_technique=='pca':
      n = len(np.unique(z))
      self.n=n
      print("Number of clusters: \n",n)
      kmeans=KMeans(n_clusters=n,random_state=0)
      kmeans.fit(self.X_embed)
      y_pred=kmeans.predict(self.X_embed)
      self.y_pred=y_pred
      cluster_classes=plt.scatter(self.X_embed[:, 0], self.X_embed[:, 1], c=y_pred, cmap='viridis')
      centers = kmeans.cluster_centers_
      plt.scatter(centers[:, 0], centers[:, 1], c='blue', s=100, alpha=0.9)
      plt.legend(*cluster_classes.legend_elements(),
                    loc="upper right", title="Classes")
      plt.show()
      data=kmeans.labels_[0:100]
      print("Labels of data :\n",data)
      dist=kmeans.transform(self.X_embed)
      self.dist=dist
    
    

  def hd_Clustering(self,z):
    """ Method performs hdbscan clustering 

    PARAMETERS:

    z:numpy.ndarray
    dummy variable for the labels of data through which it can be visualize

    """
    if self.embedding_technique=='umap':
      n = len(np.unique(z))
      clusterer = HDBSCAN_flat(self.emb,
                          cluster_selection_method='leaf',
                          n_clusters= n, min_cluster_size=10)
      self.clusterer=clusterer
      clusterer.fit(self.emb)
      cluster_labels=clusterer.labels_
      print(cluster_labels)
    #Visulalization of data in scattered plot
      cluster1_classes=plt.scatter(self.emb[:, 0], self.emb[:, 1], c=cluster_labels, cmap='viridis')
      plt.legend(*cluster1_classes.legend_elements(),
                    loc="upper right", title="Classes")
      plt.show()

    elif self.embedding_technique=='pca':
      n = len(np.unique(z))
      clusterer = HDBSCAN_flat(self.X_embed,
                          cluster_selection_method='leaf',
                          n_clusters= n, min_cluster_size=10)
      self.clusterer=clusterer
      clusterer.fit(self.X_embed)
      cluster_labels=clusterer.labels_
      print(cluster_labels)
    #Visulalization of data in scattered plot
      cluster1_classes=plt.scatter(self.X_embed[:, 0], self.X_embed[:, 1], c=cluster_labels, cmap='viridis')
      plt.legend(*cluster1_classes.legend_elements(),
                    loc="upper right", title="Classes")
      plt.show()

  def clustering(self):
    """abstract method to perform embedding technique on different datsets"""
    pass

  def score(self,x,y,n):
    """Method to calculate clustering score for kmeans"""
    dist_cluster=x[y]
    lower=sum([(1/z)**(n-1) for z in x])
    upper=(1/dist_cluster)**(n-1)
    return upper/lower  
    

  def k_outlier(self):
    """ Method to have outliers identified and visualize using kmeans""" 
    if self.embedding_technique=='umap':
      N=self.n
    

      clustering_scores=[self.score(self.dist[i],self.y_pred[i],N)\
                         for i in list(range(0,len(self.y_pred)))]
    
    

      clustering_scores=np.array(clustering_scores)
      self.clustering_scores=clustering_scores
      mask_outliers = (clustering_scores <0.7) 
      print(min(clustering_scores))
      print(max(clustering_scores))
      mask_inliers = ~mask_outliers
    #Plot scatter plot to highlight outliers
      plt.scatter(self.emb[mask_inliers, 0], self.emb[mask_inliers, 1],c='blue' , label='inliers')
      plt.scatter(self.emb[mask_outliers, 0], self.emb[mask_outliers, 1], c='red', label='outliers')
      plt.legend()
    elif self.embedding_technique=='pca':
      N=self.n
    

      clustering_scores=[self.score(self.dist[i],self.y_pred[i],N)\
                         for i in list(range(0,len(self.y_pred)))]
    
    

      clustering_scores=np.array(clustering_scores)
      self.clustering_scores=clustering_scores
      mask_outliers = (clustering_scores <0.7) 
      print(min(clustering_scores))
      print(max(clustering_scores))
      mask_inliers = ~mask_outliers
    #Plot scatter plot to highlight outliers
      plt.scatter(self.X_embed[mask_inliers, 0], self.X_embed[mask_inliers, 1],c='blue' , label='inliers')
      plt.scatter(self.X_embed[mask_outliers, 0], self.X_embed[mask_outliers, 1], c='red', label='outliers')
      plt.legend()

  def khd_outlier_visualization(self,a,z):
    """Method to have  look at what images correspond to the outlying points using kmeans
    
    PARAMETERS:
    A:numpy.ndarray
    dummy variable for the data Whose images has to be visualized

    z:numpy.ndarray
    dummy variable for the labels of data through which it can be visualize

    """
    if self.clustering_technique=='kmeans':
      indices=self.clustering_scores.argsort()[::1][:11]
      print(type(indices))
      d = indices.flatten()
      for i in d:
        plt.imshow(a[i])
        plt.title('Number {}'.format(z[i]))
    elif self.clustering_technique=='hdbscan':
      indices=self.clustering_sc.argsort()[::1][:11]
      print(type(indices))
      d = indices.flatten()
      for i in d:
        plt.imshow(a[i])
        plt.title('Number {}'.format(z[i]))
    

  

  def hd_outlier(self):
    """ Method to have outliers identified and visualize using hdbscan"""
    if self.embedding_technique=='umap': 
      clustering_sc=self.clusterer.probabilities_
      self.clustering_sc=clustering_sc
    
      mask_outliers = (clustering_sc < 0.5) 
      mask_inliers = ~mask_outliers
    #Plot scatter plot to highlight outliers
      plt.scatter(self.emb[mask_inliers, 0], self.emb[mask_inliers, 1],c='blue' , label='inliers')
      plt.scatter(self.emb[mask_outliers, 0], self.emb[mask_outliers, 1], c='red', label='outliers')
      plt.legend()
      print(min(clustering_sc))
      print(max(clustering_sc))
    elif self.embedding_technique=='pca': 
      clustering_sc=self.clusterer.probabilities_
      self.clustering_sc=clustering_sc
    
      mask_outliers = (clustering_sc < 0.5) 
      mask_inliers = ~mask_outliers
    #Plot scatter plot to highlight outliers
      plt.scatter(self.X_embed[mask_inliers, 0], self.X_embed[mask_inliers, 1],c='blue' , label='inliers')
      plt.scatter(self.X_embed[mask_outliers, 0], self.X_embed[mask_outliers, 1], c='red', label='outliers')
      plt.legend()
      print(min(clustering_sc))
      print(max(clustering_sc))



  #def hd_outlier_visualization(self,a,z):
    """Method to have  look at what images correspond to the outlying points using hdbscan
    
    PARAMETERS:
    A:numpy.ndarray
    dummy variable for the data Whose images has to be visualized

    z:numpy.ndarray
    dummy variable for the labels of data through which it can be visualize
    
    """

    
    
  @abstractmethod
  def outlier_prediction(self):
    """ abstract method for visualizing outliers on different datsets using scatter plot"""
    pass
  @abstractmethod
  def outlier(self):
    """abstract method for visualizing images with outliers on different datasets"""
    pass

"""#Base class"""

class sub_class(Base_class):

  """
  This class is defined as the inherited class from the
  main class. 
  
  """
  def __init__(self,input_data='cifar10',embedding_technique='pca',clustering_technique='kmeans'):
    super().__init__(input_data, embedding_technique,clustering_technique)
    #self.input_data=input_data
    #self.embedding_technique = embedding_technique
    #self.clustering_technique = clustering_technique

  def display_data(self):


#MNIST DATASET
    if self.input_data=="mnist":
      (x_train, y_train), (x_test, y_test) = mnist.load_data()
      print(f'Shape of training data: {x_train.shape}')
      print(f'Shape of training labels: {y_train.shape}')
      print(f'Number of training samples: {x_train.shape[0]}')
      print(15 * '-')
      print(f'Shape of testing data: {x_test.shape}')
      print(f'Shape of testing labels: {y_test.shape}')
      print(f'Number of testing samples: {x_test.shape[0]}')
      print(15 * '-')
      print(f'Size of images: {x_train.shape[1:4]}')
      
      
      fig, axs = plt.subplots(3, 3, figsize = (12, 12))
      for i, ax in enumerate(axs.flat):
        ax.matshow(x_train[i])
        ax.axis('off')
        ax.set_title('Number {}'.format(y_train[i]))
        x_train = x_train.astype('float32') 
        x_test = x_test.astype('float32')
      #return x_train,x_test,y_train,y_test
      self.x_test=x_test
      self.y_test=y_test
      
    

#CIFAR-10 DATASET
    elif self.input_data=="cifar10":
      (x_train, y_train), (x_test, y_test) = cifar10.load_data()
      print(f'Shape of training data: {x_train.shape}')
      print(f'Shape of training labels: {y_train.shape}')
      print(f'Number of training samples: {x_train.shape[0]}')
      print(15 * '-')
      print(f'Shape of testing data: {x_test.shape}')
      print(f'Shape of testing labels: {y_test.shape}')
      print(f'Number of testing samples: {x_test.shape[0]}')
      print(15 * '-')
      print(f'Size of images: {x_train.shape[1:4]}')
      
      
      sns.countplot(np.squeeze(y_train))
      plt.xlabel('Index of each class')

      index_to_name = {0:'Airplane', 1:'Car', 2:'Bird',
                 3:'Cat', 4:'Deer', 5:'Dog',
                 6:'Frog', 7:'Horse', 8:'Ship',
                 9:'Truck'}
                 #self.index_to_name=index_to_name
      plt.figure(figsize = (10, 9))
      for num, i in enumerate(np.random.randint(x_train.shape[0],size = 9)):
        plt.subplot(3,3, num + 1)
        plt.imshow(x_train[i])
        class_index = np.squeeze(y_train[i][0]).astype(int)
        plt.title(f'{class_index}: {index_to_name[class_index]}')
        plt.axis('off')
        #Resizing the images from 32X32 to 96X96 using tensorflow
      #return x_train,x_test,y_train,y_test
      self.x_test=x_test
      self.Y_test=y_test.reshape(len(y_test))
      self.Y_train=y_train.reshape(len(y_train))


#Make_blobs dataset
    elif self.input_data=="make_blob":
      (x_train,y_train)=make_blobs(n_samples=5000,centers=4,n_features=4,cluster_std=0.3,random_state=4)
      print("Shape of make_blobs dataset:" ,x_train.shape)
      plt.figure(figsize=(9,6))
      plt.scatter(x_train[:,0],x_train[:,1],c=y_train,s=50)
      #return x_train,y_train
    
    else:
            return "Entered input dataset cant be processed"
    self.x_train=x_train
    
    self.y_train=y_train
    
    #x_test,y_train,y_test
    

    

    
    
  def featurize(self):
    if self.input_data=="mnist":
      
      X_train = self.x_train.reshape(len(self.x_train),-1)
      X_test = self.x_test.reshape(len(self.x_test),-1)
      X_train, X_test = X_train / 255.0, X_test / 255.0
      

      print('Shape of training data: ',X_train.shape)
      print('Shape of testing data:' ,X_test.shape)
      self.X_train=X_train
      self.X_test=X_test
  
      
    elif self.input_data=="cifar10":
      #num_classes = 10
      SIZE=96
      ALPHA = 0.75
      model= tf.keras.Sequential([
          tf.keras.layers.InputLayer(input_shape=(SIZE, SIZE, 3,)),
          hub.KerasLayer(f"https://tfhub.dev/google/imagenet/mobilenet_v2_035_96/feature_vector/4",
                   trainable=False),])
      model.build((None,)+(SIZE, SIZE, 3,)) 
      model.summary() 
      model.compile(optimizer="adam", loss="categorical_crossentropy", 
              metrics=["accuracy"])
    
      #return model
      X_p  = tf.keras.applications.mobilenet_v2.preprocess_input(self.x_train, data_format=None)
      print("Dimension of preprocessed images " , X_p.shape)
      X_p_resized= tf.image.resize(
            X_p,
            (SIZE,SIZE),
            method=tf.image.ResizeMethod.BICUBIC,
            preserve_aspect_ratio=False,
            antialias=False,
            name=None)
      self.processed_input= model.predict(X_p_resized)
      print("Shape of data after featurization " , self.processed_input.shape)
        
      #print(self.x_train.shape)
      #X_test=tf.image.resize(self.x_test,size=(96,96),preserve_aspect_ratio=False,antialias=False,name=None)
      #X_train=tf.image.resize(self.x_train,size=(96,96),preserve_aspect_ratio=False,antialias=False,name=None)
      #X_train, X_test = X_train / 255.0, X_test / 255.0
      #print(f'Shape of training data: {X_train.shape}')
      #print(f'Shape of testing data: {X_test.shape}')
      #print(X_test.shape)
      #model=self.get_model()
      #self.processed_input=model.predict(preprocess_input(X_train,data_format=None))
      #print("The shape of cifar10 data after featurization:",self.processed_input.shape)
      


  def embedding(self):

    if self.input_data=='mnist':
      if self.embedding_technique=='pca':
        output_pca=self.pca_embedding(self.X_train,self.y_train)
        print(output_pca)
      elif self.embedding_technique=='umap':
         output_umap=self.umap_embedding(self.X_train,self.y_train)
         print(output_umap)

    elif self.input_data=='cifar10':
      if self.embedding_technique=='pca':
        output_pca=self.pca_embedding(self.processed_input,self.Y_train)
        print(self.Y_train.shape)
        print(output_pca)
      elif self.embedding_technique=='umap':

        output_umap=self.umap_embedding(self.processed_input,self.Y_train)
        print(output_umap)
    else:
      if self.embedding_technique=='pca':
        output_pca=self.pca_embedding(self.x_train,self.y_train)
        print(output_pca)
      elif self.embedding_technique=='umap':

        output_umap=self.umap_embedding(self.x_train,self.y_train)
        print(output_umap)


      



  def clustering(self):

    if self.input_data=='mnist':
      if self.clustering_technique=='kmeans':
        cluster_kmeans=self.k_Clustering(self.y_train)
        print(cluster_kmeans)
      elif self.clustering_technique=='hdbscan':
        cluster_hdbscan=self.hd_Clustering(self.y_train)
        print(cluster_hdbscan)
    elif self.input_data=='cifar10':
      if self.clustering_technique=='kmeans':
        cluster_kmeans=self.k_Clustering(self.Y_train)
        print(cluster_kmeans)
      elif self.clustering_technique=='hdbscan':

        cluster_hdbscan=self.hd_Clustering(self.Y_train)
        print(cluster_hdbscan)
    else:
       if self.clustering_technique=='kmeans':
         cluster_kmeans=self.k_Clustering(self.y_train)
         print(cluster_kmeans)
       elif self.clustering_technique=='hdbscan':
         cluster_hdbscan=self.hd_Clustering()
         print(cluster_hdbscan)



  def outlier_prediction(self):
    if self.input_data=='mnist':
      if self.clustering_technique=='kmeans':
        out_pred_kmeans=self.k_outlier()
        print(out_pred_kmeans)
      elif self.clustering_technique=='hdbscan':
        out_pred_hdbscan=self.hd_outlier()
        print(out_pred_hdbscan)
    elif self.input_data=='cifar10':
      if self.clustering_technique=='kmeans':
        out_pred_kmeans=self.k_outlier()
        print(out_pred_kmeans)
      elif self.clustering_technique=='hdbscan':
        out_pred_hdbscan=self.hd_outlier()
        print(out_pred_hdbscan)
    else:
      if self.clustering_technique=='kmeans':
        out_pred=self.k_outlier()
        print(out_pred_kmeans)
      elif self.clustering_technique=='hdbscan':
        out_pred_hdbscan=self.hd_outlier()
        print(out_pred_hdbscan)



  def outlier(self):
    if self.input_data=='mnist':
      
        out_vis1=self.khd_outlier_visualization(self.x_train,self.y_train)
        print(out_vis1)
    if self.input_data=='cifar10':
      
        out_vis1=self.khd_outlier_visualization(self.x_train,self.y_train)
        print(out_vis1)

"""#Output for different datasets with different embedding and clustering techniques

##MNIST dataset

###1st case when embedding='pca' and clustering='kmeans'
"""

outlier_visualization = sub_class('mnist','pca','kmeans')

outlier_visualization.display_data()
outlier_visualization.featurize()

outlier_visualization.embedding()

outlier_visualization.clustering()

outlier_visualization.outlier_prediction()

outlier_visualization.outlier()

"""###2nd case when embedding='umap' and clustering='hdbscan'"""

outlier_visualization = sub_class('mnist','umap','hdbscan')

outlier_visualization.display_data()
outlier_visualization.featurize()

outlier_visualization.embedding()

outlier_visualization.clustering()

outlier_visualization.outlier_prediction()

outlier_visualization.outlier()

"""##Cifar10 dataset

###1st case when embedding='pca' and clustering='kmeans'
"""

outlier_visualization = sub_class('cifar10','pca','kmeans')

outlier_visualization.display_data()

outlier_visualization.featurize()

outlier_visualization.embedding()

outlier_visualization.clustering()

outlier_visualization.outlier_prediction()

outlier_visualization.outlier()

"""###2nd case when embedding='umap' and clustering='hdbcan'

"""

outlier_visualization = sub_class('cifar10','umap','hdbscan')

outlier_visualization.display_data()

outlier_visualization.featurize()

outlier_visualization.embedding()

outlier_visualization.clustering()

outlier_visualization.outlier_prediction()

outlier_visualization.outlier()

"""##Make_blobs dataset"""

outlier_visualization = sub_class('make_blob','umap','hdbscan')

outlier_visualization.display_data()
outlier_visualization.featurize()

outlier_visualization.embedding()

outlier_visualization.clustering()

outlier_visualization.outlier_prediction()
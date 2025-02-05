import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

def perform_kmeans_clustering(array, n_clusters=3, random_state=None):
    """
    Perform K-Means clustering on the given NumPy array.

    Args:
        array (np.ndarray): The input 2D NumPy array with rows as observations and columns as features.
        n_clusters (int): The number of clusters to form.
        random_state (int, optional): Seed for random number generator for reproducibility.

    Returns:
        np.ndarray: The cluster labels for each data point.
        np.ndarray: The coordinates of the cluster centers.
    """
    # Perform K-Means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    kmeans.fit(array)
    
    # Get the cluster labels and centers
    cluster_labels = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_
    
    return cluster_labels, cluster_centers

def plot_clusters(array, cluster_labels, cluster_centers):
    """
    Plot the data points and the cluster centers on a 2D scatter plot (for 2D data).
    
    Args:
        array (np.ndarray): The input 2D NumPy array with rows as observations and columns as features.
        cluster_labels (np.ndarray): The cluster labels for each data point.
        cluster_centers (np.ndarray): The coordinates of the cluster centers.
    """
    plt.scatter(array[:, 0], array[:, 1], c=cluster_labels, cmap='viridis', marker='o')
    plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1], c='red', marker='x', s=200, label='Centroids')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('K-Means Clustering')
    plt.legend()
    plt.show()

def plot_clusters3D(array, cluster_labels, cluster_centers, x_id=0, y_id=1, z_id=2):
    """
    Plot the data points and the cluster centers on a 2D scatter plot (for 2D data).
    
    Args:
        array (np.ndarray): The input 2D NumPy array with rows as observations and columns as features.
        cluster_labels (np.ndarray): The cluster labels for each data point.
        cluster_centers (np.ndarray): The coordinates of the cluster centers.
    """
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.scatter(array[:, x_id], array[:, y_id], array[:, z_id], c=cluster_labels, cmap='viridis', marker='o')
    ax.scatter(cluster_centers[:, x_id], cluster_centers[:, y_id], cluster_centers[:, z_id], c='red', marker='x', s=200, label='Centroids')
    ax.set_xlabel(fixed_labels[x_id])
    ax.set_ylabel(fixed_labels[y_id])
    ax.set_zlabel(fixed_labels[z_id])
    plt.show()

def perform_pca(array, n_components=None):
    """
    Perform PCA on the given NumPy array, where columns are the independent variables.
    
    Args:
        array (np.ndarray): The input 2D NumPy array with rows as observations and columns as variables.
        n_components (int, optional): The number of principal components to keep. If None, all components are kept.
        
    Returns:
        np.ndarray: The transformed array in the reduced space.
        np.ndarray: The explained variance ratio of each principal component.
    """
    # Standardize the array (important for PCA)
    mean = np.mean(array, axis=0)
    std = np.std(array, axis=0)
    standardized_array = (array - mean) / std
    
    # Perform PCA
    pca = PCA(n_components=n_components)
    transformed_array = pca.fit_transform(standardized_array)
    
    # Return the transformed data and the explained variance ratio
    return transformed_array, pca.explained_variance_ratio_

def sort_columns_by_variance(array):
    """
    Sort the columns of a NumPy array by their variance in descending order.
    
    Args:
        array (np.ndarray): The input 2D NumPy array.
        
    Returns:
        np.ndarray: A new NumPy array with columns sorted by variance.
    """
    # Calculate the variance of each column
    variances = np.var(array, axis=0)
    
    # Get the indices that would sort the variances in descending order
    sorted_indices = np.argsort(variances)[::-1]
    
    # Sort the array columns by the sorted indices
    sorted_array = array[:, sorted_indices]
    
    return sorted_array, sorted_indices

sentiments = np.load('sentiments.npy')


fixed_labels = np.array([
    "anger",
    "fear",
    "neutral",
    "disgust",
    "surprise",
    "sadness",
    "joy"
])


print(sentiments.shape)

sentiments, idx = sort_columns_by_variance(sentiments)
sentiments = sentiments[:, 0:7]


fixed_labels = fixed_labels[idx]

print(fixed_labels[:7])

transformed_array, explained_variance = perform_pca(sentiments, n_components=7)

# Perform K-Means clustering
cluster_labels, cluster_centers = perform_kmeans_clustering(sentiments, n_clusters=10)

# Output cluster labels and centers
print("Cluster Labels:", cluster_labels)
print("Cluster Centers:", cluster_centers)

# Plot the clusters (only works for 2D data visualization)
for i in range(2,7):
    plot_clusters3D(sentiments, cluster_labels, cluster_centers, z_id=i)
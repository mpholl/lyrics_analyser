import numpy as np
import matplotlib.pyplot as plt

plt.style.use('thesisplots')

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



n_bins = 32
sentiment_sum = sentiments.sum(axis=1)
sentiment_sum[np.where(sentiment_sum>0)] = 2
sentiment_sum[np.where(sentiment_sum==0)] = 1
sentiment_sum[np.where(sentiment_sum==2)] = 0

print(sentiment_sum.sum())

for i in range(7):
    tmp_sentiments = sentiments[:, i]
    plt.hist(tmp_sentiments[np.where(tmp_sentiments > 0)], bins=n_bins)
    plt.xlabel(fixed_labels[i])
    plt.tight_layout()
    plt.savefig(f'figures/{fixed_labels[i]}.png', facecolor='white')
    plt.show()

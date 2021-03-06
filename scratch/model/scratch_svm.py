import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
import time



# Create a class of SVM from scratch
class ScratchSVMClassifier():
    """
    Implementation of SVM from scratch

    Parameters
    ----------
    num_iter: int
        The number of iteration

    lr: float
        Learning rate

    threshold: float
        Threshold


    Attributes
    ----------
    self.coef_: ndarray, shape(n_features,)
        parameters

    self.support_vector: ndarray, shape(n_features,RANDOM)
        support vectors

    self.label: ndarray, shape(n_features,RANDOM)
        labels
    """

    def __init__(self, num_iter, lr, threshold):
        # Record hyperparameters as attribute
        self.iter = num_iter
        self.lr = lr
        self.threshold = threshold


    def fit(self, X, y, X_val=None, y_val=None):
        """
        Fit datasets by SVM.

        Parameters
        ----------
        X: ndarray whose shape is (n_samples,n_features)
            Features of train dataset

        y: ndarray whose shape is (n_samples,)
            Correct values of train dataset

        X_val: ndarray whose shape is (n_samples,n_features)
            Features of validation dataset

        y_val: ndarray whose shape is (n_samples,)
            Correct values of validation dataset
        """

        # Change the vectors to a matrix
        y = y.reshape(len(y), 1)
        if y_val is not None:
            y_val = y_val.reshape(len(y_val), 1)

        # Transform arrays to move their features to rows
        X = X.T
        y = y.T
        if (X_val is not None) and (y_val is not None):
            X_val = X_val.T
            y_val = y_val.T

        # Set an initial value of parameter
        self.coef_ = np.full(X.shape[1], 0.00000001)
        self.coef_ = self.coef_.reshape(1, len(self.coef_))

        # Time the processing of updating parameters from here
        t0 = time.time()

        # Update the parameter
        for i in range(self.iter):
            # Update the parameter
            self.coef_ = self._gradient_descent(X, y)
            # Let the parameter fulfill the condition
            self.coef_[self.coef_ < 0] = 0

        # Time it to here
        t1 = time.time()
        print('time : {}s'.format(t1 - t0))

        # Get indexes
        index = np.vstack((self.coef_, self.coef_))

        # Decide support vectors
        self.support_vector = np.delete(X, np.where(index < self.threshold)[1], axis=1)

        # Decide support vectors
        self.label = np.delete(y, np.where(self.coef_ < self.threshold)[1], axis=1)

        # Decide support vectors
        self.coef_ = np.delete(self.coef_, np.where(self.coef_ < self.threshold)[1], axis=1)


    def predict(self, X):
        """
        Prediction

        Parameters
        ----------
        X: ndarray whose shape is (n_samples,n_features)
            Samples


        Returns
        ----------
        ndarray whose shape is (n_samples,1)
            Results of the prediction
        """

        # Transform arrays to move their features to rows
        X = X.T

        # Compute a linear kernel
        linear_kernel = self._linear_kernel(X, self.support_vector)

        # Get the prediction
        y_pred = np.dot(self.label * linear_kernel, self.coef_.T)

        # Classify the prediction
        y_pred[y_pred >= 0] = 1
        y_pred[y_pred < 0] = -1

        # Return the classified prediction
        return y_pred


    # Create a definition to fit datasets by steepest descent method
    def _gradient_descent(self, X, y):
        """
        Fit datasets by steepest descent method

        Parameters
        ----------
        X: ndarray whose shape is (n_samples,n_features)
            train dataset

        y: ndarray whose shape is (n_samples,1)
            correct value


        Returns
        ----------
        ndarray whose shape is (1,)
            parameter(weight)
        """

        # Compute a linear kernel
        linear_kernel = self._linear_kernel(X, X)

        # Compute a metrix of sample labels
        yy = np.dot(y.T, y)

        # Sum
        total = np.dot(yy * linear_kernel, self.coef_.T)

        # Update the parameter
        return self.coef_ + self.lr * (1 - total.T)


    # Compute a linear kernel
    def _linear_kernel(self, X1, X2):
        return np.dot(X1.T, X2)


    # Compute index values
    def compute_index_values(self, X, y):
        """
        Compute Index values.

        Parameters
        ----------
        X: ndarray, shape(n_samples,n_features)
            Features of train dataset

        y: ndarray, shape(n_samples,)
            Correct values of train dataset
        """

        y_pred = self.predict(X)

        # Change values of y to only 2 kinds of values, 0 and 1
        y = [1 if i == max(y) else -1 for i in y]

        # Return index values
        print("accuracy score: ", accuracy_score(y, y_pred))
        print("precision score: ", precision_score(y, y_pred))
        print("recall score: ", recall_score(y, y_pred))
        print("f1 score: ", precision_score(y, y_pred))
        print("confusion matrix:")
        print(confusion_matrix(y, y_pred))


    def decision_boundary(self, X, y, step=0.01, title="Decision Boundary", xlabel="1st Feature", ylabel="2nd Feature",
                          target_names=["setosa", "virginica"]):
        """
        Plot a decision boundary of a model fitting binary classification by 2-dimentional features.

        Parameters
        ----------------
        X : ndarray, shape(n_samples, 2)
            Features of train dataset

        y : ndarray, shape(n_samples,)
            Correct values of train dataset

        step : float, (default : 0.1)
            Set intervals to compute the prediction

        title : str
            Input the title of the graph

        xlabel, ylabel : str
            Input names of each axis

        target_names= : list of str
            Input a list of the legends
        """

        # Setting
        scatter_color = ["r", "b"]
        contourf_color = ["pink", "skyblue"]
        n_class = 2

        # Predict
        mesh_f0, mesh_f1 = np.meshgrid(np.arange(np.min(X[:, 0]) - 0.5, np.max(X[:, 0]) + 0.5, step),
                                       np.arange(np.min(X[:, 1]) - 0.5, np.max(X[:, 1]) + 0.5, step))
        mesh = np.c_[np.ravel(mesh_f0), np.ravel(mesh_f1)]
        pred = self.predict(mesh).reshape(mesh_f0.shape)

        # Plot
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.contourf(mesh_f0, mesh_f1, pred, n_class - 1, cmap=ListedColormap(contourf_color))
        plt.contour(mesh_f0, mesh_f1, pred, n_class - 1, colors='y', linewidths=3, alpha=0.5)

        for i, target in enumerate(set(y)):
            plt.scatter(X[y == target][:, 0], X[y == target][:, 1], s=80, color=scatter_color[i], label=target_names[i],
                        marker='o')

        plt.scatter(self.support_vector[0, :], self.support_vector[1, :], s=80, color="black", marker='o')

        patches = [mpatches.Patch(color=scatter_color[i], label=target_names[i]) for i in range(n_class)]
        plt.legend(handles=patches)
        plt.legend()
        plt.show()
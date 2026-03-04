# Image_Classification_with_CNNs
This project focuses on image classification using Convolutional Neural Networks (CNNs).

The CNN architectures used in this project are based on the paper "On the rate of convergence of image classifiers based on convolutional neural networks" (available at https://arxiv.org/abs/2003.01526).

For this project, several model variants are trained, differing in various hyperparameters, such as the number of hidden layers, neurons per layer, parallel CNNs, convolutional layers, and channels per layer. These models are evaluated on two tasks: first-order classification (detecting whether a particular object is present in an image) and second-order classification (determining if two objects in an image belong to the same category).

Two Python scripts are provided:
- Generate_Dataset.py: Generates synthetic images for both first-order and second-order training tasks.
- Train_Models.py: Trains the models based on defined hyperparameters and saves both the trained weights and the convergence history for subsequent evaluation.

The required dependencies are listed in the requirements.txt file.

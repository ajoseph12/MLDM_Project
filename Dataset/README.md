# Created Dataset

The train dataset was creating by:
- Using 30000 randomly picked instances from the MNIST dataset
- Using 20000 instances generated using an autoencoder 
- Using 10000 instances generated using DCGAN
- train_X - a 60000 x 1 x 28 x 28 tensor : features 
- train_y - a 60000 x 1 tensor : labels
    
The test dataset was created by:
- Using 5000 randomly picked instances from the MNIST dataset
- Using 2500 instances generated using an autoencoder 
- Using 2500 instances generated using DCGAN
- test_X - a 10000 x 1 x 28 x 28 tensor : features 
- test_Y - a 10000 x 1 tensor : labels

The dataset (adjusted for normalization between 0 and 1) can be 
downloaded from this link : https://drive.google.com/open?id=1oIYWlQP9gXKierufI5Gi-cSEPfOmuE5M

The dataset with freemancode generated with label for 60,000 train images can be downloaded from https://drive.google.com/open?id=1A-dfQmsd9tdNWUeqywasIjSQgnIAUy1S


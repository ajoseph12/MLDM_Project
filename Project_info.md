Project Information 
===================

* __Credits__ - 6 - about 120+ hours of work per groupmate
* __Timeline__ - 3.5 months 
* __Report__ - [Scientific Format](https://2017.icml.cc/Conferences/2017/StyleAuthorInstructions) - 8 pages with introduction, SOTA, experimental setup, experimental resutls etc. Use icml template
* __Defence__ - Present what was done and online presentation

Introduction
------------
* __Sequence Mining__ - it's an MLDM project hence we'll implement machine learning and data mining approaches. For mining approaches, sequence mining algorithms must be used. The algo must track the main patterns which are representative of each class of digits. This is done in an unsupervised way as we don't want to learn a classifier, rather only extract the most important patterns. 
* __Metric Learning__ - According to the representation we learn from sequence mining, a metric learning algo should be implemented, eg: apply LMNN - implement at least one algo (implementations exist in matlab and python). During the defence, methodological questions will also be posed.  
* __Deep Learning__ - Used only to generate features/ learn latent space. DO NOT learn classifier. The new features can be used with KNN algo.


Dataset Creation 
----------------

* Dataset ought to be created using one's own environment to create digits. 
* You can also merge created dataset with SOTA dataset like [MNIST](http://yann.lecun.com/exdb/mnist/).
* You can also generate your own datasets using GANZ - adversarial methods.


Dataset Representation
----------------------

* __Structured Method__ - in the form of sequences. We will have to implement an algo based on Freeman's Code (FC).
	- __The Idea__ - you have a matrix of pixels, we begin at the top left of the matrix. Once you meet the 1st pixel, you seek the second one. Once done, look for the corresponding directional primitive of the freeman codes which allows you to go from the first to the second pixel. So as you advance through the pixels you keep encoding the freeman's codes. Once this is done on multiple samples we'll have FC for instances in our dataset. Once this is done, we'll have to use the Nearest Neighbours algo using the edit distance. If we use DNN/CNN/GANZ to create new examples you'll get a numerical representation.
		- ___Attention 1___ - be careful if the digit has two different connected components, or for example if the user falters trying to draw something we must be able to recognize the faulty pixel as noise and ignore it capturing only the principle digit being expressed (a filtering approach is suggested to recognise the single principle component ignoring the noise).
		- ___Attention 2___ - a digit can be represented in multiple sizes (big, small, medium). And considering a digit say '1' written in a _1024x1024_ format, its edit distance with an image created of the digit '1' in a _460x460_ format must be the same (Scaling approaches suggested for this, or even normalizing it).
		- ___Attention 3___ - if the dataset is not representative of digits written in different formats your accuracy is going to suffer, so try reproducing/creating images of different sizes/formats (use GANZ, handcrafted data...etc).
		- ___Attention 4___ - implementing the standard edit distance won't work well. Since edit distance assigns a cost of only '1' the editing, deleting and adding operation, this is bound not to work too well, since performing operations of edit, delete or add within the FC would cost the same for numbers '0' and '4' with are orthogonal. Hence we would need to penalise more the edit distance cost of two very different directional primitives of the FC. So in the worst case scenario, one would have 8 symbols + empty letter (the empty symbol is required to insert/delete). This would make it _9x9_ symbols, i.e 81 possible edit distance cost (there are plenty of scientific papers trying different techniques). 


* __Numerical Method__ - using Deep Learning. 
	- __The Idea__ - If one uses DNN/CNN/GANZ to create new examples a numerical representation of the image is obtainable. On to this a standard KNN with ecludian distance can be applied. It would be ideal to test this numerical represenation with standard ecludain distance and __improve its quality by applying a metric learning algo like LMNN on the numerical representation__. 
		- ___Comment 1___ - Since numerical features are learnt using DNN techniques, non-linearity will be captured and with these features, we'll be able to apply LMNN - a simple linear method. Since the non-linearity would have already been captured by Deep Learning, the algo as a whole should work well. 
		- ___Comment 2___ -There are two different methods to learn representations; deep learning and metric learning. Here, we merge and do both and check if by actually merging we get better results or improve baseline (10% accuracy - the probability of randomly guessing one of the digits). 


Sequence Mining
---------------

*  __The Idea__ - The objective would be to apply the sequence mining algorithm on each category of digits. This should in turn help extract the most interesting patterns characterizing each class of digits.  
	- ___Attention 1___ - imagine we have 2 sequence patterns samples - 1222224.. and 1216224..for a digit say '3'. But for some reason, there is a small noise in one of the three's resulting in a slight change is sequence values. So one must think of a way of filtering this noise so a to predict the right digit - either remove 16 and replace with 2's or the can just be removed. 
	- ___Comment 1___ - A strategy to deal with _Attention 1_ would be, one can consider two patterns to be the same, if the edit distance between patterns one and two is bounded by some threshold. This way we can allow for some edit errors or noise. 
	- ___Comment 2___ - One could use a CNN to learn features to benifit from the the filters that learn to extract patterns. Since the convolutional kernels in a CNN can be seen as a sub-patterns of the digit (filters extract low-high level features of images). Deep Learning could be used to mine for digits . __This method can't be used as a replacement to _Comment 1_ as implementing data data mining approaches is imperative, deep learning is just the cherry on the cake.__ 



Going Further
-------------

* Implement Transfer learning methods. For example, we are two in a group, the only one draws digits for training and the second draw digits for testing. And there's possibly going to be a shift in the distribution between the two and one will need to automatically adapt one's model to this shift.
* KNN is not perfect, we have storage and complexity problems. So we'll have to implement different strategies to overcome these disadvantages (CNN, radial speed up method,.. etc). There exits plenty of algorithms to help over the disadvantages of KNN, so one should evaluate different strategies and compare its performance - in terms of accuracy and time/space complexity - with the baseline (standard KNN) .
* Create something from the designed classifier (possibly the optimal one), like a game of sorts - a calculator for example.


General Comments 
----------------

* Ideally, both the methods - Structured and Numerical - must lead to very good accuracy rates. 
* The objective is to get the best results and it's a competition between groups. __Bonus__ to group with the best accuracy.
* Platform could have an option for downloading own dataset for comparison. 
* Don't have to reimplement LMNN from scratch.
* Report must be done in LATEX.


Reference and Msc Material
--------------------------
* [Open-Source Data Mining Library](http://www.philippe-fournier-viger.com/spmf/)
* [A Taxonomy of Sequential Pattern Mining Algorithms](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.332.4745&rep=rep1&type=pdf)
* [Metric Learning - Python](https://pypi.python.org/pypi/metric-learn)


## Questions and Comments (Please don't change the above text,  if you have any questions, comments or suggestions, please put them below)
* Make the adjustable pointer for writing the digit to increase or decrease the thickness of the digit written. 





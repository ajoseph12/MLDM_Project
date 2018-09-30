Project Information 
===================

* __Credits__ - 6 - about 120+ hours of work per groupmate
* __Timeline__ - 3.5 months 
* __Report__ - [Scientific Format](https://2017.icml.cc/Conferences/2017/StyleAuthorInstructions) - 8 pages with introduction, SOTA, experimental setup, experimental resutls etc. Use icml template
* __Defence__ - Present what was done and online presentation

Intorduction
------------

* __Sequence Mining__ - Hence we'll implement machine learning and data mining approaches. For mining approachs, sequence mining algorithms 
must be used. The algo must track the main patterns which are representative of each class of digits. This is doen in an unsupervised way as we don't want learn a classifier, rather only extract the most important patterns. 
* __Metric Learning__ - According to the repsentation we learn from sequence minig, a metric learning algo should be implemented, eg: apply LMNN - implement at least one algo (implementations exist in matlab and python). During defence, methodological questions will also be posed.  
* __Deep Learning__ - Used only to generate features/ learn latent space. DO NOT learn classifier. The new features can be used with KNN algo.


Dataset Creation 
----------------

* Dataset ought to be created using ones own environment to create digits. 
* You can also merge created dataset with SOTA dataset like [MNIST](http://yann.lecun.com/exdb/mnist/)
* You can also generate your own datasets using GANZ - adverserial methods


Dataset Representation
----------------------

* __Structured Method__ - in the form of sequences. We wiil have to implement an algo based on Freeman's Code (FC).
	- __The Idea__ - you have a matrix of pixels, we begin at the top left of the matrix. Once you meet the 1st pixel, you seek the second one. Once done, look for the corresponding directional primitive of the freeman codes which allows you to go from the 
	first to the second pixel. So as you advance throught the pixels you keep encoding the freeman's codes. Once this is done on multiple samples we'll have FC for instances in our dataset. Once this is done, we'll have to use the Nearest Neighbours algo using the edit distance. If we use DNN/CNN/GANZ to create new examples you'll get a numerical representation.
		- ___Attention 1___ - be careful if the digit has two different connected components, or for example if the user falters trying to draw something we must be able to recognize the fautly pixel as noise and ignore it capturing only the principle digit being expressed (a filtering approach is suggested to recognise the single principle component ignoring the noise).
		- ___Attention 2___ - a digit can be represented in multiple sizes (big, small , medium). And condidering a digit say '1' written in a _1024x1024_ format, its edit distance with an image created of the digit '1' in a _460x460_ format must be the same (Scaling approaches suggested for this, or even normalizing it).
		- ___Attention 3___ - if the dataset is not representative of digits written in different formats your accuracy is going to suffer, so try reproducing/creating images of different sizes/formats (use GANZ, handcrafted data...etc).
		- ___Attention 4___ - implementing the standard edit distance won't work well. Since edit distance assigns a cost of only '1' the editing, deleting and adding operation, this is bound not to work too well, since performing operations of edit, delete or add within the FC would cost the same for numbers '0' and '4' with are orthogonal. Hence we would need to penalise more the edit distance cost of two very different directional primitive of the FC. So in the worst case scenario, one would have 8 symbols + empty letter (the empty symbol is required to insert/delete). This would make it _9x9_ symbols, i.e 81 possible edit distance cost (there are plenty of scientific papers trying differnt techniques). 


* __Numerical Method__ - using Deep Learning. 
	- __The Idea__ - If one uses DNN/CNN/GANZ to create new examples a numerical representation of the image is obtainable. On to this a standard KNN with ecludian distance can be applied. It would be ideal to test these numerical represenation with standard ecludain distance and __improve its quality by applying a metirc learning algo like LMNN on the numerical representation__. 
		- __Comment 1__ - Since numerical features are learnt using DNN techniques, non-linearity will be captured and with these features we'll be able to apply LMNN - a simply linear method. Since the non-linearity would have already been caputred by Deep Learning, the algo as a whole should work well. 
		- __Comment 2__ -There are two different methods to learn representations; deep learning and metric learning. Here, we merge and do both and chech if by actually merging we get better results or improve baseline (10% accuracy - the probabilty of randomly geussing one of the digits). 

General Comments 
----------------

* Implement Transfer learning methods. For example we are two in a group, only one draws digits for training and the second draws digits for testing. And there's possibly going to be a shift in the distribution between the two and one will need to automatically adapt ones model to this shift.
* 



General Comments 
----------------

* Ideally, both the methods - Structured and Numerical - must lead to very good accuracy rates. 
* The objective is to get the best results and it's a competition between groups. __Bonus__ to group with best accuracy.
* Platform could have an option for downloading own dataset for comparison. 








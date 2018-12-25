Handwritten Digit Recognition using Machine Learning, Deep Learning and Metric Learning Approaches 
===============================================================================

Report link : https://www.overleaf.com/2372177757gnmdrmkmngtf 

Please follow instructions (with regard to usage of tenses) in this link while you write your respective parts : https://services.unimelb.edu.au/__data/assets/pdf_file/0009/471294/Using_tenses_in_scientific_writing_Update_051112.pdf

Abstract (Allwyn)
-----------
A brief idea about what exactly is being tackled here.

Introduction (Rohil)
----------------
Check out this link (https://hal.archives-ouvertes.fr/hal-00714509/document) for an idea on how to proceed 

Algorithms 
---------------
* __KNN__ (Rohil) - You'll only need to put up the pseudo-code and talk about the algo in a few lines. (Pseudo-code can be found in the link given in the introduction)
* __CNN__ (Rohil) - Same as with KNN
* __DCGanz__ (Allwyn) - Briefly speak about the algo in general and the loss functions concerning the same, followed by the the DC implementation of the same
* __DCAuto-encoders__ (Allwyn) - Similar to DCGanz (talk about de-noising)
* __LMNN- Metric Learning__ (Rohil) - Talk about why LMNN and the loss function concerning the same

 Dataset and Embeddings (Allwyn)
----------------------------------
* __Dataset__ - talk about the pipeline, the different sections in the pipeline and how did all of it come together (image of pipeline Mnist + DCGanz + Autoencoders)
* __Embeddings__ - talk about the need for embeddings (capture non-linear features) and how did you go about putting it together. Also talk about the fact that you effectuated CNN on it to get most relevant embeddings for later use on structured method, numerical method and RE

Structured Method (Allwyn)
------------------------
* __Idea__  - A rough summary as to what the section is about and what is one trying to achieve here
* __Methodology__ - Describe the scientific/experimental approach employed to arrive at the desired results. Also do talk about the workarounds you came up with to decrease computation time.
* __Results__ - Plot curves  : accuracy (number of neighbours vs accuracy) , time ( computation taken with and without work arounds), and other graphs you can think about

Numerical Method (Rohil)
------------------------
* __Idea__  - A rough summary as to what the section is about and what is one trying to achieve here
* __Methodology__ - Describe the scientific/experimental approach employed to arrive at the desired results. Also do talk about the dilemma faced using LMNN and how to arrived at the best k so as to bring up your accuracy.
* __Results__ - Plot curves  : accuracy (with all data and with strong examples and with increasing K values for LMNN) , time (computation time on all data and strong examples), and other graphs you can think about.
 
Sequence Mining (Nisal)
------------------------
* __Idea__  - A rough summary as to what the section is about and what is one trying to achieve here
* __Methodology__ - Describe the scientific/experimental approach employed to arrive at the desired results. Do put in a few words regarding the idea employed to average patterns and display them.
* __Results__ - Plot patterns for say two numbers and briefly talk about the captured patterns and how number of frequent patterns is a function of the digit (for example, the number 8 will have many more patterns than the number 1)

The GUI (Nisal)
------------------------
Please refer to the link in the introduction to get an idea as to how to proceed here.

Conclusions and Future Work
----------------------------------------
- Future work with numerical method (Allwyn)
- Future work with structured method (Rohil)
- Future work with sequence mining (Nisal)
- Conclusions (Allwyn)
 




# Welcome to the SUAM Project 

SUAM stands for **S**peeding **U**p data **A**nalysis for **M**exico with artificial intelligence and distributed computing. Is a project based on a previous work done and with results being evaluated by a Scientific Committee.

# The SUAM's origin

Concerned about the current situation about the SARS-CoV-2 in Mexico, a group of young, enthusiasts and very capable people decided to start this project.

# Inspired on
The main idea, that is to say, bring some technologies in just one, and also the architecture idea, is based upon an article series: [https://scholar.google.com/citations?user=wpPYUQUAAAAJ&hl=en](https://scholar.google.com/citations?user=wpPYUQUAAAAJ&hl=en)

# About the Project

The SUAM project combines some of the best software (to our knowledge), tools and related technologies in the next fields:

 1. Bioinformatics.
 2. Machine learning (ML). Focused on classification and clusterization.
 3. Deep learning (DL).
 4. Distributed computing (DC).

## Built on top

1. For bioinformatics:
- [Biopython](https://biopython.org/)
- [Clustal Omega](http://www.clustal.org/omega/)
- [MUSCLE](http://www.drive5.com/muscle/)
2. For ML/DL:
 - [Pandas](https://pandas.pydata.org/)
 - [NumPy](https://numpy.org/)
 - [Keras](https://keras.io/)
 - [PyTorch](https://pytorch.org/)
 - [Scikit-learn](https://scikit-learn.org/)
3. For DC:
 - [Ray](https://pypi.org/project/ray/)

## Structure

The project folders are:
 - `bio`. Contains the bioinformatics framework for sequences alignments and it would be intended for future use to, among others: molecular mechanics.
 - `cl`. Stands for classifiers; related to classification problems in ML.
 - `dl`. Framework for DL. Actually supporting: Keras, PyTorch and Scikit-learn.
 - `parsers`. Defines the `JSONParser` class in its `__init__` file. This class is responsible to parse the main JSON configuration file where the tools (for bioinformatics, classification and deep learning) can be specified, and also their parameters.
 - `runners` and `tests`. These folders could be deprecated in future versions (note that each folder -i.e. `bio`, `cl` and `dl` folders-, as required, contains its own folders).
 
In the `bio`, `cl` and `dl` folders you will find, among others, the next two main files:
 - `cfg.json`. Contains the configuration for each tool supported in the project.
 - `requirements.prod`. The Python required modules (remember: run `pip install -r requirements.prod` before anything else) for each case (bioinformatics, classifier and deep learning).

  ## A special case: the `bio` folder
The `bio` folder and its tests is the most advanced in comparison to ML/DL, and this is deliberate, because, in comparison to the  latter, their tools (Clustal Omega and MUSCLE) are not totally tighted to Python.

So, in order to reduce the required time and efforts you will find, in the `bio` folder, the `scripts` folder, where, among others, you will see the `install.sh` file. Please run this file to be able to execute Clustal Omega and MUSCLE, which are dependencies for the SUAM's bioinformatics framework.

Finally, as we said, the `bio` folder contains `tests` and their `results` (in its named folders).

# What's next?

 1. Nowadays we are working with a new (second) paper with the first results from our experiments and we expect to release the architecture first version in these days.
 2. Build and run the tests sets for ML/DL.
 3. Analyse the results of the step above.
 4. Start a new article.

## Colaborators

We're looking for young, enthusiasts and very capable people, software engineers, data scientists, computing specialists, information technologies(IT) specialists, on the levels: student (more than the 50% from curricula approved) and/or engineer.

If you believe that can help on this please write to: [suamproject@gmail.com](mailto:ram.le.dario@gmail.com?subject=SUAM Colaborator "suamproject@gmail.com") 

## Sponsors / Partially funded by

Not actually looking for money, right now we're looking devices to build a devices cluster for the data processing. Do you have an old machine and you can't sell it? Do you have an old machine and do you want to dispose it? Don't sell it, don't dispose it, donate it for the project.

If you believe that can help on this please write to: [suamproject@gmail.com](mailto:ram.le.dario@gmail.com?subject=SUAM Sponsor "suamproject@gmail.com") 

## Supported by

Are you a small-medium size organization? Would you like that your company logo appear in the project's site, or its derivated works?

If you believe that can help on this please write to: [suamproject@gmail.com](mailto:ram.le.dario@gmail.com?subject=SUAM Supporter "suamproject@gmail.com") 

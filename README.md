# Using Numenta's Hierachical Temporal Memory algorithm to classify EEG data
*NB: EEG is the recording of electrical activity along the scalp - in other words, brainwaves :-)*

## Motor Imagery Classification (NuPIC Fall 2014 [Hackathon](http://www.meetup.com/numenta/events/202402962/))
* `motor_imagery` contains the code for EEG motor imagery classification.
* EGG data was recorded around the motor cortex. 
* The signals were recorded with a 8 channels EEG and [OpenBCI](www.openBCI.com) board.
* There are 3 phases: no movement, left hand, right hand.
* The sampling rate is 4 ms.
* This classifier was made at the Numenta Hackathon (NuPIC Fall 2014 Hackathon) where I gave a little demo.
* See **[demo slides](https://docs.google.com/presentation/d/1wFWSk4P3yHDkPzV19Q0sZYX9NhwvEBLJQQXKh0eyZws/edit?usp=sharing)** and **[video](http://www.youtube.com/watch?v=UEh48KOmkIA)**.

## Seizure Detection
* `seizure_detection` uses Numenta's HTM to detect anomalies (slow waves in the EEG signal).
* Detecting these anomalies accurately makes it possible to predict seizures so that they can be avoided.
* The datasets are too big to be uploaded. They can be found on [Kaggle](https://www.kaggle.com/c/seizure-prediction) "American Epilepsy Society Seizure Prediction Challenge".
* Work in collaboration with [Nicolas Thiebaud](https://github.com/nt) and Dr. Richard Pantera.
* Disclaimer: I am not participating in the Kaggle competition. The code in `seizure_detection` was only used to learn more about EEG data analysis :-)

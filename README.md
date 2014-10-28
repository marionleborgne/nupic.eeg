# Using Numenta's Hierachical Temporal Memory algorithm to classify EEG data
Note: EEG is the recording of electrical activity along the scalp - in other words, brainwaves :-)

## Motor Imagery
* `motor_imagery` contains the code for EEG motor imagery classification.
* EGG data was recorded around the motor cortex. Setup:
** Signal recorded with a 8 channels EEG board (www.openBCI.com)
** 3 phases: no movement, left hand, right hand
** Sampling rate: 4 ms
* This classifier was made at the Numenta Hackathon (NuPIC Fall 2014 Hackathon) where I gave a little demo:
** Slides: https://docs.google.com/presentation/d/1wFWSk4P3yHDkPzV19Q0sZYX9NhwvEBLJQQXKh0eyZws/edit?usp=sharing
** Video: http://www.youtube.com/watch?v=UEh48KOmkIA

## Kaggle Competition (with Nicolas Thiebaud)
* `kaggle` contains code for the "American Epilepsy Society Seizure Prediction Challenge"
* The idea was to use Numenta's HTM to detect anomalies (slow waves in the EEG signal)
* Detecting these anomalies accurately makes it possible to predict seizures so that they can be avoided.
* See competition on [https://www.kaggle.com/c/seizure-prediction][Kaggle]

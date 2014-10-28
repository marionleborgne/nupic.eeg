__author__ = 'marion'

import os
from dataset import DataSet
from nupic.frameworks.opf.modelfactory import ModelFactory
from model_params import MODEL_PARAMS

CWD = os.path.abspath(os.getcwd())

preictal = DataSet('data/datasets/Dog_1/Dog_1_preictal_segment_0006.mat', 4)
interictal = DataSet('data/datasets/Dog_1/Dog_1_interictal_segment_0323.mat')


# train model for interictal phase
inter_model = ModelFactory.create(MODEL_PARAMS)
anomaly_interictal = [inter_model.run({"channel1": float(r)}).inferences['anomalyScore'] for r in interictal.data[0]]
inter_model.disableLearning()

# train model for preictal phase
preict_model = ModelFactory.create(MODEL_PARAMS)
anomaly_preictal = [preict_model.run({"channel1": float(r)}).inferences['anomalyScore'] for r in preictal.data[0]]
preict_model.disableLearning()

# save models
modelDir = "%s/inter_model" % CWD
inter_model.save(modelDir)
print "Saved new model in %s" % modelDir

modelDir = "%s/preict_model" % CWD
preict_model.save(modelDir)
print "Saved new model in %s" % modelDir



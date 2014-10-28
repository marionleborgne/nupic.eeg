__author__ = 'marion'

import os
from dataset import DataSet
from nupic.frameworks.opf.modelfactory import ModelFactory
CWD = os.path.abspath(os.getcwd())

# load preict model and disable learning
model_dir = "%s/preict_model" % CWD
preict_model = ModelFactory.loadFromCheckpoint(model_dir)
preict_model.disableLearning()

# load interict model and disable learning
model_dir = "%s/inter_model" % CWD
interict_model = ModelFactory.loadFromCheckpoint(model_dir)
interict_model.disableLearning()

# load test data
preictal_test = DataSet('data/datasets/Dog_1/Dog_1_test_segment_0006.mat', 4)

# run it through the 2 models
anomaly_interictal = [interict_model.run({"channel1": float(r)}).inferences['anomalyScore'] for r in preictal_test.dataForSeconds(0,60)[0]]
anomaly_preictal = [preict_model.run({"channel1": float(r)}).inferences['anomalyScore'] for r in preictal_test.dataForSeconds(0,60)[0]]

avg_anomaly_pre = sum(anomaly_interictal) / len(anomaly_interictal)
avg_anomaly_inter = sum(anomaly_preictal) / len(anomaly_preictal)


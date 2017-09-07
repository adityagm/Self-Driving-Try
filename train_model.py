# train_model

import numpy as np
from alexnet_theano import alexnet

width = 80
height = 60
lr = 1e-3 #learning rate
epochs = 8
#vaiables so that overtime we can have epochs and change things but we want to keep the model as it trains and then we want to save the model
model_name = 'self-driving car-{}-{}-{}-epcohs.model'.format(lr, 'alexnetv2', epochs)
model = alexnet_theano(width, height, lr)

train = trainData[:500]
test = trainData[-500:]

x = np.array([i[0] for i in train]).reshape(-1,width,height,1)
y = [i[1] for i in train]


test_x = np.array([i[0] for i in test]).reshape(-1,width,height,1)
test_y = [i[1] for i in test]

model.fit({'input':x},{'targets':y},n_epochs=epochs, validation_set=({'input': test_x},{'targets': test_y}), snapshot_step=500, show_metric=True, run_id=MODEL_NAME)

# tensorboard -- log dir

model.save(model_name)

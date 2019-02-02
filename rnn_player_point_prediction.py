import tensorflow as tf
import pandas as pd
import numpy as np

#tf.enable_eager_execution()

df = pd.read_csv("/tmp/player_box.csv")

player = df[df['player_id'] == 2082634.0]

player_info = player.loc[:, 'pts':'mins_played':1]

x = player_info[1:]

y = player_info.loc[:, 'pts'][:-1]

x = x.iloc[::-1]
y = y.iloc[::-1]

xtensor = tf.convert_to_tensor(x.values, dtype = tf.float32)
ytensor = tf.convert_to_tensor(y.values, dtype = tf.float32)

xtensor = tf.reshape(xtensor, (9, 1, 17))
ytensor = tf.reshape(ytensor, (9, 1, 1))

xtensor = tf.math.l2_normalize(
    xtensor,
    axis=(0,1)
)
ytensor = tf.math.l2_normalize(
    ytensor,
    axis=(0,1)
)


print(xtensor.shape, ytensor.shape)
print(xtensor)

tf.reshape(y[0], (1,1))

lstm = tf.contrib.rnn.BasicLSTMCell(17)

initial_state = state = lstm.zero_state(1, dtype=tf.float32)

dense1 = tf.layers.Dense(units = 1)

loss = 0
for i in range(9):
    output, state = lstm(xtensor[i], state)
    logits = dense1(output)
    
    loss += tf.nn.sigmoid_cross_entropy_with_logits(labels=ytensor[i], logits=logits)    

final_state = state
print(loss)

import tensorflow as tf
from tensorflow.contrib import rnn


'''
To classify images using a recurrent neural network, we consider every image
row as a sequence of pixels. Because MNIST image shape is 28*28px, we will then
handle 28 sequences of 28 steps for every sample.
'''

# Training Parameters
learning_rate = 0.001
training_steps = 10000
batch_size = 1
display_step = 200

# Network Parameters
num_input = 17
timesteps = 9 # timesteps
num_hidden = 128 # hidden layer num of features
num_scores = 1 

# tf Graph input
X = tf.placeholder("float", [None, timesteps, num_input])
Y = tf.placeholder("float", [None, num_scores])

# Define weights
weights = {
    'out': tf.Variable(tf.random_normal([num_hidden, num_scores]))
}
biases = {
    'out': tf.Variable(tf.random_normal([num_scores]))
}


def RNN(x, weights, biases):

    # Prepare data shape to match `rnn` function requirements
    # Current data input shape: (batch_size, timesteps, n_input)
    # Required shape: 'timesteps' tensors list of shape (batch_size, n_input)

    # Unstack to get a list of 'timesteps' tensors of shape (batch_size, n_input)
    x = tf.unstack(x, timesteps, 1)

    # Define a lstm cell with tensorflow
    lstm_cell = rnn.BasicLSTMCell(num_hidden, forget_bias=1.0)

    # Get lstm cell output
    outputs, states = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)

    # Linear activation, using rnn inner loop last output
    return tf.matmul(outputs[-1], weights['out']) + biases['out']

logits = RNN(X, weights, biases)
prediction = tf.nn.sigmoid(logits)

# Define loss and optimizer
loss_op = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(
    logits=logits, labels=Y))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
train_op = optimizer.minimize(loss_op)

# Evaluate model (with test logits, for dropout to be disabled)
correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# Initialize the variables (i.e. assign their default value)
init = tf.global_variables_initializer()



# Start training
with tf.Session() as sess:

    # Run the initializer
    sess.run(init)

    for step in range(1, training_steps+1):
        batch_x, batch_y = (x.values,y.values)  ######mnist.train.next_batch(batch_size)
        # Reshape data to get 28 seq of 28 elements
        batch_x = batch_x.reshape((batch_size, timesteps, num_input))
        batch_y = batch_y.reshape((timesteps, num_scores))
        # Run optimization op (backprop)
        sess.run(train_op, feed_dict={X: batch_x, Y: batch_y})
        if step % display_step == 0 or step == 1:
            # Calculate batch loss and accuracy
            loss, acc = sess.run([loss_op, accuracy], feed_dict={X: batch_x,
                                                                 Y: batch_y})
            print("Step " + str(step) + ", Minibatch Loss= " + \
                  "{:.4f}".format(loss) + ", Training Accuracy= " + \
                  "{:.3f}".format(acc))

    print("Optimization Finished!")

    # Calculate accuracy for 128 mnist test images
    test_len = 1
    test_data = x.values.reshape(1,9,17)
    test_label = y.values.reshape(9,1)
    print("Testing Accuracy:", \
        sess.run(accuracy, feed_dict={X: test_data, Y: test_label}))

ytest = list(player_info.loc[:, 'pts'][:-1])
#print(ytest)
s = 0
alpha = 0.7
average = 0
for i in range(0,9-1):
    s = alpha * s + (1-alpha) * ytest[i]
    average += abs(s - ytest[i+1])/(max(ytest[i+1], s))
average /= 9
print('exponential average estimation accuracy')
print(average)
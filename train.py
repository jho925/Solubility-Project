import torch
import pandas as pd
from sklearn.model_selection import train_test_split
from solubilitynn import GCN
import numpy as np
from solubility import solubility_pp

# torch.set_default_tensor_type('torch.LongTensor')
df = pd.read_csv('delaney.csv')
y_all = df['logp']
x_all = df.drop('logp',axis = 1)
x_train, x_test, y_train, y_test = train_test_split(x_all, y_all)

x_train, y_train = np.array(x_train), np.array(y_train)

def get_features(x):
    return np.array([solubility_pp(e[0]) for e in x])

model = GCN() # TODO

loss_fn = torch.nn.MSELoss() # is this the correct loss that you want to use?

optimizer = torch.optim.Adam(model.parameters(), lr=0.0001) # feel free to play around with this

n_epochs = 10 # or whatever
batch_size = 1 # or whatever

for epoch in range(n_epochs):
    print(epoch)
    # X is a torch Variable
    permutation = torch.randperm(int(x_train.size))

    for i in range(0, int(x_train.size), batch_size):
        optimizer.zero_grad()

        indices = permutation[i:i+batch_size]
        a2b, b2a, b2revb, f_bonds, f_atoms, bond_sum = solubility_pp(x_train[indices][0])
        batch_y = torch.FloatTensor(np.array([y_train[indices]]))

        outputs = model.forward(a2b, b2a, b2revb, f_bonds, f_atoms, bond_sum)
        loss = loss_fn(outputs, batch_y)

        loss.backward()
        optimizer.step()
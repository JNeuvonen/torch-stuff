import pandas as pd
import net.main as net
import torch
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import matplotlib.pyplot as plt


train_data = pd.read_csv('processed-data')
train_data = train_data.dropna()


y = train_data['TARGET']
x = train_data.drop('TARGET', axis=1)


model = net.NeuralNet(x.shape[1], 2, 1)
criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters())
costs = []
NUM_EPOCHS = 10
BATCH_SIZE = 64

x = x.to_numpy()
x = torch.from_numpy(x)
x = x.to(torch.float32)

y = y.to_numpy()
y = torch.from_numpy(y)
y = y.to(torch.float32)
y = y.reshape(len(y), 1)

x = torch.nn.functional.normalize(x)
y = torch.nn.functional.normalize(y)


dataset = TensorDataset(x, y)
dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# Train the model
for epoch in range(NUM_EPOCHS):

    epoch_loss = 0

    for id_batch, (x_batch, y_batch) in enumerate(dataloader):
        # Forward pass
        outputs = model(x_batch)

        loss = criterion(outputs, y_batch)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()
        print(epoch_loss)

    print(f'Epoch {epoch+1}: loss = {epoch_loss:.5f}')
    costs.append(epoch_loss)


torch.save(model, 'model.pt')

plt.plot(np.arange(NUM_EPOCHS), costs)
plt.show()

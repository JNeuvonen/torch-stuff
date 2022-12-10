import torch
import pandas as pd

model = torch.load('model.pt')

train_data = pd.read_csv('test-data')
train_data = train_data.dropna()

y = train_data['TARGET']
x = train_data.drop('TARGET', axis=1)

x = x.to_numpy()
x = torch.from_numpy(x)
x = x.to(torch.float32)

y = y.to_numpy()
y = torch.from_numpy(y)
y = y.to(torch.float32)
y = y.reshape(len(y), 1)


predictions = model(x)

predictions_arr = predictions.detach().numpy()

predictions_df = pd.DataFrame(predictions_arr)

idxmin = predictions_df.idxmin()

print(x[idxmin][0])

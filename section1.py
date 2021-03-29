import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as f


x = Variable(torch.Tensor([[25], [45], [50], [20], [60]]))
y = Variable(torch.Tensor([[0], [1], [1], [0], [1]]))


class LogisticRegressionModel(nn.Module):
    def __init__(self, input_size, output_size):
        super(LogisticRegressionModel, self).__init__()
        self.linear = nn.Linear(input_size, output_size)

    def forward(self, x):
        y_predict = f.sigmoid(self.linear(x))
        return y_predict


model = LogisticRegressionModel(1, 1)
criteria = nn.BCELoss()
optimizer = optim.SGD(model.parameters(), 0.001)

for epoch in range(1000):
    y_predict = model(x)
    loss = criteria(y_predict, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    print(epoch, loss.item())

test = Variable(torch.Tensor([[20]]))
z = model.forward(test)
print(float(z.data[0]))
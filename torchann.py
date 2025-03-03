#import dependencies
import torch
from torchvision import datasets
from PIL import Image
from torch.optim import Adam
from torch import nn, save, load
from torch.utils.data import DataLoader
from torchvision.transforms import ToTensor





#get data

train = datasets.MNIST(root='data', download=True,train=True, transform=ToTensor())
dataset = DataLoader(train,32)


#Image classifier neural newtwork

class ImageClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Conv2d(1,32,(3,3)),
            nn.ReLU(),
            nn.Conv2d(32, 64, (3, 3)),
            nn.ReLU(),
            nn.Conv2d(64, 64, (3, 3)),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(64*(28-6)*(28-6),10)
        )

    def forward(self,x):
        return  self.model(x)



# Instance of the neural network, loss, optimizer
clf = ImageClassifier().to('cpu')
optim = Adam(clf.parameters(),lr=1e-3)
loss_fn=nn.CrossEntropyLoss()

# Training flow

if __name__ == '__main__':
  for epoch in range(10):
      for batch in dataset:
          X,y=batch
          X, y = X.to('cpu'), y.to('cpu')
          yhat= clf(X)
          loss = loss_fn(yhat,y)

          # Apply backprop
          optim.zero_grad()
          loss.backward()
          optim.step()

      print(f"Epoch:{epoch} loss is {loss.item()}")

  with open('model_state.pt', 'wb') as w:
      save(clf.state_dict(),w)

  with open('model_state.pt', 'rb') as w:
      clf.load_state_dict(load(w))


  img = Image.open('img_1.jpg')
  imgTensor = ToTensor()(img).unsqueeze(0)
  print(torch.argmax(clf(imgTensor)))













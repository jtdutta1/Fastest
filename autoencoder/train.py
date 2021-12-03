from typing import final
import torch
from model import EncoderDecoder
import numpy as np
from torch.utils.data import DataLoader
from torch.nn import MSELoss
from torch.optim import Adam, SGD
from torchvision import datasets, transforms

# def collate_fn(data):
#     imgs, label = [i[0] for i in data], [i[1] for i in data]
#     imgs = torch.tensor(imgs).float()
#     imgs = imgs.reshape(imgs.shape[0], -1)
#     label = torch.tensor(label).float()
#     print(imgs.shape)
#     print(label.shape)

def main():
    # Check if cuda is available
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    transform = transforms.Compose([transforms.ToTensor()])
    # Create the train test split
    # Automatically download if missing
    train_data = datasets.MNIST(root="data", 
                                train=True, 
                                transform=transform, 
                                download=True)
    val_data = datasets.MNIST(root="data",
                              train=False,
                              transform=transform,
                              download=True)
    
    # Create dataloaders
    train_loader = DataLoader(train_data,
                              batch_size=32,
                              shuffle=True)
    val_loader = DataLoader(val_data,
                            batch_size=32,
                            shuffle=False)
    
    # Define model, loss function and optimizer 
    net = EncoderDecoder()
    net.to(device)
    epochs=10
    optimizer = Adam(net.parameters(), lr=0.001, weight_decay=1e-7)
    loss_fn = MSELoss(reduction="mean")
    
    # Training loop
    for i in range(epochs):
        # print(i)
        print("Epoch {}/{}".format(i + 1, epochs))
        epoch_loss = []
        counter = 0
        for imgs, labels in train_loader:
            imgs = imgs.to(device)
            labels = labels.to(device)
            imgs = imgs.reshape(imgs.shape[0], -1)
            # print(imgs.device)
            # print(labels.device)
            counter += 1
            # print(features.shape)
            # print(labels)
            # print(labels.dtype)
            y_pred = net(imgs)
            # print(y_pred.dtype)
            # print(y_pred)
            loss = loss_fn(imgs, y_pred)
            epoch_loss.append(loss.item())
            # with torch.no_grad():
                # acc = accuracy_score(labels.view(-1).cpu(), y_pred.view(-1).cpu())
            print("{}/{}. Train Loss: {:.2f}".format(counter, len(train_data)//32, loss.item()), end="\r")
            # print(loss.dtype)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        
        epoch_loss = np.array(epoch_loss)
        print()
        print("Checking val loss")
        val_loss = []
        counter = 0
        for imgs, labels in val_loader:
            imgs = imgs.to(device)
            labels = labels.to(device)
            imgs = imgs.reshape(imgs.shape[0], -1)
            counter += 1
            # print(features.shape)
            # print(labels)
            # print(labels.dtype)
            with torch.no_grad():
                y_pred = net(imgs)
                loss = loss_fn(imgs, y_pred)
                val_loss.append(loss.item())
                print("{}/{}. Train Loss: {:.2f}".format(counter, len(val_data)//32, loss.item()), end="\r")
        print()
        val_loss = np.array(val_loss)
        print("Training loss epoch: {:.2f}\tValidation loss: {:.2f}".format(epoch_loss.mean(), val_loss.mean()))
    
    # Save model
    torch.save(net, "model.pth")

if __name__ == "__main__":
    main()
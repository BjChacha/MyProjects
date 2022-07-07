import torch
import numpy as np
from gol import next_frame

def create_set(H, W, sparse, length):
    x = (np.random.rand(length, H, W) > 0.5).astype(float)
    y = np.empty_like(x)
    
    for i in range(length):
        y[i] = next_frame(x[i])

    return x, y


def main():
    
    H = 10
    W = 10
    sparse = 0.1
    
    x, y = create_set(H, W, sparse, 100)
    x, y = torch.tensor(x, dtype=torch.float), torch.tensor(y, dtype=torch.float)
    D_in, H, D_out = H*W, 1000, H*W
    model = torch.nn.Sequential(
        torch.nn.Linear(D_in, H),
        torch.nn.ReLU(),
        torch.nn.Linear(H, D_out)
    )

    epochs = 10
    learning_rate = 1e-3

    loss_fn = torch.nn.MSELoss(reduction='sum')
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

    # x, y = torch.tensor(x), torch.tensor(y)

    for e in range(epochs):
        for i in range(x.shape[0]):
            x[i] = torch.flatten(x[i])
            y_pred = model(x[i])
            y_pred = torch.flatten(y_pred)
            loss = loss_fn(y_pred, y[i])
            print(e, loss.item())

            model.zero_grad()
            loss.backward()
            optimizer.step()


def debug():
    layer = torch.nn.Flatten()

    x = np.random.rand(5, 5)
    # x = torch.tensor(x)
    print(x.shape)
    # y = layer(x)
    y = torch.flatten(x)
    print(y.shape)
    
if __name__ == "__main__":
    main()
    # debug()
from programs import JC
import json
import torch
import pdb


## First-Byte Dependent
class FBDModel:
    def __init__(self, D_in):
        H = max(5, int(D_in / 2))
        
        self.nn = torch.nn.Sequential(
                    torch.nn.Linear(D_in, H),
                    torch.nn.Softplus(5),
                    torch.nn.Linear(H, H),
                    torch.nn.Softplus(5),
                    torch.nn.Linear(H, H),
                    torch.nn.Softplus(5),
                    torch.nn.Linear(H, 1),
                    torch.nn.Softplus(5))

    def train(self, x, y):
        epoch=400
        batch_size=100
        lr=0.1
        loss_func=torch.nn.MSELoss(reduction='mean')
        
        print_freq = 20
        save_freq = 20
        save_path='models/first_byte_dependent.pl'

        self.nn = train_model(self.nn, x, y, epoch, lr, batch_size, loss_func, print_freq, save_freq, save_path)

## First-Byte Value Dependent
class FBVDModel:
    def __init__(self, D_in):
        H = max(5, int(D_in / 2))
        
        self.nn = torch.nn.Sequential(
                    torch.nn.Linear(D_in, H),
                    torch.nn.Softplus(5),
                    torch.nn.Linear(H, H),
                    torch.nn.Softplus(5),
                    torch.nn.Linear(H, H),
                    torch.nn.Softplus(5),
                    torch.nn.Linear(H, 1),
                    torch.nn.Sigmoid())

    def train(self, x, y):
        y = y.reshape(len(y))
        
        epoch=400
        batch_size=100
        lr=0.1
        loss_func=torch.nn.BCELoss()
        
        print_freq = 20
        save_freq = 20
        save_path='models/first_byte_value_dependent.pl'

        self.nn = train_model(self.nn, x, y, epoch, lr, batch_size, loss_func, print_freq, save_freq, save_path)

## Two-Byte Partial Dependence
class TBPDModel:
    def __init__(self, D_in):
        H = max(5, int(D_in / 2))
        
        self.nn = torch.nn.Sequential(
                    torch.nn.Linear(D_in, H),
                    torch.nn.Softplus(5),
                    torch.nn.Linear(H, H),
                    torch.nn.Softplus(5),
                    torch.nn.Linear(H, H),
                    torch.nn.Softplus(5),
                    torch.nn.Linear(H, 1),
                    torch.nn.Softplus(5))

    def train(self, x, y):
        epoch=400
        batch_size=100
        lr=0.1
        loss_func=torch.nn.MSELoss(reduction='mean')
        
        print_freq = 20
        save_freq = 20
        save_path='models/two_byte_partial_dependance.pl'

        self.nn = train_model(self.nn, x, y, epoch, lr, batch_size, loss_func, print_freq, save_freq, save_path)


class JCModel:
    def __init__(self, D_in=40):
        H = 80
                
        self.nn = torch.nn.Sequential(
                    torch.nn.Linear(D_in, H),
                    torch.nn.Softplus(5),
                    torch.nn.Linear(H, H),
                    torch.nn.Softplus(5),
                    torch.nn.Linear(H, D_in),
                    torch.nn.Softplus(5),
                    torch.nn.Linear(D_in, 1),
                    torch.nn.Sigmoid())

    def words_to_ascii(words):
        t = list()
        for word in words:
            for c in word:
                if c == ' ':
                    t.append(0.0)
                else:
                    t.append(ord(c)/256)

        return t

    def train(self, x, y):
        y = y.reshape(len(y))
        
        epoch=400
        batch_size=100
        lr=0.1
        loss_func=torch.nn.BCELoss()
        
        print_freq = 20
        save_freq = 20
        save_path='models/json_compare.pl'

        self.nn = self.train_model(self.nn, x, y, epoch, lr, batch_size, loss_func, print_freq, save_freq, save_path)


## Training Function
def train_model(model, x, y, nepochs, learning_rate, batch_size, loss_func, print_freq=1000, save_freq=None, save_path=None):

    print("Training ...")

    loss_fn = loss_func

    decayRate = 0.975
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    lr_scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer=optimizer, gamma=decayRate)

    N = x.shape[0]
    for epoch in range(nepochs):
        rperm = torch.randperm(N)
        x_perm = x[rperm]
        z_perm = y[rperm]
        for i in range(0, N, batch_size):
            xb = x_perm[i:i+batch_size]
            zb = z_perm[i:i+batch_size]
            z_pred = model(xb)
            loss = loss_fn(z_pred, zb)
            model.zero_grad()
            loss.backward()
            optimizer.step()
            
        lr_scheduler.step()

        if epoch % print_freq == 0:
            print(f'Epoch: {epoch}, Loss: {loss.item()}')
        if save_freq is not None and save_path is not None and epoch % save_freq == 0:
            print('Saving Model')
            torch.save(model.state_dict(), save_path)

    return model


from torch_geometric.nn import GCNConv, SAGEConv
from nni.nas.pytorch import mutables
import torch.nn as nn

class BaseNAS:
    def search(self, space, dset, trainer):
        """
        The main process of NAS.
        Parameters
        ----------
        space : BaseArchitectureSpace
            No implementation yet
        dataset : ...datasets
            Dataset to train and evaluate.
        trainer : ..train.BaseTrainer
            Including model, giving HP space and using for training

        Returns
        -------
        model: ..train.BaseTrainer
            The trainer including the best trained model
        """

class GraphSpace(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, ops, *arg, **kwargs):
        super().__init__()
        """self.op1 = mutables.LayerChoice([GCNConv(input_dim, hidden_dim),SAGEConv(input_dim, hidden_dim)])
        self.op2 = mutables.LayerChoice([
            GCNConv(hidden_dim, output_dim),
            SAGEConv(hidden_dim, output_dim)       
        ], key = "2")"""
        self.op1 = mutables.LayerChoice([op(input_dim, hidden_dim) for op in ops])
        self.op2 = mutables.LayerChoice([op(hidden_dim, output_dim) for op in ops])

    def forward(self, data):
        x = self.op1(data.x, data.edge_index)
        x = self.op2(x, data.edge_index)
        return x
        
class BaseEstimator:
    def infer(self, model, dataset):
        dset = dataset[0]
        pred = model(dset)[dset.train_mask]
        y = dset.y[dset.train_mask]
        loss_func = nn.CrossEntropyLoss()
        loss = loss_func(pred, y)
        return loss, loss
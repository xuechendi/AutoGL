import sys
sys.path.append('../')
from torch_geometric.nn import GCNConv
import torch
from autogl.datasets import build_dataset_from_name
from autogl.solver import AutoNodeClassifier
from autogl.module.train import NodeClassificationFullTrainer
from autogl.module.nas import Darts, OneShotEstimator, SinglePathNodeClassificationSpace
from autogl.module.nas.space.graph_nas import GraphNasNodeClassificationSpace
from autogl.module.train import Acc
from autogl.module.nas.algorithm.enas import Enas

if __name__ == '__main__':
    dataset = build_dataset_from_name('cora')
    solver = AutoNodeClassifier(
        feature_module='PYGNormalizeFeatures',
        graph_models=[],
        hpo_module=None,
        ensemble_module=None,
        default_trainer=NodeClassificationFullTrainer(
            optimizer=torch.optim.Adam,
            lr=0.01,
            max_epoch=300,
            early_stopping_round=300,
            weight_decay=1e-4,
            device="auto",
            init=False,
            feval=['acc'],
            loss="nll_loss",
            lr_scheduler_type=None,),
        #nas_algorithms=[Enas()],
        nas_algorithms=[Darts(num_epochs=200)],
        #nas_spaces=[SinglePathNodeClassificationSpace(hidden_dim=32, ops=[GCNConv, GCNConv])],
        nas_spaces=[GraphNasNodeClassificationSpace(hidden_dim=64,search_act_con=False,layer_number=4)],
        nas_estimators=[OneShotEstimator()]
    )
    solver.fit(dataset)
    solver.get_leaderboard().show()
    out = solver.predict_proba()
    print('acc on cora', Acc.evaluate(out, dataset[0].y[dataset[0].test_mask].detach().numpy()))

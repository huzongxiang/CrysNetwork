# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 16:50:25 2022

@author: huzon
"""


import warnings
import logging
from pathlib import Path
import numpy as np
import tensorflow as tf
from matdgl.data import Dataset
from matdgl.models import GNN
from matdgl.data.generator import GraphGenerator
from matdgl.models.graphmodel import GraphModel, MpnnModel, TransformerModel


tf.get_logger().setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

np.random.seed(52)
tf.random.set_seed(52)

ModulePath = Path(__file__).parent.absolute()

print('reading dataset...')
dataset = Dataset(task_type='e_above_hull', data_path=ModulePath)
print('done')
print(dataset.dataset_file)

BATCH_SIZE = 64
DATA_SIZE = 60000
CUTOFF = 2.5

Generators = GraphGenerator(dataset, data_size=DATA_SIZE, batch_size=BATCH_SIZE, cutoff=CUTOFF)
train_data = Generators.train_generator
valid_data = Generators.valid_generator
test_data = Generators.test_generator


#parameters
atom_dim=16
bond_dim=64
num_atom=118
state_dim=16
sp_dim=230
units=32
edge_steps=1
message_steps=1
transform_steps=1
num_attention_heads=8
dense_units=64
output_dim=64
readout_units=64
dropout=0.0
reg0=0.00
reg1=0.00
reg2=0.00
reg3=0.00
reg_rec=0.00
batch_size=BATCH_SIZE
spherical_harmonics=True
regression=dataset.regression
optimizer = 'Adam'

print('\n----- parameters -----',
    '\ntask_type: ', dataset.task_type,
    '\nsample_size:', Generators.data_size,
    '\ncutoff: ', CUTOFF,
    '\natom_dim: ', atom_dim,
    '\nbond_dim: ', bond_dim,
    '\nnum_atom: ', num_atom,
    '\nstate_dim: ', state_dim,
    '\nsp_dim: ', sp_dim,
    '\nunits: ', units,
    '\nedge_steps: ', edge_steps,
    '\nmessage_steps: ', message_steps,
    '\ntransform_steps: ', transform_steps,
    '\nnum_attention_heads: ', num_attention_heads,
    '\ndense_units: ', dense_units,
    '\noutput_dim: ', output_dim,
    '\nreadout_units: ', readout_units,
    '\ndropout: ', dropout,
    '\nreg0: ', reg0,
    '\nreg1: ', reg1,
    '\nreg2: ', reg2,
    '\nreg3: ', reg3,
    '\nreg_rec: ', reg_rec,
    '\nbatch_size: ', batch_size,
    '\nspherical_harmonics: ', spherical_harmonics,
    '\noptimizer: ', optimizer,
    '\nregression: ', regression,)

del dataset

gnn = GNN(model=TransformerModel,
        atom_dim=atom_dim,
        bond_dim=bond_dim,
        num_atom=num_atom,
        state_dim=state_dim,
        sp_dim=sp_dim,
        units=units,
        edge_steps=edge_steps,
        message_steps=message_steps,
        transform_steps=transform_steps,
        num_attention_heads=num_attention_heads,
        dense_units=dense_units,
        output_dim=output_dim,
        readout_units=readout_units,
        dropout=dropout,
        reg0=reg0,
        reg1=reg1,
        reg2=reg2,
        reg3=reg3,
        reg_rec=reg_rec,
        batch_size=batch_size,
        spherical_harmonics=spherical_harmonics,
        optimizer = optimizer,
        regression=regression,
        )

gnn.train(train_data, valid_data, test_data, epochs=500, lr=1e-3, warm_up=True, load_weights=False,
            verbose=1, checkpoints=None, save_weights_only=True, workdir=ModulePath)
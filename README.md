![](https://img.shields.io/badge/license-MIT-red)
![](https://img.shields.io/badge/build-passing-brightgreen)
![](https://img.shields.io/pypi/v/matdgl)
![](https://img.shields.io/pypi/dm/matdgl)
![](https://img.shields.io/badge/python-3.8-blue)
![](https://img.shields.io/badge/tensorflow-2.10.0-red)
![](https://img.shields.io/github/stars/huzongxiang/MatDGL?style=social)

# MatDGL(Material Deep Graph Learning)
MatDGL is a neural network package that allows researchers to train custom models for material modeling tasks. It aims to accelerate the research and application of material science. It provides user a series of state-of-the-art models and supports user's innovative researches.

## Table of Contents

* [Hightlights](#hightlights)
* [Installation](#installation)
* [Usage](#usage)
* [Framework](#matdgl-framework)
* [Implemented-models](#implemented-models)
* [Contributors](#contributors)
* [References](#references)
* [Contact](#Contact)

<a name="Hightlights"></a>
## Hightlights
+ Easy to installation.
+ Three steps to fast testing.
+ Flexible and adaptive to user's trainning task.

<a name="Installation"></a>
## Installation

MatDGL can be installed easily through anaconda! As follows:

+ Create a new conda environment named "matdgl" by command, then activate environment "matdgl":    
    ```bash
    conda create -n matdgl python=3.8
    conda activate matdgl
    ```  
   It's necessary to create a new conda environment to aviod bugs causing by version conflict.   
 
+ Configure dependencies of matdgl:
    ```bash
    conda install -c conda-forge tensorflow-gpu
    ```

+ Install pymatgen:  
    ```bash
    conda install --channel conda-forge pymatgen  
    ```    

+ Install other dependencies:  
    ```bash
    conda install --channel conda-forge mendeleev  
    conda install --channel conda-forge graphviz  
    conda install --channel conda-forge pydot  
    conda install --channel conda-forge sklearn
    ```   

+ Install matdgl:  
    ```bash
    pip install matdgl
    ```  
  

<a name="Usage"></a>
## Usage
### Quick start
MatDGL is very easy to use!  
Just ***three steps*** can finish a fast test using matdgl:
+ **download test data**  
Get test datas from https://github.com/huzongxiang/MatDGL/tree/main/datas/    
There are four json files in datas: dataset_classification.json, dataset_multiclassification.json, dataset_regression.json  
and dataset_pretrain.json.    
+ **prepare workdir**  
Download datas and put it in your trainning work directory, test.py file should also be put in the directory  
	```
	workdir
	│   test.py
    |
	└───datas
		│   dataset_classification.json
		│   dataset_multiclassification.json
		│   dataset_regression.json
		│   dataset_pretrain.json
	``` 
+ **run command**  
run command:  
	```bash
	python test.py
	```  
You have finished your testing multi-classification trainning! The trainning results and model weight could be saved in /results and /models, respectively.  

### Understanding trainning script  
You can use matdgl by provided trainning scripts in user_easy_trainscript only, but understanding script will help you custom your trainning task!   
     
+ **get datas**  
Get current work directory of running trainning script, the script will read datas from 'workdir/datas/' , then saves results and models to 'workdir/results/' and 'workdir/models/'  
	```python
	from pathlib import Path
	ModulePath = Path(__file__).parent.absolute() # workdir
	```  

+ **fed trainning datas**   
Module Dataset will read data from 'ModulePath/datas/dataset.json', 'task_type' defines regression/classification/multi-classification, 'data_path' gets path of trainning datas.  
	```python
	from matdgl.data import Dataset
	dataset = Dataset(task_type='multiclassfication', data_path=ModulePath)
	```  

+ **generator**  
Module GraphGenerator feds datas into model during trainning. The Module splits datas into train, valid, test sets, and transform structures data into labelled graphs and gets three generators.
BATCH_SIZE is batch size during trainning, DATA_SIZE defines number of datas your used in entire datas, CUTOFF is cutoff of graph edges in crystal.   
	```python
	from matdgl.data.generator import GraphGenerator
	BATCH_SIZE = 128
	DATA_SIZE = None
	CUTOFF = 2.5
	Generators = GraphGenerator(dataset, data_size=DATA_SIZE, batch_size=BATCH_SIZE, cutoff=CUTOFF)
	train_data = Generators.train_generator
	valid_data = Generators.valid_generator
	test_data = Generators.test_generator

	#if task is multiclassfication, should define variable multiclassifiction
	multiclassification = Generators.multiclassification  
	```  

+ **building model**  
Module GNN defines a trainning framework that accepts a series of models. MatDGL provides a series of mainstream models as your need.  
	```python
	from matdgl.models import GNN
	from matdgl.models.gnnmodel import MpnnBaseModel, TransformerBaseModel, CgcnnModel, GraphAttentionModel

	gnn = GNN(model=MpnnBaseModel,
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
		)
	```

+ **trainning**  
Using trainning function of model to train. Common trainning parameters can be defined, workdir is current directory of trainning script, it saves results of model during trainning. If test_data exists, model will predict on test_data.  
	```python
	gnn.train(train_data, valid_data, test_data, epochs=700, lr=3e-3, warm_up=True, load_weights=False, verbose=1, checkpoints=None, save_weights_only=True, workdir=ModulePath)
	```

+ **prediction**  
The simplest method for predicting is using script predict.py in /user_easy_train_scripts.  
Using predict_data funciton to predict.  
	```python
	gnn.predict_datas(test_data, workdir=ModulePath)    # predict on test datas with labels
	y_pred_keras = gnn.predict(datas)                   # predict on new datas without labels
	```

+ **preparing your custom datas**  
If you have your structures (and labels), the Dataset receives pymatgen.core.Structure type. So you should transform your POSCAR or cif to pymatgen.core.Structure type.  
	```python
	import os
	from pymatgen.core.structure import Structure
	structures = []                                      # your structure list
	for cif in os.listdir(cif_path):
		structures.append(Structure.from_file(cif))    # for POSCAR too

	# construct your dataset
	from matdgl.data import Dataset
	dataset = Dataset(task_type='my_classification', data_path=ModulePath)  # task_type could be my_regression, my_classification, my_multiclassification
	dataset.prepare_x(structures)
	dataset.prepare_y(labels)   # if you have labels used to trainning model, labels could be None in prediction on new datas without labels

	# alternatively, you can construct dataset as follow
	dataset.structures = structures
	dataset.labels = labels

	# save your structures and labels to dataset in dataset_my*.json
	dataset.save_datasets(strurtures, labels)

	# for prediction on new datas without labels, Generators has not attribute multiclassification, should assign definite value
	Generators = GraphGenerator(dataset, data_size=DATA_SIZE, batch_size=BATCH_SIZE, cutoff=CUTOFF)     # dataset.labels is None
	Generators.multiclassification = 5
	multiclassification = Generators.multiclassification  # multiclassification = 5
	```

+ **models provided by matdgl**  
 We provide GraphModel, MpnnBaseModel, TransformerBaseModel, MpnnModel, TransformerModel, DirectionalMpnnModel, DirectionalTransformerModel and CGCNN model according to your demends. TransformerModel, GraphModel and MpnnModel are different models. TransformerModel is a graph transformer. MpnnModel is a massege passing neural network. GraphModel is a combination of TransformerModel and MpnnModel. MpnnBaseModel and TransformerBaseModel don't take directional informations of crystal into count so them run faster. MpnnBaseModel is the fastest model but accuracy is enough for most tasks. TransformerModel can achieve the hightest accuracy in most tasks. The CGCNN model is the crystal graph convolution neural network model. The GraphAttentionModel is the graph attention neural network.  
	```python
	from matdgl.models import GNN
	from matdgl.models.gnnmodel import MpnnBaseModel, TransformerBaseModel , DirectionalMpnnModel, DirectionalTransformerModel, MpnnModel, TransformerModel, GraphModel, CgcnnModel, GraphAttentionModel
	```

+ **custom your model and trainning**  
The Module GNN provides a flexible trainning framework to accept tensorflow.keras.models.Model type customized by user. Yon can custom your model and train the model according to the following example.  
	```python
	from tensorflow.keras.models import Model
	from tensorflow.keras import layers
	from matdgl.layers import MessagePassing
	from matdgl.layers import PartitionPadding

	def MyModel(
		bond_dim,
		atom_dim=16,
		num_atom=118,
		state_dim=16,
		sp_dim=230,
		units=32,
		message_steps=1,
		readout_units=64,
		batch_size=16,
		):
		atom_features = layers.Input((), dtype="int32", name="atom_features_input")
		atom_features_ = layers.Embedding(num_atom, atom_dim, dtype="float32", name="atom_features")(atom_features)
		bond_features = layers.Input((bond_dim), dtype="float32", name="bond_features")
		local_env = layers.Input((6), dtype="float32", name="local_env")
		state_attrs = layers.Input((), dtype="int32", name="state_attrs_input")   
		state_attrs_ = layers.Embedding(sp_dim, state_dim, dtype="float32", name="state_attrs")(state_attrs)

		pair_indices = layers.Input((2), dtype="int32", name="pair_indices")

		atom_graph_indices = layers.Input(
		(), dtype="int32", name="atom_graph_indices"
		)

		bond_graph_indices = layers.Input(
		(), dtype="int32", name="bond_graph_indices"
		)

		pair_indices_per_graph = layers.Input((2), dtype="int32", name="pair_indices_per_graph")

		x = MessagePassing(message_steps)(
		[atom_features_, edge_features, state_attrs_, pair_indices,
			atom_graph_indices, bond_graph_indices]
		)

		x = PartitionPadding(batch_size)([x[0], atom_graph_indices])
		x = layers.BatchNormalization()(x)
		x = layers.GlobalAveragePooling1D()(x)
		x = layers.Dense(readout_units, activation="relu", name='readout0')(x)
		x = layers.Dense(1, activation="sigmoid", name='final')(x)

		model = Model(
		inputs=[atom_features, bond_features, local_env, state_attrs, pair_indices, atom_graph_indices,
					bond_graph_indices, pair_indices_per_graph],
		outputs=[x],
		)
		return model

	from matdgl.models import GNN
	gnn = GNN(model=MyModel,     
		atom_dim=16,
		bond_dim=64,
		num_atom=118,
		state_dim=16,
		sp_dim=230,
		units=32,
		message_steps=1,
		readout_units=64,
		batch_size=16,
		optimizer='Adam',
		regression=False,
		multiclassification=None,)
	gnn.train(train_data, valid_data, test_data, epochs=700, lr=3e-3, warm_up=True, load_weights=False, verbose=1, checkpoints=None, save_weights_only=True, workdir=ModulePath)  
	```  
	You can set edge as your model output.   
	```python
	from matdgl.layers import EdgeMessagePassing
	def MyModel(
		bond_dim,
		atom_dim=16,
		num_atom=118,
		state_dim=16,
		sp_dim=230,
		units=32,
		message_steps=1,
		readout_units=64,
		batch_size=16,
		):
		atom_features = layers.Input((), dtype="int32", name="atom_features_input")
		atom_features_ = layers.Embedding(num_atom, atom_dim, dtype="float32", name="atom_features")(atom_features)
		bond_features = layers.Input((bond_dim), dtype="float32", name="bond_features")
		local_env = layers.Input((6), dtype="float32", name="local_env")
		state_attrs = layers.Input((), dtype="int32", name="state_attrs_input")   
		state_attrs_ = layers.Embedding(sp_dim, state_dim, dtype="float32", name="state_attrs")(state_attrs)

		pair_indices = layers.Input((2), dtype="int32", name="pair_indices")

		atom_graph_indices = layers.Input(
		(), dtype="int32", name="atom_graph_indices"
		)

		bond_graph_indices = layers.Input(
		(), dtype="int32", name="bond_graph_indices"
		)

		pair_indices_per_graph = layers.Input((2), dtype="int32", name="pair_indices_per_graph")

		x = EdgeMessagePassing(units,
					edge_steps,
					kernel_regularizer=l2(reg0),
					sph=spherical_harmonics
					)([bond_features, local_env, pair_indices])

		x = PartitionPadding(batch_size)([x[1], bond_graph_indices])
		x = layers.BatchNormalization()(x)
		x = layers.GlobalAveragePooling1D()(x)
		x = layers.Dense(readout_units, activation="relu", name='readout0')(x)
		x = layers.Dense(readout_units//2, activation="relu", name='readout1')(x)
		x = layers.Dense(1, name='final')(x)

		model = Model(
		inputs=[atom_features, bond_features, local_env, state_attrs, pair_indices, atom_graph_indices,
					bond_graph_indices, pair_indices_per_graph],
		outputs=[x],
		)
		return model
	```  

	The Module GNN has some basic parameter necessary to be defined but not necessary to be used:  
	```python
	class GNN:
	    def __init__(self,
		model: Model,
		atom_dim=16,
		bond_dim=32,
		num_atom=118,
		state_dim=16,
		sp_dim=230,
		batch_size=16,
		regression=True,
		optimizer = 'Adam',
		multiclassification=None,
		**kwargs,
		):
		"""
		pass
		"""  
	```  


<a name="MatDGL-framework"></a>
## Framework  
MatDGL 


<a name="Implemented-models"></a>
## Implemented-models  
We list currently supported GNN models:
* **GCN** from Kipf and Welling: [Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907) (ICLR 2017)  
* **GAT** from Veličković *et al.*: [Graph Attention Networks](https://arxiv.org/abs/1710.10903) (ICLR 2018)  
* **GN** from Battaglia *et al.*: [Relational inductive biases, deep learning, and graph networks](https://arxiv.org/pdf/1806.01261v1)   
* **Transformer** from Vaswani *et al.*: [Attention Is All You Need](https://arxiv.org/pdf/1706.03762) (NIPS 2017)  


<a name="Contributors"></a>
## Contributors
Zongxiang Hu


<a name="References"></a>
## References


<a name="Contact"></a>
## Contact
Please contact me if you have any questions.  
Mail: huzongxiang@yahoo.com  
Wechat: voodoozx2015

##  _Retinal vessel segmentation based on GT-UNet_
### Introduction
This project is a retinal blood vessel segmentation code based on UNet-like Group Transformer Network (GT-UNet), including data preprocessing, model training and testing, visualization, etc. 
 
### Requirements  
The main package and version of the python environment are as follows
```
# Name                    Version         
python                    3.7.9                    
pytorch                   1.7.0         
torchvision               0.8.0         
cudatoolkit               10.2.89       
cudnn                     7.6.5           
matplotlib                3.3.2              
numpy                     1.19.2        
opencv                    3.4.2         
pandas                    1.1.3        
pillow                    8.0.1         
scikit-learn              0.23.2          
scipy                     1.5.2           
tensorboardX              2.1        
tqdm                      4.54.1             
```  

---  
## Usage 



The project structure and intention are as follows : 
```
VesselSeg-Pytorch			# Source code		
    ├── config.py		 	# Configuration information
    ├── lib			            # Function library
    │   ├── common.py
    │   ├── dataset.py		        # Dataset class to load training data
    │   ├── datasetV2.py		        # Dataset class to load training data with lower memory
    │   ├── extract_patches.py		# Extract training and test samples
    │   ├── help_functions.py		# 
    │   ├── __init__.py
    │   ├── logger.py 		        # To create log
    │   ├── losses
    │   ├── metrics.py		        # Evaluation metrics
    │   └── pre_processing.py		# Data preprocessing
    ├── models		        # All models are created in this folder
    │   ├── __init__.py
    │   ├── nn
    │   └── GT-UNet.py
    ├── prepare_dataset	        # Prepare the dataset (organize the image path of the dataset)
    │   ├── chasedb1.py
    │   ├── data_path_list		  # image path of dataset
    │   ├── drive.py
    │   └── stare.py
    ├── tools			     # some tools
    │   ├── ablation_plot.py
    │   ├── ablation_plot_with_detail.py
    │   ├── merge_k-flod_plot.py
    │   └── visualization
    ├── function.py			        # Creating dataloader, training and validation functions 
    ├── test.py			            # Test file
    └── train.py			          # Train file
```
### Training model
Please confirm the configuration information in the `config.py`. Pay special attention to the `train_data_path_list` and `test_data_path_list`. Then, running:
```
python train.py
```
You can configure the training information in config, or modify the configuration parameters using the command line. The training results will be saved to the corresponding directory(save name) in the `experiments` folder.  
### 3) Testing model
The test process also needs to specify parameters in `config.py`. You can also modify the parameters through the command line, running:
```
python test.py  
```  
The above command loads the `best_model.pth` in `./experiments/GT-UNet_vessel_seg` and performs a performance test on the testset, and its test results are saved in the same folder.    
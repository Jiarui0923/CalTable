<img src="images/tulane_long.png" width="128px"><img src="images/icon_apl.png" width="256px"><img src="images/icon_long.png" width="128px"> 

# (CalTable) Calculate Table
`Update: 2025/03/11`

This is part of [Antigen Processing Likelihood (APL) Suite](https://github.com/Jiarui0923/APL) Project.


## Introduction
Calculate Table (`CalTable`) is a robust computational tool designed for interdisciplinary data processing, enabling users to perform calculations with the simplicity of a Pandas DataFrame interface. By connecting seamlessly with EasyAPI, CalTable allows users from various fields to easily manipulate and analyze their data, making complex computations accessible without requiring specialized programming knowledge.

If there is any issue, please put up with an issue or contact Jiarui Li (jli78@tulane.edu)

## Installation
The pip install command: 
```bash
pip install -U caltable @ https://github.com/Jiarui0923/CalTable@2.0.8
```  

## Requirements
All code was developed in Python 3.12.x.

|Package|Version|Usage|Website|Require|
|:------|:-----:|:----|:-----:|:-----:|
|pandas <img src="https://pandas.pydata.org/docs/_static/pandas.svg" width="52pt">|`2.2.2`|Data processing|[<img src="/images/icons/link.png" width="20pt">](https://pandas.pydata.org/)|`REQUIRED`|

The markdown documentation is generated by DocFlow, `1.0.0` version of which is embedded to this package.
The details about docflow could be found at: https://github.com/Jiarui0923/DocFlow

The base layer for EasyAPI access is supported by EasyAccess, `1.0.3` version of which is embedded to this package.
The details about docflow could be found at: https://github.com/Jiarui0923/EasyAccess

## Extensions
There are supported extensions for scientific calculation:
1. **CalTable-Bio**
   [https://git.tulane.edu/apl/caltable-bio ](https://github.com/Jiarui0923/caltable-bio)
   Biology related extentions

## Getting Start
This is the easiest way to start from a workbench configuration file.
The detail guide could be found at: [tutorial.md](/docs/tutorial.md) and [tutorial.ipynb](/docs/tutorial.ipynb) 
```python
workbench = ct.WorkBench.load('corex.workbench.json') # Load work desk
table = ct.DataTable([{'path':str(file)} for file in Path('./data').glob('*.pdb') ]) # Create path table with PDB files from `./data` folder
table[0, 'sconf_weight'] = 0.7 
table = workbench['read-corex'](table) # Read PDB, select chain A, and compute COREX.
table[0, 'corex'] # Visualize COREX result
```
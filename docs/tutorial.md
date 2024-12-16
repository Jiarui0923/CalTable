# CalTable Guideline
`Update: 2024-11-04`

Calculate Table (`CalTable`) is a robust computational tool designed for interdisciplinary data processing, enabling users to perform calculations with the simplicity of a Pandas DataFrame interface. By connecting seamlessly with EasyAPI, CalTable allows users from various fields to easily manipulate and analyze their data, making complex computations accessible without requiring specialized programming knowledge.

## Installation
There are two options:
1. If you are at Tulane Campus (uptown or downtown), you could install the package from our Jellyroll Python Pakcage Index (JPIP) follow command:
   `pip install -U caltable --index-url https://jellyroll.cs.tulane.edu/pypi/simple/`  
   (Just make sure you connected to WIFI `tulane` or `eduroam`)
2. For off-campus, please install using the attached file:
   `pip install caltable-1.0.1.zip`

## Basic Tutorial
**This section aims to let you learn how to use CalTable easily. For more customization function, please check the next section, advanced tutorial**

Now, let's try the simplest way to use CalTable to compute COREX. 


```python
# import caltable if you have successfully installed it.
import caltable as ct
from pathlib import Path
```

Before, we start the tutorial, I'd like to provide the shortest code to run code on a folder of PDB files and visualize the result.


```python
workbench = ct.WorkBench.load('corex.workbench.json') # Load work desk
table = ct.DataTable([{'path':str(file)} for file in Path('./data').glob('*.pdb') ]) # Create path table with PDB files from `./data` folder
table[0, 'sconf_weight'] = 0.7 
table = workbench['read-corex'](table) # Read PDB, select chain A, and compute COREX.
table[0, 'corex'] # Visualize COREX result
```

    [9.0s] ✓ Task (COREX) CORrelation with hydrogen EXchange protection factors Finished.






<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>...</th>
      <th>87</th>
      <th>88</th>
      <th>89</th>
      <th>90</th>
      <th>91</th>
      <th>92</th>
      <th>93</th>
      <th>94</th>
      <th>95</th>
      <th>96</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2.120279</td>
      <td>2.120279</td>
      <td>2.120279</td>
      <td>2.120279</td>
      <td>2.263343</td>
      <td>2.628881</td>
      <td>3.209727</td>
      <td>3.475768</td>
      <td>3.660153</td>
      <td>3.875141</td>
      <td>...</td>
      <td>4.232127</td>
      <td>3.504005</td>
      <td>2.833538</td>
      <td>2.276724</td>
      <td>1.987038</td>
      <td>1.826393</td>
      <td>1.592688</td>
      <td>1.592688</td>
      <td>1.592688</td>
      <td>1.592688</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 97 columns</p>
</div>




```python
table
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>path</th>
      <th>pdb_id</th>
      <th>pdb</th>
      <th>chain</th>
      <th>corex</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>data\6cdb.pdb</td>
      <td>6cdb</td>
      <td>PDB:821 lines</td>
      <td>A</td>
      <td>COREX (ln(kf)) Values:[-5.000873006361232, -5....</td>
    </tr>
  </tbody>
</table>
</div>



**REAL TUTORIAL Beginning**  
First step, please load the WorkBench, which is a `*.workbench.json` file.  
Work Bench is a top level object for caltable.  
It is like a desk with all tools placed on it.  
To save the time and simplify the configuration procedure, we have prepared some working desk with possible useful tools for you.  
These desks are stored in file such as `*.workbench.json`.  
So, please load them to use the prepared working desk.


```python
# Load the workbench
# You could replace the file path to other workbench file
workbench = ct.WorkBench.load('corex.workbench.json')
# Then, let's visualize the desk.  
# The `LibIndex` shows all `toolbox` on this desk.  
# There are typically two toolboxs including `local` and `Jellyroll Bioinformatics`. (Later `AWS` maybe here)
# Each toolbox listed all tools inside.
# For example, `local` toolbox has tools to enable you read PDB files (`read-file`) and sheet files (`read-sheet`)
# The COREX tool only provided by a remote server `Jellyroll` in our lab.
# The `workflows` shows some working procedure, protocal, or what you like call it.
# Each workflow is a sequential combination of a set of tools to appoach the calculation target.
workbench
```




# COREX WorkBench (1.0)  
Provide a set of tools and workflows for COREX computations  
## Workflows  
- **read-corex**: **COREX (Local Files)**: Run COREX for local PDB files.  
- **read-sasa**: **SASA (Local Files)**: Run SASA for local PDB files.  
- **read-bfactor**: **B-Factor (Local Files)**: Fetch residue level b-factor for local PDB files.  
- **read-all**: **Run all things (Local Files)**: Calculate COREX, SASA, and B-factor for local PDB files.  
- **read-pdbs**: **Run PDB files**: Read local PDB files and select chain.  
- **read-table**: **Fetch Local Sheet**: Fetch parameters from local sheet file.  
- **corex**: **COREX**: Run COREX for the pdb column.  
- **sasa**: **SASA**: Run SASA for pdb column.  
- **bfactor**: **B-Factor**: Fetch residue level b-factor for PDB column.  
- **all**: **Run all things**: Calculate COREX, SASA, and B-factor for PDB column.  
## LibIndex  
`2 libs` `8 Algorithms`

  
### local  
- **read-file**: Read local files from the given path.  
- **read-sheet**: Read local sheet file and attach to the table.  


  
### Jellyroll Bioinformatics  
- **select-chain**: Select destinated chains from the given PDB file.  
- **sasa**: Calculate the solvent accessible surface area for the given protein. The results will be an array concatenated by the order of sorted(chains)  
- **corex**: An algorithm designed to compute comformational stability of a protein. The results will be an array concatenated by the order of sorted(chains)  
- **list-chain**: List all chains from the given PDB file.  
- **bfactor**: Extract residue level B-Factor from the given PDB file (The B-Factor of CA atom).  
- **get-pdb**: Get PDB file by PDB ID.  


  
  





```python
# For example, `read-corex` enables you to compute COREX for local PDB files
# We could call it to read its documentation:
# It is combination of read-file, select-chain, list-chain, and corex.
# The `parameters` section shows the optional parameter and required parameters
# The parameter with `[OPTIONAL]` means you can ignore this parameter, caltable will fill it with the default value.
# The without parameter with `[OPTIONAL]` means you must provide it.
workbench['read-corex']
```




### COREX (Local Files)  

Run COREX for local PDB files.  
  
#### Parameters  
- **path**: (string:**string**)=`None`; The path to the target file; (`None`)   
- **chain**: (string:**PDB Chain IDs**)_[OPTIONAL]_=`A`; The selected protein chains ID.; (`[A-Za-z0-9]+(,[A-Za-z0-9]+)*`) The protein chain ids, seperate with `,`, no blank character.  
- **window_size**: (number:**float>1**)_[OPTIONAL]_=`10`; The protein folding unit size. Also, the number of partition schemes.; (`{'min': 1}`) The float number that is greater than 1.  
- **min_size**: (number:**float>1**)_[OPTIONAL]_=`4`; The minumum protein folding unit size.; (`{'min': 1}`) The float number that is greater than 1.  
- **samples**: (number:**float>1**)_[OPTIONAL]_=`10000`; (Ignore for exhaustive sampling) The sample number for each partition scheme. Total sample number=samples*window_size.; (`{'min': 1}`) The float number that is greater than 1.  
- **sampler**: (string:**COREX Sampler**)_[OPTIONAL]_=`exhaustive`; The COREX states sampler; (`(exhaustive|montecarlo|adaptive)`) (exhaustive|montecarlo|adaptive) The COREX micro-states sampler, which could be exhaustive enumerate, Monte Carlo, or Adaptibe Monte Carlo sampler.  
- **threshold**: (number:**float>0**)_[OPTIONAL]_=`0.75`; (Ignore for exhaustive sampling) The threshold for the sampler.; (`{'min': 0}`) The float number that is greater than 0.  
- **sconf_weight**: (number:**float>0**)_[OPTIONAL]_=`1.0`; Entropy factor.; (`{'min': 0}`) The float number that is greater than 0.  
- **base_fraction**: (number:**float>0**)_[OPTIONAL]_=`1.0`; The base fraction used to sum all COREX (ln_kf) values.; (`{'min': 0}`) The float number that is greater than 0.  
- **probe_radius**: (number:**float>1**)_[OPTIONAL]_=`1.4`; The probe radius for SASA in A.; (`{'min': 1}`) The float number that is greater than 1.  
- **n_points**: (number:**float>1**)_[OPTIONAL]_=`1000`; The number of test points in Shrake & Rupley algorithm for SASA.; (`{'min': 1}`) The float number that is greater than 1.  
#### Returns  
- **pdb**: (string:**PDB File**)=`None`; The output PDB file that only contains selected chains.; (`None`) The protein PDB file  
- **pdb_id**: (string:**string**)=`None`; The file name; (`None`)   
- **chain**: (string:**PDB Chain IDs**)=`None`; The chains contained in the PDB files.; (`[A-Za-z0-9]+(,[A-Za-z0-9]+)*`) The protein chain ids, seperate with `,`, no blank character.  
- **corex**: (numarray:**COREX (ln(kf)) Values**)=`None`; The COREX values. The order is the same order as the PDB.; (`None`) COREX Values in Sorted Chain ID Order  





```python
# Of course, you can read the documentation of each tool
# not only just documentation for workflow provided.
# The same tools may appear in different toolkits,
# CalTable will automatically choose the best one to run.
# For example,
workbench.toolkits['corex']()
# Also, you could build your own workflow by your self.
# We will discuss this later in advanced tutorial.
```




### (COREX) CORrelation with hydrogen EXchange protection factors  

An algorithm designed to compute comformational stability of a protein. The results will be an array concatenated by the order of sorted(chains)  
  
#### Parameters  
- **pdb**: (string:**PDB File**)=`None`; The input PDB file.; (`None`) The protein PDB file  
- **window_size**: (number:**float>1**)_[OPTIONAL]_=`10`; The protein folding unit size. Also, the number of partition schemes.; (`{'min': 1}`) The float number that is greater than 1.  
- **min_size**: (number:**float>1**)_[OPTIONAL]_=`4`; The minumum protein folding unit size.; (`{'min': 1}`) The float number that is greater than 1.  
- **samples**: (number:**float>1**)_[OPTIONAL]_=`10000`; (Ignore for exhaustive sampling) The sample number for each partition scheme. Total sample number=samples*window_size.; (`{'min': 1}`) The float number that is greater than 1.  
- **sampler**: (string:**COREX Sampler**)_[OPTIONAL]_=`exhaustive`; The COREX states sampler; (`(exhaustive|montecarlo|adaptive)`) (exhaustive|montecarlo|adaptive) The COREX micro-states sampler, which could be exhaustive enumerate, Monte Carlo, or Adaptibe Monte Carlo sampler.  
- **threshold**: (number:**float>0**)_[OPTIONAL]_=`0.75`; (Ignore for exhaustive sampling) The threshold for the sampler.; (`{'min': 0}`) The float number that is greater than 0.  
- **sconf_weight**: (number:**float>0**)_[OPTIONAL]_=`1.0`; Entropy factor.; (`{'min': 0}`) The float number that is greater than 0.  
- **base_fraction**: (number:**float>0**)_[OPTIONAL]_=`1.0`; The base fraction used to sum all COREX (ln_kf) values.; (`{'min': 0}`) The float number that is greater than 0.  
- **probe_radius**: (number:**float>1**)_[OPTIONAL]_=`1.4`; The probe radius for SASA in A.; (`{'min': 1}`) The float number that is greater than 1.  
- **n_points**: (number:**float>1**)_[OPTIONAL]_=`1000`; The number of test points in Shrake & Rupley algorithm for SASA.; (`{'min': 1}`) The float number that is greater than 1.  
#### Returns  
- **corex**: (numarray:**COREX (ln(kf)) Values**)=`None`; The COREX values. The order is the same order as the PDB.; (`None`) COREX Values in Sorted Chain ID Order  




Now, our working desk is ready. Let's prepare the material (the data)


```python
# This function allows to build a data table from a folder of PDB files
# You could use this function to load any folder of PDB files you want.
# Here, the example is folder `data`
def build_table_with_pdb(path):
    pdb_files = [{'path':str(file)}
                for file in Path(path).glob('*.pdb')
                if file.is_file()]
    return ct.DataTable(pdb_files)
table = build_table_with_pdb('data')
table
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>path</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>data\6cdb.pdb</td>
    </tr>
  </tbody>
</table>
</div>



DataTable is the DataFrame of CalTable.  
All inputs and outputs will be stored in a data table.  
What `build_table_with_pdb` do, is just create a list of dictionary with key to be `path` and value to be the path to the pdb file.  
The inputs of the workflow or tool mean CalTable will check whether there is a column named this in the Data Table.  
If there is match one, it will use this column as the input for this paramter.
The outputs of the workflow or tool mean CalTable will store back a data with the format defined to the column named as output name.  

Now, we could start to use the `read-corex` to compute COREX for the PDB file:


```python
# Directly call this workflow with the table
# The PDB read and chain selection will happen on your computer
# The COREX will happen on the remote server
table = workbench['read-corex'](table)
# The result now has been written to the table
table
```

    [8.9s] ✓ Task (COREX) CORrelation with hydrogen EXchange protection factors Finished.




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>path</th>
      <th>pdb_id</th>
      <th>pdb</th>
      <th>chain</th>
      <th>corex</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>data\6cdb.pdb</td>
      <td>6cdb</td>
      <td>PDB:821 lines</td>
      <td>A</td>
      <td>COREX (ln(kf)) Values:[-5.000873006361232, -5....</td>
    </tr>
  </tbody>
</table>
</div>



Now, let is visualize the results and fetch the values.


```python
# The CalTable will automatically infer the data type and find the best way to visualize it.
# For example:
table[0, 'pdb'] # Index row:0 and column:pdb
```


<div id="3dmolviewer_1730756471608242"  style="position: relative; width: 400px; height: 300px;">
        <p id="3dmolwarning_1730756471608242" style="background-color:#ffcccc;color:black">3Dmol.js failed to load for some reason.  Please check your browser console for error messages.<br></p>
        </div>
<script>

var loadScriptAsync = function(uri){
  return new Promise((resolve, reject) => {
    //this is to ignore the existence of requirejs amd
    var savedexports, savedmodule;
    if (typeof exports !== 'undefined') savedexports = exports;
    else exports = {}
    if (typeof module !== 'undefined') savedmodule = module;
    else module = {}

    var tag = document.createElement('script');
    tag.src = uri;
    tag.async = true;
    tag.onload = () => {
        exports = savedexports;
        module = savedmodule;
        resolve();
    };
  var firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
});
};

if(typeof $3Dmolpromise === 'undefined') {
$3Dmolpromise = null;
  $3Dmolpromise = loadScriptAsync('https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.4.0/3Dmol-min.js');
}

var viewer_1730756471608242 = null;
var warn = document.getElementById("3dmolwarning_1730756471608242");
if(warn) {
    warn.parentNode.removeChild(warn);
}
$3Dmolpromise.then(function() {
viewer_1730756471608242 = $3Dmol.createViewer(document.getElementById("3dmolviewer_1730756471608242"),{backgroundColor:"white"});
viewer_1730756471608242.zoomTo();
	viewer_1730756471608242.addModelsAsFrames("ATOM      1  N   SER A   6     -12.615  82.680 -12.301  1.00 77.47           N  \nATOM      2  CA  SER A   6     -13.722  82.765 -13.253  1.00 79.72           C  \nATOM      3  C   SER A   6     -13.286  83.466 -14.546  1.00 75.97           C  \nATOM      4  O   SER A   6     -12.140  83.325 -14.972  1.00 77.43           O  \nATOM      5  CB  SER A   6     -14.920  83.495 -12.624  1.00 82.09           C  \nATOM      6  OG  SER A   6     -15.483  82.752 -11.551  1.00 80.73           O  \nATOM      7  N   GLU A   7     -14.217  84.196 -15.173  1.00 76.61           N  \nATOM      8  CA  GLU A   7     -13.938  85.015 -16.360  1.00 72.64           C  \nATOM      9  C   GLU A   7     -13.498  84.163 -17.556  1.00 69.72           C  \nATOM     10  O   GLU A   7     -12.640  84.566 -18.347  1.00 67.45           O  \nATOM     11  CB  GLU A   7     -12.899  86.102 -16.043  1.00 73.92           C  \nATOM     12  CG  GLU A   7     -12.927  87.333 -16.961  1.00 73.67           C  \nATOM     13  CD  GLU A   7     -11.773  88.297 -16.685  1.00 76.60           C  \nATOM     14  OE1 GLU A   7     -11.033  88.644 -17.638  1.00 75.10           O  \nATOM     15  OE2 GLU A   7     -11.604  88.701 -15.510  1.00 77.99           O  \nATOM     16  N   ILE A   8     -14.099  82.982 -17.711  1.00 71.08           N  \nATOM     17  CA  ILE A   8     -13.846  82.133 -18.883  1.00 64.68           C  \nATOM     18  C   ILE A   8     -14.829  82.586 -19.963  1.00 62.85           C  \nATOM     19  O   ILE A   8     -15.996  82.186 -20.009  1.00 67.11           O  \nATOM     20  CB  ILE A   8     -13.950  80.639 -18.558  1.00 65.26           C  \nATOM     21  CG1 ILE A   8     -12.603  80.104 -18.036  1.00 60.40           C  \nATOM     22  CG2 ILE A   8     -14.369  79.811 -19.791  1.00 58.01           C  \nATOM     23  CD1 ILE A   8     -12.187  80.597 -16.653  1.00 59.18           C  \nATOM     24  N   ASN A   9     -14.358  83.473 -20.816  1.00 58.28           N  \nATOM     25  CA  ASN A   9     -15.092  83.880 -21.997  1.00 55.07           C  \nATOM     26  C   ASN A   9     -14.330  83.411 -23.233  1.00 52.44           C  \nATOM     27  O   ASN A   9     -13.231  82.847 -23.142  1.00 48.76           O  \nATOM     28  CB  ASN A   9     -15.309  85.395 -22.000  1.00 55.57           C  \nATOM     29  CG  ASN A   9     -14.005  86.165 -21.989  1.00 56.74           C  \nATOM     30  OD1 ASN A   9     -13.144  85.935 -21.138  1.00 59.41           O  \nATOM     31  ND2 ASN A   9     -13.844  87.073 -22.944  1.00 57.86           N  \nATOM     32  N   THR A  10     -14.936  83.652 -24.394  1.00 49.65           N  \nATOM     33  CA  THR A  10     -14.370  83.193 -25.657  1.00 52.38           C  \nATOM     34  C   THR A  10     -12.951  83.710 -25.860  1.00 46.65           C  \nATOM     35  O   THR A  10     -12.056  82.948 -26.251  1.00 43.12           O  \nATOM     36  CB  THR A  10     -15.280  83.632 -26.808  1.00 53.44           C  \nATOM     37  OG1 THR A  10     -16.519  82.918 -26.727  1.00 58.27           O  \nATOM     38  CG2 THR A  10     -14.622  83.376 -28.168  1.00 51.61           C  \nATOM     39  N   ASP A  11     -12.729  85.003 -25.598  1.00 48.82           N  \nATOM     40  CA  ASP A  11     -11.398  85.594 -25.749  1.00 50.20           C  \nATOM     41  C   ASP A  11     -10.354  84.837 -24.933  1.00 46.86           C  \nATOM     42  O   ASP A  11      -9.267  84.517 -25.436  1.00 45.74           O  \nATOM     43  CB  ASP A  11     -11.434  87.065 -25.327  1.00 54.09           C  \nATOM     44  CG  ASP A  11     -12.629  87.810 -25.907  1.00 60.37           C  \nATOM     45  OD1 ASP A  11     -13.301  88.552 -25.148  1.00 60.20           O  \nATOM     46  OD2 ASP A  11     -12.894  87.647 -27.122  1.00 60.90           O  \nATOM     47  N   THR A  12     -10.665  84.549 -23.665  1.00 43.39           N  \nATOM     48  CA  THR A  12      -9.731  83.808 -22.825  1.00 43.54           C  \nATOM     49  C   THR A  12      -9.325  82.496 -23.480  1.00 40.44           C  \nATOM     50  O   THR A  12      -8.134  82.178 -23.566  1.00 34.98           O  \nATOM     51  CB  THR A  12     -10.337  83.530 -21.447  1.00 47.22           C  \nATOM     52  OG1 THR A  12     -10.773  84.757 -20.850  1.00 49.81           O  \nATOM     53  CG2 THR A  12      -9.284  82.875 -20.548  1.00 40.45           C  \nATOM     54  N   LEU A  13     -10.307  81.712 -23.940  1.00 35.58           N  \nATOM     55  CA  LEU A  13      -9.982  80.406 -24.506  1.00 36.16           C  \nATOM     56  C   LEU A  13      -9.246  80.541 -25.832  1.00 36.38           C  \nATOM     57  O   LEU A  13      -8.444  79.673 -26.183  1.00 34.79           O  \nATOM     58  CB  LEU A  13     -11.250  79.560 -24.665  1.00 39.33           C  \nATOM     59  CG  LEU A  13     -11.980  79.186 -23.358  1.00 38.67           C  \nATOM     60  CD1 LEU A  13     -13.003  78.075 -23.591  1.00 33.75           C  \nATOM     61  CD2 LEU A  13     -10.985  78.794 -22.250  1.00 34.97           C  \nATOM     62  N   GLU A  14      -9.487  81.618 -26.575  1.00 35.93           N  \nATOM     63  CA  GLU A  14      -8.681  81.850 -27.764  1.00 37.74           C  \nATOM     64  C   GLU A  14      -7.221  82.108 -27.401  1.00 36.71           C  \nATOM     65  O   GLU A  14      -6.316  81.528 -28.017  1.00 35.17           O  \nATOM     66  CB  GLU A  14      -9.261  83.008 -28.568  1.00 40.66           C  \nATOM     67  CG  GLU A  14     -10.634  82.695 -29.162  1.00 47.24           C  \nATOM     68  CD  GLU A  14     -10.560  82.476 -30.657  1.00 55.54           C  \nATOM     69  OE1 GLU A  14     -10.467  83.486 -31.393  1.00 61.46           O  \nATOM     70  OE2 GLU A  14     -10.571  81.299 -31.090  1.00 57.40           O  \nATOM     71  N   ARG A  15      -6.967  82.965 -26.402  1.00 35.95           N  \nATOM     72  CA  ARG A  15      -5.585  83.201 -25.982  1.00 39.04           C  \nATOM     73  C   ARG A  15      -4.943  81.921 -25.459  1.00 34.72           C  \nATOM     74  O   ARG A  15      -3.784  81.634 -25.772  1.00 32.37           O  \nATOM     75  CB  ARG A  15      -5.524  84.316 -24.935  1.00 39.76           C  \nATOM     76  CG  ARG A  15      -6.162  85.615 -25.417  1.00 47.84           C  \nATOM     77  CD  ARG A  15      -5.691  86.834 -24.638  1.00 51.55           C  \nATOM     78  NE  ARG A  15      -6.129  86.800 -23.245  1.00 56.01           N  \nATOM     79  CZ  ARG A  15      -7.336  87.175 -22.821  1.00 55.78           C  \nATOM     80  NH1 ARG A  15      -8.247  87.620 -23.684  1.00 54.83           N  \nATOM     81  NH2 ARG A  15      -7.636  87.100 -21.530  1.00 50.93           N  \nATOM     82  N   VAL A  16      -5.696  81.126 -24.688  1.00 33.67           N  \nATOM     83  CA  VAL A  16      -5.219  79.813 -24.244  1.00 35.16           C  \nATOM     84  C   VAL A  16      -4.827  78.954 -25.445  1.00 33.15           C  \nATOM     85  O   VAL A  16      -3.767  78.302 -25.465  1.00 30.28           O  \nATOM     86  CB  VAL A  16      -6.299  79.126 -23.387  1.00 35.55           C  \nATOM     87  CG1 VAL A  16      -6.005  77.645 -23.254  1.00 34.04           C  \nATOM     88  CG2 VAL A  16      -6.385  79.778 -22.014  1.00 32.29           C  \nATOM     89  N   THR A  17      -5.686  78.942 -26.464  1.00 33.07           N  \nATOM     90  CA  THR A  17      -5.378  78.244 -27.705  1.00 32.22           C  \nATOM     91  C   THR A  17      -4.066  78.732 -28.312  1.00 33.64           C  \nATOM     92  O   THR A  17      -3.256  77.923 -28.777  1.00 34.41           O  \nATOM     93  CB  THR A  17      -6.534  78.415 -28.696  1.00 33.88           C  \nATOM     94  OG1 THR A  17      -7.737  77.905 -28.114  1.00 30.95           O  \nATOM     95  CG2 THR A  17      -6.256  77.666 -29.996  1.00 34.16           C  \nATOM     96  N   GLU A  18      -3.826  80.047 -28.313  1.00 33.39           N  \nATOM     97  CA  GLU A  18      -2.577  80.539 -28.892  1.00 34.25           C  \nATOM     98  C   GLU A  18      -1.368  80.104 -28.079  1.00 38.17           C  \nATOM     99  O   GLU A  18      -0.300  79.823 -28.652  1.00 34.07           O  \nATOM    100  CB  GLU A  18      -2.596  82.064 -29.015  1.00 39.37           C  \nATOM    101  CG  GLU A  18      -3.784  82.610 -29.786  1.00 40.86           C  \nATOM    102  CD  GLU A  18      -3.828  82.052 -31.202  1.00 50.38           C  \nATOM    103  OE1 GLU A  18      -2.776  82.078 -31.886  1.00 59.63           O  \nATOM    104  OE2 GLU A  18      -4.917  81.589 -31.612  1.00 56.38           O  \nATOM    105  N   ILE A  19      -1.519  80.047 -26.749  1.00 31.90           N  \nATOM    106  CA  ILE A  19      -0.436  79.577 -25.897  1.00 30.68           C  \nATOM    107  C   ILE A  19      -0.070  78.146 -26.249  1.00 30.40           C  \nATOM    108  O   ILE A  19       1.110  77.824 -26.451  1.00 32.34           O  \nATOM    109  CB  ILE A  19      -0.814  79.712 -24.412  1.00 30.20           C  \nATOM    110  CG1 ILE A  19      -0.780  81.186 -23.996  1.00 30.42           C  \nATOM    111  CG2 ILE A  19       0.132  78.865 -23.542  1.00 32.29           C  \nATOM    112  CD1 ILE A  19      -1.439  81.456 -22.671  1.00 31.62           C  \nATOM    113  N   PHE A  20      -1.066  77.260 -26.309  1.00 28.26           N  \nATOM    114  CA  PHE A  20      -0.761  75.863 -26.611  1.00 28.73           C  \nATOM    115  C   PHE A  20      -0.265  75.690 -28.044  1.00 33.30           C  \nATOM    116  O   PHE A  20       0.556  74.805 -28.317  1.00 31.33           O  \nATOM    117  CB  PHE A  20      -1.992  74.991 -26.367  1.00 28.67           C  \nATOM    118  CG  PHE A  20      -2.326  74.811 -24.908  1.00 31.55           C  \nATOM    119  CD1 PHE A  20      -1.381  74.328 -24.025  1.00 32.00           C  \nATOM    120  CD2 PHE A  20      -3.576  75.152 -24.422  1.00 34.75           C  \nATOM    121  CE1 PHE A  20      -1.683  74.165 -22.664  1.00 35.77           C  \nATOM    122  CE2 PHE A  20      -3.891  74.995 -23.066  1.00 33.78           C  \nATOM    123  CZ  PHE A  20      -2.928  74.506 -22.186  1.00 32.45           C  \nATOM    124  N   LYS A  21      -0.763  76.504 -28.971  1.00 29.61           N  \nATOM    125  CA  LYS A  21      -0.270  76.438 -30.342  1.00 35.04           C  \nATOM    126  C   LYS A  21       1.207  76.794 -30.401  1.00 33.66           C  \nATOM    127  O   LYS A  21       2.002  76.089 -31.030  1.00 35.19           O  \nATOM    128  CB  LYS A  21      -1.085  77.366 -31.246  1.00 34.70           C  \nATOM    129  CG  LYS A  21      -2.252  76.689 -31.899  1.00 38.04           C  \nATOM    130  CD  LYS A  21      -3.037  77.664 -32.764  1.00 41.48           C  \nATOM    131  CE  LYS A  21      -4.209  76.965 -33.428  1.00 42.03           C  \nATOM    132  NZ  LYS A  21      -5.102  77.944 -34.089  1.00 45.17           N  \nATOM    133  N   ALA A  22       1.599  77.876 -29.723  1.00 36.64           N  \nATOM    134  CA  ALA A  22       3.007  78.259 -29.710  1.00 34.65           C  \nATOM    135  C   ALA A  22       3.864  77.214 -29.011  1.00 36.72           C  \nATOM    136  O   ALA A  22       5.008  76.972 -29.413  1.00 35.62           O  \nATOM    137  CB  ALA A  22       3.176  79.614 -29.035  1.00 34.42           C  \nATOM    138  N   LEU A  23       3.345  76.588 -27.956  1.00 32.96           N  \nATOM    139  CA  LEU A  23       4.146  75.569 -27.294  1.00 32.07           C  \nATOM    140  C   LEU A  23       4.153  74.245 -28.041  1.00 30.56           C  \nATOM    141  O   LEU A  23       4.866  73.330 -27.624  1.00 31.03           O  \nATOM    142  CB  LEU A  23       3.648  75.345 -25.859  1.00 31.66           C  \nATOM    143  CG  LEU A  23       3.833  76.482 -24.858  1.00 33.45           C  \nATOM    144  CD1 LEU A  23       3.034  76.187 -23.608  1.00 33.98           C  \nATOM    145  CD2 LEU A  23       5.323  76.653 -24.518  1.00 32.07           C  \nATOM    146  N   GLY A  24       3.356  74.093 -29.100  1.00 32.47           N  \nATOM    147  CA  GLY A  24       3.381  72.857 -29.858  1.00 29.67           C  \nATOM    148  C   GLY A  24       4.566  72.823 -30.816  1.00 34.58           C  \nATOM    149  O   GLY A  24       4.392  72.695 -32.026  1.00 33.14           O  \nATOM    150  N   ASP A  25       5.776  72.937 -30.283  1.00 32.08           N  \nATOM    151  CA  ASP A  25       6.987  73.064 -31.095  1.00 33.61           C  \nATOM    152  C   ASP A  25       8.137  72.473 -30.295  1.00 35.00           C  \nATOM    153  O   ASP A  25       8.407  72.942 -29.186  1.00 31.73           O  \nATOM    154  CB  ASP A  25       7.248  74.536 -31.443  1.00 33.31           C  \nATOM    155  CG  ASP A  25       8.507  74.740 -32.286  1.00 37.65           C  \nATOM    156  OD1 ASP A  25       8.389  75.185 -33.443  1.00 41.93           O  \nATOM    157  OD2 ASP A  25       9.615  74.482 -31.792  1.00 33.61           O  \nATOM    158  N   TYR A  26       8.809  71.458 -30.854  1.00 34.52           N  \nATOM    159  CA  TYR A  26       9.806  70.698 -30.093  1.00 34.87           C  \nATOM    160  C   TYR A  26      10.912  71.593 -29.549  1.00 33.11           C  \nATOM    161  O   TYR A  26      11.300  71.484 -28.378  1.00 31.05           O  \nATOM    162  CB  TYR A  26      10.403  69.602 -30.972  1.00 36.72           C  \nATOM    163  CG  TYR A  26      11.504  68.795 -30.316  1.00 38.05           C  \nATOM    164  CD1 TYR A  26      11.225  67.945 -29.254  1.00 38.24           C  \nATOM    165  CD2 TYR A  26      12.809  68.857 -30.785  1.00 40.10           C  \nATOM    166  CE1 TYR A  26      12.206  67.196 -28.657  1.00 40.15           C  \nATOM    167  CE2 TYR A  26      13.817  68.105 -30.190  1.00 42.21           C  \nATOM    168  CZ  TYR A  26      13.504  67.277 -29.125  1.00 41.32           C  \nATOM    169  OH  TYR A  26      14.476  66.526 -28.523  1.00 44.79           O  \nATOM    170  N   ASN A  27      11.454  72.465 -30.398  1.00 33.26           N  \nATOM    171  CA  ASN A  27      12.547  73.331 -29.975  1.00 32.61           C  \nATOM    172  C   ASN A  27      12.082  74.367 -28.964  1.00 29.26           C  \nATOM    173  O   ASN A  27      12.827  74.711 -28.039  1.00 27.57           O  \nATOM    174  CB  ASN A  27      13.186  74.005 -31.195  1.00 34.00           C  \nATOM    175  CG  ASN A  27      14.156  73.091 -31.912  1.00 35.18           C  \nATOM    176  OD1 ASN A  27      14.766  72.217 -31.291  1.00 32.19           O  \nATOM    177  ND2 ASN A  27      14.299  73.277 -33.228  1.00 38.27           N  \nATOM    178  N   ARG A  28      10.864  74.887 -29.129  1.00 28.90           N  \nATOM    179  CA  ARG A  28      10.321  75.804 -28.130  1.00 29.61           C  \nATOM    180  C   ARG A  28      10.120  75.105 -26.793  1.00 27.43           C  \nATOM    181  O   ARG A  28      10.352  75.700 -25.741  1.00 26.89           O  \nATOM    182  CB  ARG A  28       9.003  76.413 -28.607  1.00 28.44           C  \nATOM    183  CG  ARG A  28       9.177  77.457 -29.687  1.00 32.37           C  \nATOM    184  CD  ARG A  28       7.900  78.256 -29.905  1.00 33.95           C  \nATOM    185  NE  ARG A  28       7.967  78.876 -31.218  1.00 40.16           N  \nATOM    186  CZ  ARG A  28       7.167  78.574 -32.227  1.00 44.62           C  \nATOM    187  NH1 ARG A  28       6.175  77.701 -32.059  1.00 42.97           N  \nATOM    188  NH2 ARG A  28       7.344  79.180 -33.397  1.00 44.34           N  \nATOM    189  N   ILE A  29       9.689  73.843 -26.813  1.00 28.15           N  \nATOM    190  CA  ILE A  29       9.604  73.080 -25.572  1.00 28.63           C  \nATOM    191  C   ILE A  29      10.992  72.896 -24.957  1.00 28.13           C  \nATOM    192  O   ILE A  29      11.155  72.950 -23.732  1.00 25.16           O  \nATOM    193  CB  ILE A  29       8.901  71.736 -25.829  1.00 29.38           C  \nATOM    194  CG1 ILE A  29       7.399  71.969 -26.071  1.00 29.64           C  \nATOM    195  CG2 ILE A  29       9.121  70.768 -24.667  1.00 27.42           C  \nATOM    196  CD1 ILE A  29       6.722  72.785 -24.950  1.00 32.39           C  \nATOM    197  N   ARG A  30      12.016  72.690 -25.791  1.00 26.87           N  \nATOM    198  CA  ARG A  30      13.363  72.526 -25.244  1.00 29.16           C  \nATOM    199  C   ARG A  30      13.857  73.817 -24.605  1.00 27.38           C  \nATOM    200  O   ARG A  30      14.477  73.802 -23.524  1.00 28.12           O  \nATOM    201  CB  ARG A  30      14.328  72.061 -26.340  1.00 28.91           C  \nATOM    202  CG  ARG A  30      14.166  70.599 -26.731  1.00 30.89           C  \nATOM    203  CD  ARG A  30      15.513  70.037 -27.162  1.00 39.48           C  \nATOM    204  NE  ARG A  30      15.960  70.650 -28.402  1.00 39.00           N  \nATOM    205  CZ  ARG A  30      17.232  70.855 -28.746  1.00 35.15           C  \nATOM    206  NH1 ARG A  30      18.238  70.509 -27.936  1.00 37.45           N  \nATOM    207  NH2 ARG A  30      17.491  71.421 -29.911  1.00 35.06           N  \nATOM    208  N   ILE A  31      13.596  74.945 -25.259  1.00 26.43           N  \nATOM    209  CA  ILE A  31      13.938  76.238 -24.674  1.00 26.28           C  \nATOM    210  C   ILE A  31      13.202  76.429 -23.349  1.00 27.44           C  \nATOM    211  O   ILE A  31      13.795  76.838 -22.340  1.00 27.34           O  \nATOM    212  CB  ILE A  31      13.612  77.368 -25.666  1.00 27.93           C  \nATOM    213  CG1 ILE A  31      14.490  77.253 -26.924  1.00 29.71           C  \nATOM    214  CG2 ILE A  31      13.740  78.736 -24.988  1.00 27.08           C  \nATOM    215  CD1 ILE A  31      14.104  78.225 -28.021  1.00 26.44           C  \nATOM    216  N   MET A  32      11.893  76.138 -23.335  1.00 28.17           N  \nATOM    217  CA  MET A  32      11.102  76.365 -22.127  1.00 28.01           C  \nATOM    218  C   MET A  32      11.555  75.465 -20.989  1.00 25.95           C  \nATOM    219  O   MET A  32      11.574  75.888 -19.831  1.00 27.15           O  \nATOM    220  CB  MET A  32       9.619  76.133 -22.402  1.00 25.47           C  \nATOM    221  CG  MET A  32       8.977  77.104 -23.385  1.00 29.33           C  \nATOM    222  SD  MET A  32       8.684  78.740 -22.718  1.00 33.67           S  \nATOM    223  CE  MET A  32       7.196  78.394 -21.765  1.00 31.21           C  \nATOM    224  N   GLU A  33      11.886  74.209 -21.286  1.00 25.79           N  \nATOM    225  CA  GLU A  33      12.360  73.323 -20.231  1.00 31.21           C  \nATOM    226  C   GLU A  33      13.699  73.812 -19.674  1.00 31.92           C  \nATOM    227  O   GLU A  33      13.903  73.828 -18.448  1.00 31.61           O  \nATOM    228  CB  GLU A  33      12.448  71.894 -20.768  1.00 29.70           C  \nATOM    229  CG  GLU A  33      12.606  70.813 -19.705  1.00 30.57           C  \nATOM    230  CD  GLU A  33      14.054  70.560 -19.339  1.00 39.43           C  \nATOM    231  OE1 GLU A  33      14.927  70.827 -20.190  1.00 36.92           O  \nATOM    232  OE2 GLU A  33      14.314  70.110 -18.205  1.00 41.59           O  \nATOM    233  N   LEU A  34      14.606  74.261 -20.555  1.00 27.83           N  \nATOM    234  CA  LEU A  34      15.865  74.841 -20.081  1.00 31.02           C  \nATOM    235  C   LEU A  34      15.605  75.999 -19.119  1.00 31.19           C  \nATOM    236  O   LEU A  34      16.209  76.084 -18.038  1.00 28.51           O  \nATOM    237  CB  LEU A  34      16.710  75.301 -21.281  1.00 29.80           C  \nATOM    238  CG  LEU A  34      18.166  75.749 -21.097  1.00 36.29           C  \nATOM    239  CD1 LEU A  34      18.938  75.608 -22.413  1.00 32.15           C  \nATOM    240  CD2 LEU A  34      18.259  77.186 -20.588  1.00 35.99           C  \nATOM    241  N   LEU A  35      14.712  76.913 -19.507  1.00 31.10           N  \nATOM    242  CA  LEU A  35      14.392  78.054 -18.652  1.00 30.23           C  \nATOM    243  C   LEU A  35      13.697  77.621 -17.371  1.00 32.24           C  \nATOM    244  O   LEU A  35      13.811  78.308 -16.345  1.00 31.82           O  \nATOM    245  CB  LEU A  35      13.518  79.050 -19.419  1.00 25.72           C  \nATOM    246  CG  LEU A  35      14.237  79.697 -20.607  1.00 28.30           C  \nATOM    247  CD1 LEU A  35      13.293  80.553 -21.426  1.00 28.45           C  \nATOM    248  CD2 LEU A  35      15.400  80.526 -20.089  1.00 29.33           C  \nATOM    249  N   SER A  36      12.978  76.495 -17.413  1.00 30.52           N  \nATOM    250  CA  SER A  36      12.329  75.960 -16.222  1.00 31.09           C  \nATOM    251  C   SER A  36      13.352  75.471 -15.212  1.00 37.15           C  \nATOM    252  O   SER A  36      13.101  75.528 -14.002  1.00 37.83           O  \nATOM    253  CB  SER A  36      11.375  74.827 -16.601  1.00 32.85           C  \nATOM    254  OG  SER A  36      12.019  73.572 -16.571  1.00 32.40           O  \nATOM    255  N   VAL A  37      14.496  74.979 -15.684  1.00 34.01           N  \nATOM    256  CA  VAL A  37      15.588  74.645 -14.770  1.00 36.60           C  \nATOM    257  C   VAL A  37      16.316  75.904 -14.307  1.00 37.34           C  \nATOM    258  O   VAL A  37      16.547  76.094 -13.109  1.00 41.43           O  \nATOM    259  CB  VAL A  37      16.554  73.649 -15.434  1.00 36.62           C  \nATOM    260  CG1 VAL A  37      17.783  73.402 -14.536  1.00 40.08           C  \nATOM    261  CG2 VAL A  37      15.831  72.342 -15.752  1.00 35.31           C  \nATOM    262  N   SER A  38      16.692  76.784 -15.235  1.00 35.97           N  \nATOM    263  CA  SER A  38      17.427  77.977 -14.844  1.00 38.51           C  \nATOM    264  C   SER A  38      17.288  79.074 -15.893  1.00 38.60           C  \nATOM    265  O   SER A  38      17.308  78.798 -17.097  1.00 36.91           O  \nATOM    266  CB  SER A  38      18.909  77.664 -14.636  1.00 42.28           C  \nATOM    267  OG  SER A  38      19.653  78.858 -14.720  1.00 44.76           O  \nATOM    268  N   GLU A  39      17.181  80.319 -15.425  1.00 37.55           N  \nATOM    269  CA  GLU A  39      17.174  81.455 -16.337  1.00 38.98           C  \nATOM    270  C   GLU A  39      18.496  81.519 -17.095  1.00 36.30           C  \nATOM    271  O   GLU A  39      19.531  81.048 -16.621  1.00 38.21           O  \nATOM    272  CB  GLU A  39      16.948  82.755 -15.572  1.00 40.56           C  \nATOM    273  CG  GLU A  39      18.137  83.140 -14.703  1.00 43.56           C  \nATOM    274  CD  GLU A  39      17.917  84.432 -13.942  1.00 49.83           C  \nATOM    275  OE1 GLU A  39      16.774  84.939 -13.924  1.00 52.49           O  \nATOM    276  OE2 GLU A  39      18.896  84.941 -13.362  1.00 57.03           O  \nATOM    277  N   ALA A  40      18.462  82.099 -18.292  1.00 36.54           N  \nATOM    278  CA  ALA A  40      19.638  82.043 -19.153  1.00 34.91           C  \nATOM    279  C   ALA A  40      19.558  83.121 -20.223  1.00 36.45           C  \nATOM    280  O   ALA A  40      18.487  83.671 -20.508  1.00 32.95           O  \nATOM    281  CB  ALA A  40      19.785  80.662 -19.805  1.00 36.07           C  \nATOM    282  N   SER A  41      20.715  83.404 -20.816  1.00 36.12           N  \nATOM    283  CA  SER A  41      20.853  84.323 -21.931  1.00 33.51           C  \nATOM    284  C   SER A  41      20.621  83.583 -23.238  1.00 32.47           C  \nATOM    285  O   SER A  41      20.613  82.355 -23.287  1.00 31.50           O  \nATOM    286  CB  SER A  41      22.247  84.947 -21.937  1.00 39.63           C  \nATOM    287  OG  SER A  41      23.224  83.946 -22.182  1.00 36.05           O  \nATOM    288  N   VAL A  42      20.461  84.352 -24.318  1.00 32.62           N  \nATOM    289  CA  VAL A  42      20.321  83.748 -25.644  1.00 35.56           C  \nATOM    290  C   VAL A  42      21.560  82.938 -26.007  1.00 36.50           C  \nATOM    291  O   VAL A  42      21.455  81.828 -26.542  1.00 35.04           O  \nATOM    292  CB  VAL A  42      20.028  84.824 -26.707  1.00 34.95           C  \nATOM    293  CG1 VAL A  42      20.151  84.224 -28.122  1.00 36.36           C  \nATOM    294  CG2 VAL A  42      18.629  85.412 -26.489  1.00 36.41           C  \nATOM    295  N   GLY A  43      22.750  83.481 -25.741  1.00 37.89           N  \nATOM    296  CA  GLY A  43      23.969  82.746 -26.049  1.00 37.06           C  \nATOM    297  C   GLY A  43      24.051  81.419 -25.319  1.00 33.19           C  \nATOM    298  O   GLY A  43      24.437  80.399 -25.898  1.00 32.61           O  \nATOM    299  N   HIS A  44      23.652  81.403 -24.050  1.00 33.26           N  \nATOM    300  CA  HIS A  44      23.698  80.159 -23.292  1.00 35.31           C  \nATOM    301  C   HIS A  44      22.652  79.162 -23.777  1.00 36.10           C  \nATOM    302  O   HIS A  44      22.940  77.963 -23.891  1.00 32.82           O  \nATOM    303  CB  HIS A  44      23.509  80.441 -21.805  1.00 37.08           C  \nATOM    304  CG  HIS A  44      23.513  79.205 -20.964  1.00 43.24           C  \nATOM    305  ND1 HIS A  44      22.356  78.606 -20.514  1.00 41.25           N  \nATOM    306  CD2 HIS A  44      24.535  78.434 -20.516  1.00 44.50           C  \nATOM    307  CE1 HIS A  44      22.663  77.529 -19.813  1.00 43.28           C  \nATOM    308  NE2 HIS A  44      23.978  77.404 -19.796  1.00 48.03           N  \nATOM    309  N   ILE A  45      21.429  79.628 -24.051  1.00 33.45           N  \nATOM    310  CA  ILE A  45      20.394  78.740 -24.580  1.00 31.91           C  \nATOM    311  C   ILE A  45      20.857  78.129 -25.891  1.00 32.00           C  \nATOM    312  O   ILE A  45      20.797  76.909 -26.095  1.00 31.72           O  \nATOM    313  CB  ILE A  45      19.073  79.508 -24.769  1.00 34.87           C  \nATOM    314  CG1 ILE A  45      18.548  80.043 -23.428  1.00 31.82           C  \nATOM    315  CG2 ILE A  45      18.030  78.617 -25.474  1.00 29.26           C  \nATOM    316  CD1 ILE A  45      17.464  81.106 -23.573  1.00 30.73           C  \nATOM    317  N   SER A  46      21.336  78.985 -26.796  1.00 33.56           N  \nATOM    318  CA  SER A  46      21.820  78.551 -28.098  1.00 31.13           C  \nATOM    319  C   SER A  46      22.913  77.498 -27.953  1.00 33.59           C  \nATOM    320  O   SER A  46      22.843  76.425 -28.567  1.00 32.56           O  \nATOM    321  CB  SER A  46      22.321  79.770 -28.863  1.00 29.85           C  \nATOM    322  OG  SER A  46      23.384  79.409 -29.718  1.00 37.25           O  \nATOM    323  N   HIS A  47      23.917  77.778 -27.113  1.00 33.44           N  \nATOM    324  CA  HIS A  47      25.016  76.832 -26.930  1.00 35.31           C  \nATOM    325  C   HIS A  47      24.526  75.515 -26.337  1.00 33.91           C  \nATOM    326  O   HIS A  47      24.865  74.433 -26.830  1.00 32.95           O  \nATOM    327  CB  HIS A  47      26.082  77.448 -26.034  1.00 36.49           C  \nATOM    328  CG  HIS A  47      27.210  76.519 -25.727  1.00 39.39           C  \nATOM    329  ND1 HIS A  47      27.369  75.924 -24.495  1.00 42.62           N  \nATOM    330  CD2 HIS A  47      28.223  76.065 -26.501  1.00 37.64           C  \nATOM    331  CE1 HIS A  47      28.448  75.162 -24.514  1.00 43.04           C  \nATOM    332  NE2 HIS A  47      28.984  75.228 -25.720  1.00 42.34           N  \nATOM    333  N   GLN A  48      23.707  75.589 -25.286  1.00 33.29           N  \nATOM    334  CA  GLN A  48      23.268  74.383 -24.592  1.00 33.93           C  \nATOM    335  C   GLN A  48      22.410  73.494 -25.487  1.00 34.22           C  \nATOM    336  O   GLN A  48      22.559  72.266 -25.466  1.00 31.65           O  \nATOM    337  CB  GLN A  48      22.505  74.763 -23.318  1.00 38.15           C  \nATOM    338  CG  GLN A  48      22.293  73.605 -22.348  1.00 42.88           C  \nATOM    339  CD  GLN A  48      23.506  72.670 -22.273  1.00 50.69           C  \nATOM    340  OE1 GLN A  48      24.540  73.010 -21.682  1.00 49.76           O  \nATOM    341  NE2 GLN A  48      23.381  71.484 -22.884  1.00 52.28           N  \nATOM    342  N   LEU A  49      21.502  74.085 -26.272  1.00 31.13           N  \nATOM    343  CA  LEU A  49      20.585  73.292 -27.093  1.00 31.64           C  \nATOM    344  C   LEU A  49      21.111  73.021 -28.501  1.00 29.25           C  \nATOM    345  O   LEU A  49      20.485  72.262 -29.241  1.00 32.94           O  \nATOM    346  CB  LEU A  49      19.210  73.985 -27.183  1.00 29.31           C  \nATOM    347  CG  LEU A  49      18.542  74.247 -25.831  1.00 30.47           C  \nATOM    348  CD1 LEU A  49      17.221  74.995 -25.996  1.00 30.01           C  \nATOM    349  CD2 LEU A  49      18.326  72.935 -25.079  1.00 31.19           C  \nATOM    350  N   ASN A  50      22.247  73.600 -28.875  1.00 33.86           N  \nATOM    351  CA  ASN A  50      22.779  73.496 -30.234  1.00 34.39           C  \nATOM    352  C   ASN A  50      21.768  74.030 -31.249  1.00 34.07           C  \nATOM    353  O   ASN A  50      21.384  73.359 -32.215  1.00 32.03           O  \nATOM    354  CB  ASN A  50      23.214  72.068 -30.571  1.00 36.36           C  \nATOM    355  CG  ASN A  50      24.157  72.024 -31.761  1.00 36.94           C  \nATOM    356  OD1 ASN A  50      23.927  71.311 -32.738  1.00 40.45           O  \nATOM    357  ND2 ASN A  50      25.211  72.820 -31.693  1.00 38.55           N  \nATOM    358  N   LEU A  51      21.336  75.263 -31.005  1.00 32.83           N  \nATOM    359  CA  LEU A  51      20.467  76.028 -31.881  1.00 30.88           C  \nATOM    360  C   LEU A  51      21.146  77.362 -32.149  1.00 30.53           C  \nATOM    361  O   LEU A  51      21.867  77.880 -31.293  1.00 34.39           O  \nATOM    362  CB  LEU A  51      19.079  76.242 -31.238  1.00 29.46           C  \nATOM    363  CG  LEU A  51      18.335  74.951 -30.884  1.00 31.08           C  \nATOM    364  CD1 LEU A  51      17.095  75.215 -30.016  1.00 28.93           C  \nATOM    365  CD2 LEU A  51      17.965  74.204 -32.188  1.00 28.64           C  \nATOM    366  N   SER A  52      20.951  77.908 -33.340  1.00 30.99           N  \nATOM    367  CA  SER A  52      21.599  79.174 -33.643  1.00 32.71           C  \nATOM    368  C   SER A  52      21.018  80.290 -32.779  1.00 35.56           C  \nATOM    369  O   SER A  52      19.888  80.211 -32.293  1.00 33.99           O  \nATOM    370  CB  SER A  52      21.444  79.518 -35.124  1.00 33.69           C  \nATOM    371  OG  SER A  52      20.143  79.987 -35.400  1.00 32.61           O  \nATOM    372  N   GLN A  53      21.816  81.340 -32.568  1.00 35.45           N  \nATOM    373  CA  GLN A  53      21.319  82.473 -31.793  1.00 35.92           C  \nATOM    374  C   GLN A  53      20.154  83.158 -32.499  1.00 36.99           C  \nATOM    375  O   GLN A  53      19.202  83.594 -31.845  1.00 34.29           O  \nATOM    376  CB  GLN A  53      22.448  83.468 -31.509  1.00 34.36           C  \nATOM    377  CG  GLN A  53      23.541  82.903 -30.604  1.00 41.03           C  \nATOM    378  CD  GLN A  53      24.262  83.971 -29.789  1.00 45.29           C  \nATOM    379  OE1 GLN A  53      23.719  85.048 -29.521  1.00 50.35           O  \nATOM    380  NE2 GLN A  53      25.490  83.668 -29.381  1.00 44.94           N  \nATOM    381  N   SER A  54      20.219  83.271 -33.833  1.00 37.57           N  \nATOM    382  CA  SER A  54      19.103  83.803 -34.615  1.00 38.85           C  \nATOM    383  C   SER A  54      17.800  83.087 -34.289  1.00 34.08           C  \nATOM    384  O   SER A  54      16.775  83.716 -34.000  1.00 36.04           O  \nATOM    385  CB  SER A  54      19.400  83.664 -36.112  1.00 37.04           C  \nATOM    386  OG  SER A  54      20.327  84.633 -36.536  1.00 42.79           O  \nATOM    387  N   ASN A  55      17.830  81.758 -34.373  1.00 34.02           N  \nATOM    388  CA  ASN A  55      16.643  80.946 -34.163  1.00 34.87           C  \nATOM    389  C   ASN A  55      16.126  81.091 -32.731  1.00 35.79           C  \nATOM    390  O   ASN A  55      14.939  81.343 -32.512  1.00 31.73           O  \nATOM    391  CB  ASN A  55      16.982  79.489 -34.493  1.00 32.70           C  \nATOM    392  CG  ASN A  55      15.770  78.595 -34.482  1.00 31.70           C  \nATOM    393  OD1 ASN A  55      14.641  79.077 -34.561  1.00 36.71           O  \nATOM    394  ND2 ASN A  55      15.991  77.283 -34.377  1.00 26.61           N  \nATOM    395  N   VAL A  56      17.015  80.945 -31.742  1.00 34.68           N  \nATOM    396  CA  VAL A  56      16.612  81.106 -30.343  1.00 33.92           C  \nATOM    397  C   VAL A  56      15.941  82.458 -30.141  1.00 35.42           C  \nATOM    398  O   VAL A  56      14.866  82.558 -29.532  1.00 36.16           O  \nATOM    399  CB  VAL A  56      17.827  80.942 -29.408  1.00 32.94           C  \nATOM    400  CG1 VAL A  56      17.437  81.291 -27.980  1.00 32.64           C  \nATOM    401  CG2 VAL A  56      18.397  79.523 -29.488  1.00 30.05           C  \nATOM    402  N   SER A  57      16.561  83.519 -30.667  1.00 35.62           N  \nATOM    403  CA  SER A  57      16.002  84.859 -30.525  1.00 36.63           C  \nATOM    404  C   SER A  57      14.620  84.958 -31.154  1.00 37.44           C  \nATOM    405  O   SER A  57      13.714  85.559 -30.572  1.00 35.71           O  \nATOM    406  CB  SER A  57      16.942  85.892 -31.146  1.00 38.81           C  \nATOM    407  OG  SER A  57      17.971  86.238 -30.235  1.00 42.89           O  \nATOM    408  N   HIS A  58      14.441  84.388 -32.345  1.00 37.24           N  \nATOM    409  CA  HIS A  58      13.122  84.400 -32.977  1.00 38.29           C  \nATOM    410  C   HIS A  58      12.078  83.724 -32.081  1.00 37.33           C  \nATOM    411  O   HIS A  58      11.012  84.299 -31.785  1.00 38.01           O  \nATOM    412  CB  HIS A  58      13.227  83.716 -34.345  1.00 35.70           C  \nATOM    413  CG  HIS A  58      11.997  83.824 -35.195  1.00 43.99           C  \nATOM    414  ND1 HIS A  58      11.673  84.964 -35.901  1.00 44.64           N  \nATOM    415  CD2 HIS A  58      11.032  82.918 -35.484  1.00 41.73           C  \nATOM    416  CE1 HIS A  58      10.549  84.764 -36.566  1.00 45.46           C  \nATOM    417  NE2 HIS A  58      10.141  83.530 -36.331  1.00 47.29           N  \nATOM    418  N   GLN A  59      12.384  82.507 -31.615  1.00 34.20           N  \nATOM    419  CA  GLN A  59      11.422  81.768 -30.801  1.00 36.66           C  \nATOM    420  C   GLN A  59      11.112  82.502 -29.503  1.00 35.52           C  \nATOM    421  O   GLN A  59       9.970  82.489 -29.038  1.00 34.70           O  \nATOM    422  CB  GLN A  59      11.939  80.361 -30.503  1.00 34.62           C  \nATOM    423  CG  GLN A  59      12.397  79.591 -31.724  1.00 34.66           C  \nATOM    424  CD  GLN A  59      11.384  79.609 -32.859  1.00 36.99           C  \nATOM    425  OE1 GLN A  59      10.178  79.500 -32.639  1.00 36.91           O  \nATOM    426  NE2 GLN A  59      11.879  79.758 -34.083  1.00 34.96           N  \nATOM    427  N   LEU A  60      12.110  83.167 -28.917  1.00 34.02           N  \nATOM    428  CA  LEU A  60      11.890  83.897 -27.671  1.00 34.46           C  \nATOM    429  C   LEU A  60      11.091  85.175 -27.891  1.00 37.35           C  \nATOM    430  O   LEU A  60      10.349  85.592 -26.992  1.00 35.32           O  \nATOM    431  CB  LEU A  60      13.224  84.236 -27.001  1.00 35.03           C  \nATOM    432  CG  LEU A  60      14.094  83.100 -26.492  1.00 32.27           C  \nATOM    433  CD1 LEU A  60      15.481  83.648 -26.072  1.00 37.05           C  \nATOM    434  CD2 LEU A  60      13.451  82.407 -25.323  1.00 31.90           C  \nATOM    435  N   LYS A  61      11.236  85.830 -29.052  1.00 38.36           N  \nATOM    436  CA  LYS A  61      10.327  86.933 -29.356  1.00 38.27           C  \nATOM    437  C   LYS A  61       8.898  86.433 -29.386  1.00 34.82           C  \nATOM    438  O   LYS A  61       7.998  87.064 -28.815  1.00 39.13           O  \nATOM    439  CB  LYS A  61      10.660  87.602 -30.686  1.00 42.24           C  \nATOM    440  CG  LYS A  61      12.104  87.987 -30.866  1.00 47.37           C  \nATOM    441  CD  LYS A  61      12.477  89.215 -30.066  1.00 51.75           C  \nATOM    442  CE  LYS A  61      13.996  89.367 -30.039  1.00 48.15           C  \nATOM    443  NZ  LYS A  61      14.537  89.486 -31.444  1.00 50.78           N  \nATOM    444  N   LEU A  62       8.670  85.281 -30.028  1.00 32.93           N  \nATOM    445  CA  LEU A  62       7.305  84.756 -30.063  1.00 36.78           C  \nATOM    446  C   LEU A  62       6.810  84.408 -28.659  1.00 37.21           C  \nATOM    447  O   LEU A  62       5.703  84.793 -28.271  1.00 35.22           O  \nATOM    448  CB  LEU A  62       7.213  83.539 -30.981  1.00 36.46           C  \nATOM    449  CG  LEU A  62       5.883  82.778 -30.860  1.00 40.64           C  \nATOM    450  CD1 LEU A  62       4.640  83.682 -31.074  1.00 45.24           C  \nATOM    451  CD2 LEU A  62       5.851  81.614 -31.827  1.00 44.91           C  \nATOM    452  N   LEU A  63       7.624  83.686 -27.882  1.00 31.76           N  \nATOM    453  CA  LEU A  63       7.209  83.283 -26.540  1.00 31.40           C  \nATOM    454  C   LEU A  63       6.973  84.492 -25.644  1.00 32.74           C  \nATOM    455  O   LEU A  63       6.070  84.479 -24.793  1.00 34.27           O  \nATOM    456  CB  LEU A  63       8.257  82.347 -25.923  1.00 30.93           C  \nATOM    457  CG  LEU A  63       8.440  80.999 -26.629  1.00 29.54           C  \nATOM    458  CD1 LEU A  63       9.652  80.240 -26.083  1.00 26.31           C  \nATOM    459  CD2 LEU A  63       7.161  80.146 -26.523  1.00 27.94           C  \nATOM    460  N   LYS A  64       7.757  85.555 -25.831  1.00 31.18           N  \nATOM    461  CA  LYS A  64       7.572  86.758 -25.024  1.00 34.12           C  \nATOM    462  C   LYS A  64       6.268  87.468 -25.388  1.00 36.25           C  \nATOM    463  O   LYS A  64       5.538  87.930 -24.499  1.00 33.49           O  \nATOM    464  CB  LYS A  64       8.766  87.702 -25.188  1.00 34.29           C  \nATOM    465  CG  LYS A  64       8.748  88.879 -24.214  1.00 39.83           C  \nATOM    466  CD  LYS A  64       9.656  90.025 -24.659  1.00 44.41           C  \nATOM    467  CE  LYS A  64      11.113  89.707 -24.429  1.00 47.89           C  \nATOM    468  NZ  LYS A  64      12.020  90.822 -24.852  1.00 54.24           N  \nATOM    469  N   SER A  65       5.948  87.548 -26.685  1.00 35.08           N  \nATOM    470  CA  SER A  65       4.710  88.215 -27.080  1.00 39.75           C  \nATOM    471  C   SER A  65       3.483  87.552 -26.462  1.00 38.41           C  \nATOM    472  O   SER A  65       2.450  88.206 -26.284  1.00 39.82           O  \nATOM    473  CB  SER A  65       4.578  88.231 -28.600  1.00 36.08           C  \nATOM    474  OG  SER A  65       4.192  86.955 -29.070  1.00 40.54           O  \nATOM    475  N   LEU A  66       3.571  86.262 -26.137  1.00 35.65           N  \nATOM    476  CA  LEU A  66       2.482  85.537 -25.504  1.00 36.02           C  \nATOM    477  C   LEU A  66       2.635  85.461 -23.993  1.00 35.68           C  \nATOM    478  O   LEU A  66       1.906  84.703 -23.347  1.00 30.63           O  \nATOM    479  CB  LEU A  66       2.371  84.129 -26.089  1.00 35.22           C  \nATOM    480  CG  LEU A  66       1.979  84.093 -27.565  1.00 39.21           C  \nATOM    481  CD1 LEU A  66       2.032  82.675 -28.062  1.00 41.20           C  \nATOM    482  CD2 LEU A  66       0.598  84.672 -27.767  1.00 38.46           C  \nATOM    483  N   HIS A  67       3.564  86.228 -23.422  1.00 34.29           N  \nATOM    484  CA  HIS A  67       3.769  86.287 -21.975  1.00 33.95           C  \nATOM    485  C   HIS A  67       4.128  84.927 -21.405  1.00 33.62           C  \nATOM    486  O   HIS A  67       3.747  84.593 -20.284  1.00 32.72           O  \nATOM    487  CB  HIS A  67       2.549  86.864 -21.251  1.00 38.80           C  \nATOM    488  CG  HIS A  67       2.180  88.234 -21.719  1.00 42.46           C  \nATOM    489  ND1 HIS A  67       2.933  89.349 -21.415  1.00 47.23           N  \nATOM    490  CD2 HIS A  67       1.160  88.666 -22.494  1.00 44.14           C  \nATOM    491  CE1 HIS A  67       2.387  90.411 -21.979  1.00 45.64           C  \nATOM    492  NE2 HIS A  67       1.310  90.024 -22.639  1.00 48.22           N  \nATOM    493  N   LEU A  68       4.878  84.140 -22.170  1.00 31.84           N  \nATOM    494  CA  LEU A  68       5.374  82.856 -21.693  1.00 31.53           C  \nATOM    495  C   LEU A  68       6.803  82.926 -21.165  1.00 33.07           C  \nATOM    496  O   LEU A  68       7.178  82.109 -20.317  1.00 27.19           O  \nATOM    497  CB  LEU A  68       5.272  81.810 -22.813  1.00 29.07           C  \nATOM    498  CG  LEU A  68       3.810  81.567 -23.242  1.00 31.61           C  \nATOM    499  CD1 LEU A  68       3.750  80.593 -24.396  1.00 27.19           C  \nATOM    500  CD2 LEU A  68       2.978  81.075 -22.062  1.00 27.62           C  \nATOM    501  N   VAL A  69       7.612  83.871 -21.653  1.00 32.23           N  \nATOM    502  CA  VAL A  69       8.912  84.178 -21.072  1.00 30.88           C  \nATOM    503  C   VAL A  69       8.983  85.683 -20.876  1.00 32.72           C  \nATOM    504  O   VAL A  69       8.230  86.445 -21.479  1.00 32.79           O  \nATOM    505  CB  VAL A  69      10.095  83.707 -21.949  1.00 29.43           C  \nATOM    506  CG1 VAL A  69      10.050  82.198 -22.140  1.00 27.83           C  \nATOM    507  CG2 VAL A  69      10.080  84.435 -23.302  1.00 29.23           C  \nATOM    508  N   LYS A  70       9.890  86.105 -20.005  1.00 32.93           N  \nATOM    509  CA  LYS A  70      10.213  87.513 -19.846  1.00 34.28           C  \nATOM    510  C   LYS A  70      11.728  87.643 -19.851  1.00 36.24           C  \nATOM    511  O   LYS A  70      12.457  86.644 -19.752  1.00 35.48           O  \nATOM    512  CB  LYS A  70       9.621  88.085 -18.556  1.00 33.19           C  \nATOM    513  CG  LYS A  70      10.205  87.444 -17.302  1.00 35.45           C  \nATOM    514  CD  LYS A  70       9.572  88.009 -16.040  1.00 36.68           C  \nATOM    515  CE  LYS A  70      10.209  87.401 -14.800  1.00 36.64           C  \nATOM    516  NZ  LYS A  70      10.220  85.915 -14.895  1.00 38.00           N  \nATOM    517  N   ALA A  71      12.211  88.885 -19.959  1.00 38.62           N  \nATOM    518  CA  ALA A  71      13.647  89.122 -20.037  1.00 41.88           C  \nATOM    519  C   ALA A  71      14.042  90.343 -19.217  1.00 44.66           C  \nATOM    520  O   ALA A  71      13.291  91.317 -19.129  1.00 42.36           O  \nATOM    521  CB  ALA A  71      14.103  89.297 -21.492  1.00 43.32           C  \nATOM    522  N   LYS A  72      15.231  90.277 -18.619  1.00 45.90           N  \nATOM    523  CA  LYS A  72      15.826  91.386 -17.887  1.00 50.83           C  \nATOM    524  C   LYS A  72      17.251  91.583 -18.383  1.00 51.65           C  \nATOM    525  O   LYS A  72      17.896  90.640 -18.836  1.00 49.48           O  \nATOM    526  CB  LYS A  72      15.832  91.132 -16.366  1.00 49.75           C  \nATOM    527  CG  LYS A  72      16.275  92.332 -15.541  1.00 54.78           C  \nATOM    528  CD  LYS A  72      15.250  93.468 -15.588  1.00 59.02           C  \nATOM    529  CE  LYS A  72      15.890  94.803 -15.974  1.00 57.13           C  \nATOM    530  NZ  LYS A  72      15.920  94.997 -17.459  1.00 53.72           N  \nATOM    531  N   ARG A  73      17.743  92.813 -18.309  1.00 55.23           N  \nATOM    532  CA  ARG A  73      19.115  93.090 -18.711  1.00 59.02           C  \nATOM    533  C   ARG A  73      20.022  92.975 -17.490  1.00 59.90           C  \nATOM    534  O   ARG A  73      19.806  93.654 -16.482  1.00 61.78           O  \nATOM    535  CB  ARG A  73      19.237  94.467 -19.358  1.00 58.26           C  \nATOM    536  CG  ARG A  73      20.677  94.896 -19.564  1.00 63.98           C  \nATOM    537  CD  ARG A  73      20.802  95.928 -20.665  1.00 65.92           C  \nATOM    538  NE  ARG A  73      22.104  95.849 -21.314  1.00 65.78           N  \nATOM    539  CZ  ARG A  73      22.363  95.110 -22.391  1.00 66.12           C  \nATOM    540  NH1 ARG A  73      21.401  94.380 -22.946  1.00 65.88           N  \nATOM    541  NH2 ARG A  73      23.584  95.102 -22.915  1.00 63.99           N  \nATOM    542  N   GLN A  74      21.019  92.098 -17.573  1.00 61.44           N  \nATOM    543  CA  GLN A  74      21.997  91.916 -16.509  1.00 63.66           C  \nATOM    544  C   GLN A  74      23.392  92.040 -17.104  1.00 63.72           C  \nATOM    545  O   GLN A  74      23.718  91.360 -18.086  1.00 63.96           O  \nATOM    546  CB  GLN A  74      21.824  90.563 -15.811  1.00 64.42           C  \nATOM    547  CG  GLN A  74      23.143  89.925 -15.371  1.00 68.73           C  \nATOM    548  CD  GLN A  74      22.936  88.728 -14.452  1.00 71.01           C  \nATOM    549  OE1 GLN A  74      22.715  88.890 -13.254  1.00 75.73           O  \nATOM    550  NE2 GLN A  74      23.017  87.522 -15.007  1.00 66.71           N  \nATOM    551  N   GLY A  75      24.207  92.911 -16.511  1.00 66.39           N  \nATOM    552  CA  GLY A  75      25.512  93.224 -17.060  1.00 63.56           C  \nATOM    553  C   GLY A  75      25.410  93.642 -18.512  1.00 65.72           C  \nATOM    554  O   GLY A  75      24.925  94.735 -18.824  1.00 65.12           O  \nATOM    555  N   GLN A  76      25.827  92.754 -19.414  1.00 64.45           N  \nATOM    556  CA  GLN A  76      25.808  93.030 -20.841  1.00 64.10           C  \nATOM    557  C   GLN A  76      24.673  92.338 -21.591  1.00 62.72           C  \nATOM    558  O   GLN A  76      24.406  92.708 -22.740  1.00 67.31           O  \nATOM    559  CB  GLN A  76      27.155  92.619 -21.468  1.00 62.00           C  \nATOM    560  CG  GLN A  76      27.395  93.144 -22.881  1.00 62.19           C  \nATOM    561  CD  GLN A  76      28.191  92.173 -23.758  1.00 61.84           C  \nATOM    562  OE1 GLN A  76      29.427  92.157 -23.732  1.00 58.28           O  \nATOM    563  NE2 GLN A  76      27.479  91.367 -24.546  1.00 60.46           N  \nATOM    564  N   SER A  77      23.987  91.366 -20.989  1.00 60.64           N  \nATOM    565  CA  SER A  77      23.154  90.450 -21.758  1.00 60.50           C  \nATOM    566  C   SER A  77      21.698  90.438 -21.293  1.00 58.62           C  \nATOM    567  O   SER A  77      21.358  90.890 -20.192  1.00 55.97           O  \nATOM    568  CB  SER A  77      23.728  89.026 -21.700  1.00 59.95           C  \nATOM    569  OG  SER A  77      24.284  88.755 -20.424  1.00 62.21           O  \nATOM    570  N   MET A  78      20.840  89.909 -22.171  1.00 53.17           N  \nATOM    571  CA  MET A  78      19.432  89.676 -21.874  1.00 50.20           C  \nATOM    572  C   MET A  78      19.266  88.284 -21.272  1.00 44.49           C  \nATOM    573  O   MET A  78      19.578  87.276 -21.915  1.00 44.31           O  \nATOM    574  CB  MET A  78      18.573  89.811 -23.135  1.00 50.40           C  \nATOM    575  CG  MET A  78      18.241  91.241 -23.540  1.00 53.87           C  \nATOM    576  SD  MET A  78      17.595  92.219 -22.164  1.00 66.98           S  \nATOM    577  CE  MET A  78      17.859  93.878 -22.800  1.00 65.15           C  \nATOM    578  N   ILE A  79      18.769  88.231 -20.045  1.00 43.18           N  \nATOM    579  CA  ILE A  79      18.507  86.985 -19.340  1.00 37.15           C  \nATOM    580  C   ILE A  79      17.015  86.699 -19.435  1.00 39.78           C  \nATOM    581  O   ILE A  79      16.187  87.538 -19.052  1.00 40.13           O  \nATOM    582  CB  ILE A  79      18.969  87.072 -17.879  1.00 40.44           C  \nATOM    583  CG1 ILE A  79      20.453  87.434 -17.824  1.00 46.47           C  \nATOM    584  CG2 ILE A  79      18.685  85.781 -17.135  1.00 37.77           C  \nATOM    585  CD1 ILE A  79      21.314  86.611 -18.748  1.00 44.83           C  \nATOM    586  N   TYR A  80      16.671  85.521 -19.947  1.00 35.20           N  \nATOM    587  CA  TYR A  80      15.287  85.108 -20.088  1.00 35.79           C  \nATOM    588  C   TYR A  80      14.883  84.166 -18.967  1.00 33.88           C  \nATOM    589  O   TYR A  80      15.716  83.490 -18.364  1.00 32.00           O  \nATOM    590  CB  TYR A  80      15.048  84.441 -21.443  1.00 33.48           C  \nATOM    591  CG  TYR A  80      15.005  85.454 -22.560  1.00 38.56           C  \nATOM    592  CD1 TYR A  80      16.179  86.013 -23.047  1.00 38.73           C  \nATOM    593  CD2 TYR A  80      13.795  85.865 -23.120  1.00 36.36           C  \nATOM    594  CE1 TYR A  80      16.159  86.951 -24.055  1.00 40.79           C  \nATOM    595  CE2 TYR A  80      13.766  86.811 -24.140  1.00 38.46           C  \nATOM    596  CZ  TYR A  80      14.960  87.346 -24.598  1.00 41.87           C  \nATOM    597  OH  TYR A  80      14.983  88.282 -25.602  1.00 47.64           O  \nATOM    598  N   SER A  81      13.579  84.132 -18.695  1.00 33.22           N  \nATOM    599  CA  SER A  81      13.037  83.224 -17.701  1.00 32.58           C  \nATOM    600  C   SER A  81      11.594  82.927 -18.068  1.00 28.69           C  \nATOM    601  O   SER A  81      10.974  83.656 -18.846  1.00 28.43           O  \nATOM    602  CB  SER A  81      13.130  83.830 -16.298  1.00 34.14           C  \nATOM    603  OG  SER A  81      12.502  85.106 -16.278  1.00 32.90           O  \nATOM    604  N   LEU A  82      11.064  81.838 -17.519  1.00 29.70           N  \nATOM    605  CA  LEU A  82       9.624  81.631 -17.610  1.00 30.07           C  \nATOM    606  C   LEU A  82       8.917  82.818 -16.969  1.00 31.16           C  \nATOM    607  O   LEU A  82       9.382  83.368 -15.964  1.00 31.78           O  \nATOM    608  CB  LEU A  82       9.219  80.322 -16.933  1.00 29.09           C  \nATOM    609  CG  LEU A  82       9.807  79.038 -17.530  1.00 31.24           C  \nATOM    610  CD1 LEU A  82       9.102  77.798 -16.986  1.00 28.58           C  \nATOM    611  CD2 LEU A  82       9.776  79.060 -19.061  1.00 27.46           C  \nATOM    612  N   ASP A  83       7.790  83.220 -17.561  1.00 30.91           N  \nATOM    613  CA  ASP A  83       7.195  84.507 -17.214  1.00 31.74           C  \nATOM    614  C   ASP A  83       6.793  84.569 -15.742  1.00 30.47           C  \nATOM    615  O   ASP A  83       7.169  85.507 -15.034  1.00 29.82           O  \nATOM    616  CB  ASP A  83       5.996  84.800 -18.113  1.00 30.04           C  \nATOM    617  CG  ASP A  83       5.253  86.069 -17.696  1.00 35.28           C  \nATOM    618  OD1 ASP A  83       5.634  87.158 -18.178  1.00 36.90           O  \nATOM    619  OD2 ASP A  83       4.305  85.978 -16.871  1.00 35.86           O  \nATOM    620  N   ASP A  84       6.028  83.588 -15.263  1.00 31.67           N  \nATOM    621  CA  ASP A  84       5.649  83.553 -13.848  1.00 29.58           C  \nATOM    622  C   ASP A  84       5.382  82.105 -13.447  1.00 30.29           C  \nATOM    623  O   ASP A  84       5.620  81.170 -14.217  1.00 26.88           O  \nATOM    624  CB  ASP A  84       4.455  84.487 -13.571  1.00 30.15           C  \nATOM    625  CG  ASP A  84       3.142  84.020 -14.219  1.00 30.34           C  \nATOM    626  OD1 ASP A  84       2.195  84.841 -14.309  1.00 29.53           O  \nATOM    627  OD2 ASP A  84       3.026  82.846 -14.641  1.00 29.06           O  \nATOM    628  N   ILE A  85       4.853  81.926 -12.237  1.00 31.51           N  \nATOM    629  CA  ILE A  85       4.689  80.588 -11.682  1.00 29.34           C  \nATOM    630  C   ILE A  85       3.626  79.772 -12.429  1.00 29.26           C  \nATOM    631  O   ILE A  85       3.663  78.535 -12.408  1.00 28.38           O  \nATOM    632  CB  ILE A  85       4.358  80.688 -10.185  1.00 30.43           C  \nATOM    633  CG1 ILE A  85       4.514  79.313  -9.550  1.00 30.69           C  \nATOM    634  CG2 ILE A  85       2.932  81.222  -9.990  1.00 29.18           C  \nATOM    635  CD1 ILE A  85       3.646  79.114  -8.337  1.00 32.55           C  \nATOM    636  N   HIS A  86       2.637  80.420 -13.053  1.00 25.25           N  \nATOM    637  CA  HIS A  86       1.648  79.651 -13.803  1.00 29.10           C  \nATOM    638  C   HIS A  86       2.286  78.963 -15.001  1.00 27.28           C  \nATOM    639  O   HIS A  86       1.951  77.815 -15.319  1.00 23.78           O  \nATOM    640  CB  HIS A  86       0.499  80.556 -14.255  1.00 27.16           C  \nATOM    641  CG  HIS A  86      -0.015  81.443 -13.164  1.00 30.61           C  \nATOM    642  ND1 HIS A  86       0.021  82.818 -13.241  1.00 30.63           N  \nATOM    643  CD2 HIS A  86      -0.528  81.147 -11.946  1.00 31.02           C  \nATOM    644  CE1 HIS A  86      -0.476  83.334 -12.130  1.00 30.65           C  \nATOM    645  NE2 HIS A  86      -0.809  82.341 -11.326  1.00 33.41           N  \nATOM    646  N   VAL A  87       3.197  79.656 -15.679  1.00 25.18           N  \nATOM    647  CA  VAL A  87       3.875  79.067 -16.832  1.00 26.69           C  \nATOM    648  C   VAL A  87       4.773  77.917 -16.390  1.00 25.89           C  \nATOM    649  O   VAL A  87       4.729  76.820 -16.966  1.00 26.66           O  \nATOM    650  CB  VAL A  87       4.652  80.153 -17.595  1.00 27.00           C  \nATOM    651  CG1 VAL A  87       5.353  79.559 -18.827  1.00 28.31           C  \nATOM    652  CG2 VAL A  87       3.703  81.270 -18.018  1.00 26.47           C  \nATOM    653  N   ALA A  88       5.563  78.132 -15.327  1.00 24.78           N  \nATOM    654  CA  ALA A  88       6.399  77.057 -14.798  1.00 25.49           C  \nATOM    655  C   ALA A  88       5.557  75.863 -14.381  1.00 27.14           C  \nATOM    656  O   ALA A  88       5.922  74.708 -14.651  1.00 25.14           O  \nATOM    657  CB  ALA A  88       7.235  77.559 -13.616  1.00 28.37           C  \nATOM    658  N   THR A  89       4.423  76.117 -13.725  1.00 25.85           N  \nATOM    659  CA  THR A  89       3.615  75.014 -13.227  1.00 25.58           C  \nATOM    660  C   THR A  89       2.992  74.247 -14.385  1.00 28.13           C  \nATOM    661  O   THR A  89       3.089  73.016 -14.447  1.00 27.52           O  \nATOM    662  CB  THR A  89       2.541  75.523 -12.263  1.00 27.49           C  \nATOM    663  OG1 THR A  89       3.163  76.114 -11.104  1.00 27.23           O  \nATOM    664  CG2 THR A  89       1.660  74.376 -11.819  1.00 26.49           C  \nATOM    665  N   MET A  90       2.359  74.965 -15.318  1.00 24.20           N  \nATOM    666  CA  MET A  90       1.839  74.345 -16.535  1.00 27.29           C  \nATOM    667  C   MET A  90       2.866  73.414 -17.177  1.00 25.63           C  \nATOM    668  O   MET A  90       2.578  72.237 -17.450  1.00 25.33           O  \nATOM    669  CB  MET A  90       1.422  75.444 -17.512  1.00 26.31           C  \nATOM    670  CG  MET A  90       0.875  74.956 -18.850  1.00 30.98           C  \nATOM    671  SD  MET A  90       0.758  76.333 -20.008  1.00 40.38           S  \nATOM    672  CE  MET A  90       0.697  77.696 -18.848  1.00 32.46           C  \nATOM    673  N   LEU A  91       4.086  73.923 -17.394  1.00 25.04           N  \nATOM    674  CA  LEU A  91       5.106  73.158 -18.113  1.00 26.89           C  \nATOM    675  C   LEU A  91       5.566  71.934 -17.328  1.00 28.18           C  \nATOM    676  O   LEU A  91       5.606  70.819 -17.870  1.00 26.54           O  \nATOM    677  CB  LEU A  91       6.304  74.050 -18.427  1.00 24.17           C  \nATOM    678  CG  LEU A  91       7.362  73.377 -19.294  1.00 28.33           C  \nATOM    679  CD1 LEU A  91       6.853  73.204 -20.730  1.00 25.91           C  \nATOM    680  CD2 LEU A  91       8.675  74.157 -19.231  1.00 26.85           C  \nATOM    681  N   LYS A  92       5.950  72.128 -16.058  1.00 24.02           N  \nATOM    682  CA  LYS A  92       6.435  71.010 -15.242  1.00 29.57           C  \nATOM    683  C   LYS A  92       5.351  69.957 -15.008  1.00 27.10           C  \nATOM    684  O   LYS A  92       5.648  68.755 -14.974  1.00 28.74           O  \nATOM    685  CB  LYS A  92       6.997  71.532 -13.906  1.00 27.76           C  \nATOM    686  CG  LYS A  92       8.360  72.220 -14.070  1.00 34.47           C  \nATOM    687  CD  LYS A  92       8.783  73.029 -12.844  1.00 36.71           C  \nATOM    688  CE  LYS A  92      10.171  73.627 -13.076  1.00 41.06           C  \nATOM    689  NZ  LYS A  92      10.394  74.878 -12.290  1.00 46.27           N  \nATOM    690  N   GLN A  93       4.089  70.375 -14.834  1.00 24.71           N  \nATOM    691  CA  GLN A  93       3.017  69.392 -14.710  1.00 26.42           C  \nATOM    692  C   GLN A  93       2.869  68.584 -15.989  1.00 28.28           C  \nATOM    693  O   GLN A  93       2.680  67.362 -15.938  1.00 27.96           O  \nATOM    694  CB  GLN A  93       1.684  70.063 -14.354  1.00 27.81           C  \nATOM    695  CG  GLN A  93       1.683  70.732 -12.956  1.00 25.80           C  \nATOM    696  CD  GLN A  93       1.394  69.760 -11.821  1.00 28.27           C  \nATOM    697  OE1 GLN A  93       0.524  68.896 -11.939  1.00 27.52           O  \nATOM    698  NE2 GLN A  93       2.124  69.906 -10.703  1.00 29.72           N  \nATOM    699  N   ALA A  94       2.950  69.252 -17.149  1.00 26.56           N  \nATOM    700  CA  ALA A  94       2.886  68.527 -18.421  1.00 30.68           C  \nATOM    701  C   ALA A  94       4.047  67.541 -18.569  1.00 29.32           C  \nATOM    702  O   ALA A  94       3.846  66.395 -18.991  1.00 28.92           O  \nATOM    703  CB  ALA A  94       2.870  69.516 -19.587  1.00 27.47           C  \nATOM    704  N   ILE A  95       5.269  67.967 -18.229  1.00 27.14           N  \nATOM    705  CA  ILE A  95       6.436  67.092 -18.355  1.00 28.45           C  \nATOM    706  C   ILE A  95       6.277  65.872 -17.457  1.00 30.97           C  \nATOM    707  O   ILE A  95       6.487  64.729 -17.887  1.00 32.77           O  \nATOM    708  CB  ILE A  95       7.728  67.868 -18.032  1.00 26.34           C  \nATOM    709  CG1 ILE A  95       7.990  68.936 -19.089  1.00 26.37           C  \nATOM    710  CG2 ILE A  95       8.935  66.929 -17.921  1.00 31.91           C  \nATOM    711  CD1 ILE A  95       9.168  69.837 -18.773  1.00 31.67           C  \nATOM    712  N   HIS A  96       5.864  66.096 -16.202  1.00 28.09           N  \nATOM    713  CA  HIS A  96       5.670  64.976 -15.289  1.00 29.49           C  \nATOM    714  C   HIS A  96       4.595  64.032 -15.795  1.00 33.05           C  \nATOM    715  O   HIS A  96       4.738  62.807 -15.697  1.00 33.00           O  \nATOM    716  CB  HIS A  96       5.304  65.478 -13.902  1.00 31.41           C  \nATOM    717  CG  HIS A  96       4.979  64.382 -12.939  1.00 33.72           C  \nATOM    718  ND1 HIS A  96       5.952  63.675 -12.263  1.00 33.51           N  \nATOM    719  CD2 HIS A  96       3.792  63.870 -12.535  1.00 34.98           C  \nATOM    720  CE1 HIS A  96       5.377  62.773 -11.489  1.00 32.53           C  \nATOM    721  NE2 HIS A  96       4.067  62.871 -11.633  1.00 37.48           N  \nATOM    722  N   HIS A  97       3.502  64.588 -16.329  1.00 28.96           N  \nATOM    723  CA  HIS A  97       2.420  63.755 -16.841  1.00 30.47           C  \nATOM    724  C   HIS A  97       2.887  62.913 -18.025  1.00 30.84           C  \nATOM    725  O   HIS A  97       2.535  61.734 -18.142  1.00 31.91           O  \nATOM    726  CB  HIS A  97       1.235  64.633 -17.250  1.00 25.84           C  \nATOM    727  CG  HIS A  97       0.029  63.855 -17.670  1.00 28.80           C  \nATOM    728  ND1 HIS A  97      -0.719  63.110 -16.785  1.00 27.82           N  \nATOM    729  CD2 HIS A  97      -0.549  63.691 -18.884  1.00 26.73           C  \nATOM    730  CE1 HIS A  97      -1.722  62.542 -17.430  1.00 30.61           C  \nATOM    731  NE2 HIS A  97      -1.639  62.876 -18.707  1.00 31.35           N  \nATOM    732  N   ALA A  98       3.654  63.516 -18.930  1.00 29.65           N  \nATOM    733  CA  ALA A  98       4.263  62.743 -20.008  1.00 31.95           C  \nATOM    734  C   ALA A  98       5.150  61.638 -19.456  1.00 38.35           C  \nATOM    735  O   ALA A  98       5.207  60.540 -20.020  1.00 39.16           O  \nATOM    736  CB  ALA A  98       5.073  63.664 -20.921  1.00 32.32           C  \nATOM    737  N   ASN A  99       5.822  61.895 -18.335  1.00 35.73           N  \nATOM    738  CA  ASN A  99       6.826  60.953 -17.866  1.00 40.79           C  \nATOM    739  C   ASN A  99       6.234  59.780 -17.097  1.00 42.87           C  \nATOM    740  O   ASN A  99       6.667  58.639 -17.290  1.00 46.14           O  \nATOM    741  CB  ASN A  99       7.848  61.679 -17.003  1.00 43.40           C  \nATOM    742  CG  ASN A  99       9.248  61.459 -17.488  1.00 52.89           C  \nATOM    743  OD1 ASN A  99       9.516  60.497 -18.211  1.00 54.33           O  \nATOM    744  ND2 ASN A  99      10.155  62.349 -17.106  1.00 57.38           N  \nATOM    745  N   HIS A 100       5.268  60.025 -16.212  1.00 41.11           N  \nATOM    746  CA  HIS A 100       4.863  58.984 -15.283  1.00 41.78           C  \nATOM    747  C   HIS A 100       4.125  57.863 -16.019  1.00 44.85           C  \nATOM    748  O   HIS A 100       3.599  58.064 -17.118  1.00 46.48           O  \nATOM    749  CB  HIS A 100       4.033  59.574 -14.133  1.00 40.94           C  \nATOM    750  CG  HIS A 100       2.646  60.018 -14.502  1.00 39.41           C  \nATOM    751  ND1 HIS A 100       1.651  59.141 -14.881  1.00 43.82           N  \nATOM    752  CD2 HIS A 100       2.069  61.244 -14.470  1.00 36.67           C  \nATOM    753  CE1 HIS A 100       0.532  59.812 -15.106  1.00 39.28           C  \nATOM    754  NE2 HIS A 100       0.760  61.092 -14.865  1.00 36.10           N  \nATOM    755  N   PRO A 101       4.129  56.652 -15.456  1.00 49.71           N  \nATOM    756  CA  PRO A 101       3.503  55.517 -16.144  1.00 48.75           C  \nATOM    757  C   PRO A 101       1.997  55.688 -16.242  1.00 50.40           C  \nATOM    758  O   PRO A 101       1.384  56.491 -15.536  1.00 50.91           O  \nATOM    759  CB  PRO A 101       3.858  54.316 -15.258  1.00 50.31           C  \nATOM    760  CG  PRO A 101       5.030  54.770 -14.435  1.00 50.23           C  \nATOM    761  CD  PRO A 101       4.806  56.234 -14.215  1.00 49.61           C  \nATOM    762  N   LYS A 102       1.403  54.897 -17.126  1.00 50.32           N  \nATOM    763  CA  LYS A 102      -0.027  54.963 -17.382  1.00 51.13           C  \nATOM    764  C   LYS A 102      -0.675  53.598 -17.168  1.00 53.68           C  \nATOM    765  O   LYS A 102      -1.898  53.495 -17.015  1.00 64.58           O  \nATOM    766  CB  LYS A 102      -0.291  55.458 -18.808  1.00 50.32           C  \nATOM    767  CG  LYS A 102       0.458  56.733 -19.199  1.00 50.14           C  \nATOM    768  CD  LYS A 102      -0.040  57.955 -18.429  1.00 45.69           C  \nATOM    769  CE  LYS A 102       0.612  59.230 -18.956  1.00 41.38           C  \nATOM    770  NZ  LYS A 102       2.104  59.178 -18.851  1.00 44.90           N  \nHETATM 1528  ZN   ZN A 201      -0.547  62.666 -14.786  1.00 31.02          ZN  \nHETATM 1529  CL   CL A 202      18.964  76.381 -35.199  1.00 30.15          CL  \nHETATM 1530  CL   CL A 203       1.992  61.240 -10.059  1.00 48.22          CL  \nHETATM 1531  CL   CL A 204      16.698  81.018 -12.347  1.00 64.21          CL  \nHETATM 1532  O1  PG4 A 205      10.096  67.125 -33.473  1.00 49.58           O  \nHETATM 1533  C1  PG4 A 205       9.530  68.141 -34.271  1.00 46.10           C  \nHETATM 1534  C2  PG4 A 205       8.282  68.741 -33.600  1.00 45.77           C  \nHETATM 1535  O2  PG4 A 205       8.367  70.148 -33.502  1.00 36.80           O  \nHETATM 1536  C3  PG4 A 205       7.405  70.822 -34.260  1.00 42.05           C  \nHETATM 1537  C4  PG4 A 205       7.778  72.276 -34.532  1.00 44.94           C  \nHETATM 1538  O3  PG4 A 205       6.795  72.867 -35.352  1.00 41.30           O  \nHETATM 1539  C5  PG4 A 205       5.789  73.571 -34.662  1.00 47.49           C  \nHETATM 1540  C6  PG4 A 205       5.350  74.846 -35.403  1.00 46.54           C  \nHETATM 1541  O4  PG4 A 205       6.414  75.777 -35.401  1.00 45.78           O  \nHETATM 1542  C7  PG4 A 205       6.034  77.121 -35.603  1.00 43.32           C  \nHETATM 1543  C8  PG4 A 205       7.148  77.898 -36.315  1.00 36.22           C  \nHETATM 1544  O5  PG4 A 205       6.703  79.163 -36.722  1.00 32.99           O  \nHETATM 1545  NA   NA A 206      12.143  70.532 -15.997  1.00 51.01          NA  \nHETATM 1548  O   HOH A 301      -4.831  80.255 -32.841  1.00 53.50           O  \nHETATM 1549  O   HOH A 302      14.220  88.715 -33.441  1.00 47.86           O  \nHETATM 1550  O   HOH A 303      10.981  77.030 -13.060  1.00 36.39           O  \nHETATM 1551  O   HOH A 304      24.869  71.137 -35.055  1.00 35.05           O  \nHETATM 1552  O   HOH A 305      15.727  71.395 -22.686  1.00 30.08           O  \nHETATM 1553  O   HOH A 306       6.265  88.086 -20.670  1.00 36.14           O  \nHETATM 1554  O   HOH A 307      12.769  80.652 -15.506  1.00 34.68           O  \nHETATM 1555  O   HOH A 308      19.538  71.077 -31.692  1.00 33.80           O  \nHETATM 1556  O   HOH A 309      16.783  67.146 -29.925  1.00 46.34           O  \nHETATM 1557  O   HOH A 310       2.260  86.987 -12.553  1.00 37.69           O  \nHETATM 1558  O   HOH A 311      14.376  87.202 -16.634  1.00 36.91           O  \nHETATM 1559  O   HOH A 312       0.291  80.696 -31.313  1.00 40.07           O  \nHETATM 1560  O   HOH A 313      26.322  73.978 -29.315  1.00 37.63           O  \nHETATM 1561  O   HOH A 314      19.126  69.088 -25.599  1.00 40.42           O  \nHETATM 1562  O   HOH A 315      15.654  70.134 -33.102  1.00 51.60           O  \nHETATM 1563  O   HOH A 316       7.537  82.477 -37.068  1.00 49.51           O  \nHETATM 1564  O   HOH A 317      23.698  86.159 -25.034  1.00 41.67           O  \nHETATM 1565  O   HOH A 318       8.407  68.051 -14.164  1.00 34.25           O  \nHETATM 1566  O   HOH A 319       5.205  90.849 -24.034  1.00 46.21           O  \nHETATM 1567  O   HOH A 320      17.630  71.714 -19.259  1.00 45.07           O  \nHETATM 1568  O   HOH A 321       5.223  84.276 -10.335  1.00 37.44           O  \nHETATM 1569  O   HOH A 322       3.051  53.700 -19.414  1.00 50.18           O  \nHETATM 1570  O   HOH A 323      -2.322  84.351 -25.562  1.00 42.81           O  \nHETATM 1571  O   HOH A 324      24.827  81.021 -33.302  1.00 33.60           O  \nHETATM 1572  O   HOH A 325      23.012  82.565 -18.864  1.00 43.22           O  \nHETATM 1573  O   HOH A 326       8.086  81.427 -11.754  1.00 44.77           O  \nHETATM 1574  O   HOH A 327       0.428  59.177 -11.380  1.00 43.79           O  \nHETATM 1575  O   HOH A 328      12.775  89.685 -15.825  1.00 53.23           O  \nHETATM 1576  O   HOH A 329       6.394  91.368 -26.409  1.00 44.30           O  \nHETATM 1577  O   HOH A 330       8.334  61.622  -9.397  1.00 41.71           O  \nHETATM 1578  O   HOH A 331      18.823  71.596 -22.008  1.00 39.77           O  \nHETATM 1579  O   HOH A 332       8.916  78.659 -10.480  1.00 44.23           O  \nHETATM 1580  O   HOH A 333      10.487  79.505 -13.480  1.00 37.28           O  \n");
	viewer_1730756471608242.setStyle({"model": -1},{"cartoon": {"color": "spectrum"}});
	viewer_1730756471608242.zoomTo();
viewer_1730756471608242.render();
});
</script>





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>10</th>
      <th>11</th>
      <th>12</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ATOM</td>
      <td>1</td>
      <td>N</td>
      <td>SER</td>
      <td>A</td>
      <td>6</td>
      <td>-12.615</td>
      <td>82.680</td>
      <td>-12.301</td>
      <td>1.00</td>
      <td>77.47</td>
      <td>N</td>
      <td></td>
    </tr>
    <tr>
      <th>1</th>
      <td>ATOM</td>
      <td>2</td>
      <td>CA</td>
      <td>SER</td>
      <td>A</td>
      <td>6</td>
      <td>-13.722</td>
      <td>82.765</td>
      <td>-13.253</td>
      <td>1.00</td>
      <td>79.72</td>
      <td>C</td>
      <td></td>
    </tr>
    <tr>
      <th>2</th>
      <td>ATOM</td>
      <td>3</td>
      <td>C</td>
      <td>SER</td>
      <td>A</td>
      <td>6</td>
      <td>-13.286</td>
      <td>83.466</td>
      <td>-14.546</td>
      <td>1.00</td>
      <td>75.97</td>
      <td>C</td>
      <td></td>
    </tr>
    <tr>
      <th>3</th>
      <td>ATOM</td>
      <td>4</td>
      <td>O</td>
      <td>SER</td>
      <td>A</td>
      <td>6</td>
      <td>-12.140</td>
      <td>83.325</td>
      <td>-14.972</td>
      <td>1.00</td>
      <td>77.43</td>
      <td>O</td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>ATOM</td>
      <td>5</td>
      <td>CB</td>
      <td>SER</td>
      <td>A</td>
      <td>6</td>
      <td>-14.920</td>
      <td>83.495</td>
      <td>-12.624</td>
      <td>1.00</td>
      <td>82.09</td>
      <td>C</td>
      <td></td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>816</th>
      <td>HETATM</td>
      <td>1576</td>
      <td>O</td>
      <td>HOH</td>
      <td>A</td>
      <td>329</td>
      <td>6.394</td>
      <td>91.368</td>
      <td>-26.409</td>
      <td>1.00</td>
      <td>44.30</td>
      <td>O</td>
      <td></td>
    </tr>
    <tr>
      <th>817</th>
      <td>HETATM</td>
      <td>1577</td>
      <td>O</td>
      <td>HOH</td>
      <td>A</td>
      <td>330</td>
      <td>8.334</td>
      <td>61.622</td>
      <td>-9.397</td>
      <td>1.00</td>
      <td>41.71</td>
      <td>O</td>
      <td></td>
    </tr>
    <tr>
      <th>818</th>
      <td>HETATM</td>
      <td>1578</td>
      <td>O</td>
      <td>HOH</td>
      <td>A</td>
      <td>331</td>
      <td>18.823</td>
      <td>71.596</td>
      <td>-22.008</td>
      <td>1.00</td>
      <td>39.77</td>
      <td>O</td>
      <td></td>
    </tr>
    <tr>
      <th>819</th>
      <td>HETATM</td>
      <td>1579</td>
      <td>O</td>
      <td>HOH</td>
      <td>A</td>
      <td>332</td>
      <td>8.916</td>
      <td>78.659</td>
      <td>-10.480</td>
      <td>1.00</td>
      <td>44.23</td>
      <td>O</td>
      <td></td>
    </tr>
    <tr>
      <th>820</th>
      <td>HETATM</td>
      <td>1580</td>
      <td>O</td>
      <td>HOH</td>
      <td>A</td>
      <td>333</td>
      <td>10.487</td>
      <td>79.505</td>
      <td>-13.480</td>
      <td>1.00</td>
      <td>37.28</td>
      <td>O</td>
      <td></td>
    </tr>
  </tbody>
</table>
<p>821 rows × 13 columns</p>
</div>




```python
# one more example
table[0, 'corex'] # Index row:0 and column:sasa
```


<div>                            <div id="a4b93515-cec0-431b-a8e5-4073a700b1b0" class="plotly-graph-div" style="height:525px; width:100%;"></div>            <script type="text/javascript">                require(["plotly"], function(Plotly) {                    window.PLOTLYENV=window.PLOTLYENV || {};                                    if (document.getElementById("a4b93515-cec0-431b-a8e5-4073a700b1b0")) {                    Plotly.newPlot(                        "a4b93515-cec0-431b-a8e5-4073a700b1b0",                        [{"hovertemplate":"x=%{x}\u003cbr\u003ey=%{y}\u003cextra\u003e\u003c\u002fextra\u003e","legendgroup":"","line":{"color":"#636efa","dash":"solid"},"marker":{"symbol":"circle"},"mode":"lines","name":"","orientation":"v","showlegend":false,"x":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96],"xaxis":"x","y":[-5.000873006361232,-5.000873006361232,-5.000873006361232,-5.000873006361232,-5.009685541903369,-4.937238112919677,-4.497895087709894,-3.9567944209500143,-3.6038903050003195,-3.280752244206353,-3.0249511364927026,-2.8917367439319017,-2.629197751435309,-2.3769898800571885,-2.3251066900766624,-2.2758657877828004,-1.8200395764391957,-1.3496257864683021,-1.129376026951422,0.2823768625263307,0.42393003122716755,0.48641748071438073,0.5440941953438235,0.5546978027736392,0.5674313914917283,0.5685389550557168,0.5712886038442245,0.5726394214609651,0.5743590898550064,0.5745213000706297,0.5745139436214154,0.5745031057400037,0.5745331606606977,0.5744144210408718,0.5745673106260467,0.5746244881643476,0.5744239474220431,0.5742481529465738,0.5742630115382257,0.5742806520618297,0.574313064646489,0.5743148466029661,0.5743170708237503,0.5743336540497628,0.5743236304649434,0.5745451772614484,0.5751369351917877,0.5754454744826817,0.5755907609956653,0.5756319150093764,0.575738025954661,0.5759619684714403,0.5760049801184507,0.5760720819403612,0.5760807053762048,0.5758151590149188,0.5755231703461398,0.5754346406959584,0.5753637074100163,0.5749468617303923,0.5740684020195927,0.5732723509296567,0.5730010683386203,0.5725376300626284,0.5704798303719094,0.5701057720215426,0.5702887635760368,0.5702906855726877,0.5702904159707204,0.5702898505643696,0.5702899459474376,0.5702902366372987,0.5702948414172867,0.570413335985925,0.5719105097171882,0.5703129765075711,0.4598585290165194,0.26636983820680277,0.09016816940170262,-1.227492996693632,-1.3529355331789066,-1.4172473603718119,-1.5558116715828312,-1.6435676864316937,-1.6862351404502798,-1.7176256156870429,-1.9194634569141185,-2.207404432039211,-2.257785885531128,-2.8181720888310755,-3.325771006369682,-3.6346376052314646,-3.841124868644924,-4.104470027861705,-4.104470027861705,-4.104470027861705,-4.104470027861705],"yaxis":"y","type":"scatter"}],                        {"template":{"data":{"histogram2dcontour":[{"type":"histogram2dcontour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"choropleth":[{"type":"choropleth","colorbar":{"outlinewidth":0,"ticks":""}}],"histogram2d":[{"type":"histogram2d","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"heatmap":[{"type":"heatmap","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"heatmapgl":[{"type":"heatmapgl","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"contourcarpet":[{"type":"contourcarpet","colorbar":{"outlinewidth":0,"ticks":""}}],"contour":[{"type":"contour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"surface":[{"type":"surface","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"mesh3d":[{"type":"mesh3d","colorbar":{"outlinewidth":0,"ticks":""}}],"scatter":[{"fillpattern":{"fillmode":"overlay","size":10,"solidity":0.2},"type":"scatter"}],"parcoords":[{"type":"parcoords","line":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolargl":[{"type":"scatterpolargl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"bar":[{"error_x":{"color":"#2a3f5f"},"error_y":{"color":"#2a3f5f"},"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"bar"}],"scattergeo":[{"type":"scattergeo","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolar":[{"type":"scatterpolar","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"histogram":[{"marker":{"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"histogram"}],"scattergl":[{"type":"scattergl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatter3d":[{"type":"scatter3d","line":{"colorbar":{"outlinewidth":0,"ticks":""}},"marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattermapbox":[{"type":"scattermapbox","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterternary":[{"type":"scatterternary","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattercarpet":[{"type":"scattercarpet","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"carpet":[{"aaxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"baxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"type":"carpet"}],"table":[{"cells":{"fill":{"color":"#EBF0F8"},"line":{"color":"white"}},"header":{"fill":{"color":"#C8D4E3"},"line":{"color":"white"}},"type":"table"}],"barpolar":[{"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"barpolar"}],"pie":[{"automargin":true,"type":"pie"}]},"layout":{"autotypenumbers":"strict","colorway":["#636efa","#EF553B","#00cc96","#ab63fa","#FFA15A","#19d3f3","#FF6692","#B6E880","#FF97FF","#FECB52"],"font":{"color":"#2a3f5f"},"hovermode":"closest","hoverlabel":{"align":"left"},"paper_bgcolor":"white","plot_bgcolor":"#E5ECF6","polar":{"bgcolor":"#E5ECF6","angularaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"radialaxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"ternary":{"bgcolor":"#E5ECF6","aaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"baxis":{"gridcolor":"white","linecolor":"white","ticks":""},"caxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"coloraxis":{"colorbar":{"outlinewidth":0,"ticks":""}},"colorscale":{"sequential":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"sequentialminus":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"diverging":[[0,"#8e0152"],[0.1,"#c51b7d"],[0.2,"#de77ae"],[0.3,"#f1b6da"],[0.4,"#fde0ef"],[0.5,"#f7f7f7"],[0.6,"#e6f5d0"],[0.7,"#b8e186"],[0.8,"#7fbc41"],[0.9,"#4d9221"],[1,"#276419"]]},"xaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"yaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"scene":{"xaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"yaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"zaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2}},"shapedefaults":{"line":{"color":"#2a3f5f"}},"annotationdefaults":{"arrowcolor":"#2a3f5f","arrowhead":0,"arrowwidth":1},"geo":{"bgcolor":"white","landcolor":"#E5ECF6","subunitcolor":"white","showland":true,"showlakes":true,"lakecolor":"white"},"title":{"x":0.05},"mapbox":{"style":"light"}}},"xaxis":{"anchor":"y","domain":[0.0,1.0],"title":{"text":"x"}},"yaxis":{"anchor":"x","domain":[0.0,1.0],"title":{"text":"y"}},"legend":{"tracegroupgap":0},"title":{"text":"COREX (ln(kf)) Values"}},                        {"responsive": true}                    ).then(function(){

var gd = document.getElementById('a4b93515-cec0-431b-a8e5-4073a700b1b0');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })                };                });            </script>        </div>





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>...</th>
      <th>87</th>
      <th>88</th>
      <th>89</th>
      <th>90</th>
      <th>91</th>
      <th>92</th>
      <th>93</th>
      <th>94</th>
      <th>95</th>
      <th>96</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-5.000873</td>
      <td>-5.000873</td>
      <td>-5.000873</td>
      <td>-5.000873</td>
      <td>-5.009686</td>
      <td>-4.937238</td>
      <td>-4.497895</td>
      <td>-3.956794</td>
      <td>-3.60389</td>
      <td>-3.280752</td>
      <td>...</td>
      <td>-2.207404</td>
      <td>-2.257786</td>
      <td>-2.818172</td>
      <td>-3.325771</td>
      <td>-3.634638</td>
      <td>-3.841125</td>
      <td>-4.10447</td>
      <td>-4.10447</td>
      <td>-4.10447</td>
      <td>-4.10447</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 97 columns</p>
</div>




```python
# Get the values of SASA as a python list
table[0, 'corex'].value
```




    [-5.000873006361232,
     -5.000873006361232,
     -5.000873006361232,
     -5.000873006361232,
     -5.009685541903369,
     -4.937238112919677,
     -4.497895087709894,
     -3.9567944209500143,
     -3.6038903050003195,
     -3.280752244206353,
     -3.0249511364927026,
     -2.8917367439319017,
     -2.629197751435309,
     -2.3769898800571885,
     -2.3251066900766624,
     -2.2758657877828004,
     -1.8200395764391957,
     -1.3496257864683021,
     -1.129376026951422,
     0.2823768625263307,
     0.42393003122716755,
     0.48641748071438073,
     0.5440941953438235,
     0.5546978027736392,
     0.5674313914917283,
     0.5685389550557168,
     0.5712886038442245,
     0.5726394214609651,
     0.5743590898550064,
     0.5745213000706297,
     0.5745139436214154,
     0.5745031057400037,
     0.5745331606606977,
     0.5744144210408718,
     0.5745673106260467,
     0.5746244881643476,
     0.5744239474220431,
     0.5742481529465738,
     0.5742630115382257,
     0.5742806520618297,
     0.574313064646489,
     0.5743148466029661,
     0.5743170708237503,
     0.5743336540497628,
     0.5743236304649434,
     0.5745451772614484,
     0.5751369351917877,
     0.5754454744826817,
     0.5755907609956653,
     0.5756319150093764,
     0.575738025954661,
     0.5759619684714403,
     0.5760049801184507,
     0.5760720819403612,
     0.5760807053762048,
     0.5758151590149188,
     0.5755231703461398,
     0.5754346406959584,
     0.5753637074100163,
     0.5749468617303923,
     0.5740684020195927,
     0.5732723509296567,
     0.5730010683386203,
     0.5725376300626284,
     0.5704798303719094,
     0.5701057720215426,
     0.5702887635760368,
     0.5702906855726877,
     0.5702904159707204,
     0.5702898505643696,
     0.5702899459474376,
     0.5702902366372987,
     0.5702948414172867,
     0.570413335985925,
     0.5719105097171882,
     0.5703129765075711,
     0.4598585290165194,
     0.26636983820680277,
     0.09016816940170262,
     -1.227492996693632,
     -1.3529355331789066,
     -1.4172473603718119,
     -1.5558116715828312,
     -1.6435676864316937,
     -1.6862351404502798,
     -1.7176256156870429,
     -1.9194634569141185,
     -2.207404432039211,
     -2.257785885531128,
     -2.8181720888310755,
     -3.325771006369682,
     -3.6346376052314646,
     -3.841124868644924,
     -4.104470027861705,
     -4.104470027861705,
     -4.104470027861705,
     -4.104470027861705]



## Customization Tutorial

We have done basic tutorial. This tutorial used `read-corex`.  
The previous tutorial only allows you to upload a series of PDB and calculate.  
But, it is more powerful than that to allow you to customize more things here.


```python
# First let is fetch the data as before
table = build_table_with_pdb('data')
table
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>path</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>data\6cdb.pdb</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Show workflow documentation
workbench['read-corex']
```




### COREX (Local Files)  

Run COREX for local PDB files.  
  
#### Parameters  
- **path**: (string:**string**)=`None`; The path to the target file; (`None`)   
- **chain**: (string:**PDB Chain IDs**)_[OPTIONAL]_=`A`; The selected protein chains ID.; (`[A-Za-z0-9]+(,[A-Za-z0-9]+)*`) The protein chain ids, seperate with `,`, no blank character.  
- **window_size**: (number:**float>1**)_[OPTIONAL]_=`10`; The protein folding unit size. Also, the number of partition schemes.; (`{'min': 1}`) The float number that is greater than 1.  
- **min_size**: (number:**float>1**)_[OPTIONAL]_=`4`; The minumum protein folding unit size.; (`{'min': 1}`) The float number that is greater than 1.  
- **samples**: (number:**float>1**)_[OPTIONAL]_=`10000`; (Ignore for exhaustive sampling) The sample number for each partition scheme. Total sample number=samples*window_size.; (`{'min': 1}`) The float number that is greater than 1.  
- **sampler**: (string:**COREX Sampler**)_[OPTIONAL]_=`exhaustive`; The COREX states sampler; (`(exhaustive|montecarlo|adaptive)`) (exhaustive|montecarlo|adaptive) The COREX micro-states sampler, which could be exhaustive enumerate, Monte Carlo, or Adaptibe Monte Carlo sampler.  
- **threshold**: (number:**float>0**)_[OPTIONAL]_=`0.75`; (Ignore for exhaustive sampling) The threshold for the sampler.; (`{'min': 0}`) The float number that is greater than 0.  
- **sconf_weight**: (number:**float>0**)_[OPTIONAL]_=`1.0`; Entropy factor.; (`{'min': 0}`) The float number that is greater than 0.  
- **base_fraction**: (number:**float>0**)_[OPTIONAL]_=`1.0`; The base fraction used to sum all COREX (ln_kf) values.; (`{'min': 0}`) The float number that is greater than 0.  
- **probe_radius**: (number:**float>1**)_[OPTIONAL]_=`1.4`; The probe radius for SASA in A.; (`{'min': 1}`) The float number that is greater than 1.  
- **n_points**: (number:**float>1**)_[OPTIONAL]_=`1000`; The number of test points in Shrake & Rupley algorithm for SASA.; (`{'min': 1}`) The float number that is greater than 1.  
#### Returns  
- **pdb**: (string:**PDB File**)=`None`; The output PDB file that only contains selected chains.; (`None`) The protein PDB file  
- **pdb_id**: (string:**string**)=`None`; The file name; (`None`)   
- **chain**: (string:**PDB Chain IDs**)=`None`; The chains contained in the PDB files.; (`[A-Za-z0-9]+(,[A-Za-z0-9]+)*`) The protein chain ids, seperate with `,`, no blank character.  
- **corex**: (numarray:**COREX (ln(kf)) Values**)=`None`; The COREX values. The order is the same order as the PDB.; (`None`) COREX Values in Sorted Chain ID Order  





```python
# From the documentation, we could see the default COREX sampling method is `exhaustive`.
# Let is change this optional parameter to run Monte Carlo.
table[0, 'sampler'] = 'montecarlo' # Set sampler for the first row
table[0, 'samples'] = 50 # Because the protein is small, there is not enough samples, therefore, use smaller sample scale.
table
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>path</th>
      <th>sampler</th>
      <th>samples</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>data\6cdb.pdb</td>
      <td>montecarlo</td>
      <td>50</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Now workflow `read-corex` will run montecarlo with 50 sample number for the first PDB file
# You could also set different sampler of other parameters for different rows if you have multiple PDBs.
workbench['read-corex'](table)
```

    [9.4s] ✓ Task (COREX) CORrelation with hydrogen EXchange protection factors Finished.




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>path</th>
      <th>sampler</th>
      <th>samples</th>
      <th>pdb_id</th>
      <th>pdb</th>
      <th>chain</th>
      <th>corex</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>data\6cdb.pdb</td>
      <td>montecarlo</td>
      <td>50</td>
      <td>6cdb</td>
      <td>PDB:821 lines</td>
      <td>A</td>
      <td>COREX (ln(kf)) Values:[-2.76049764379143, -2.7...</td>
    </tr>
  </tbody>
</table>
</div>



**More customization!**  
It is not convient if you have a large scale of data.  
Therefore, we also enable read a Excel (xlsx) or CSV (csv) file to load the parameters.  
However, `read-corex` is not support to load a sheet file.  
But we could combine workflow by ourselves to enable this.


```python
# First, check what workflow we have
workbench
```




# COREX WorkBench (1.0)  
Provide a set of tools and workflows for COREX computations  
## Workflows  
- **read-corex**: **COREX (Local Files)**: Run COREX for local PDB files.  
- **read-sasa**: **SASA (Local Files)**: Run SASA for local PDB files.  
- **read-bfactor**: **B-Factor (Local Files)**: Fetch residue level b-factor for local PDB files.  
- **read-all**: **Run all things (Local Files)**: Calculate COREX, SASA, and B-factor for local PDB files.  
- **read-pdbs**: **Run PDB files**: Read local PDB files and select chain.  
- **read-table**: **Fetch Local Sheet**: Fetch parameters from local sheet file.  
- **corex**: **COREX**: Run COREX for the pdb column.  
- **sasa**: **SASA**: Run SASA for pdb column.  
- **bfactor**: **B-Factor**: Fetch residue level b-factor for PDB column.  
- **all**: **Run all things**: Calculate COREX, SASA, and B-factor for PDB column.  
## LibIndex  
`2 libs` `8 Algorithms`

  
### local  
- **read-file**: Read local files from the given path.  
- **read-sheet**: Read local sheet file and attach to the table.  


  
### Jellyroll Bioinformatics  
- **select-chain**: Select destinated chains from the given PDB file.  
- **sasa**: Calculate the solvent accessible surface area for the given protein. The results will be an array concatenated by the order of sorted(chains)  
- **corex**: An algorithm designed to compute comformational stability of a protein. The results will be an array concatenated by the order of sorted(chains)  
- **list-chain**: List all chains from the given PDB file.  
- **bfactor**: Extract residue level B-Factor from the given PDB file (The B-Factor of CA atom).  
- **get-pdb**: Get PDB file by PDB ID.  


  
  




From this documentation, we could find that, `read-corex` is actually the combination of `read-pdbs` and `corex`.  
And, `read-table` could allow us to load a sheet file.  
Therefore, we could assemble a workflow use these existed workflows to achieve our goal.  


```python
# This new workflow will follow the order of the index order
our_workflow = workbench['read-pdbs', 'read-table', 'corex']
# The documentation will be automatically analyzed and generated
our_workflow
```




### Combined Workflows  

read-pdbs> read-table> corex  
  
#### Parameters  
- **path**: (string:**string**)=`None`; The path to the target file; (`None`)   
- **chain**: (string:**PDB Chain IDs**)_[OPTIONAL]_=`A`; The selected protein chains ID.; (`[A-Za-z0-9]+(,[A-Za-z0-9]+)*`) The protein chain ids, seperate with `,`, no blank character.  
- **sheet_path**: (string:**string**)=`None`; The path to the target sheet file (.csv or .xlsx); (`None`)   
- **window_size**: (number:**float>1**)_[OPTIONAL]_=`10`; The protein folding unit size. Also, the number of partition schemes.; (`{'min': 1}`) The float number that is greater than 1.  
- **min_size**: (number:**float>1**)_[OPTIONAL]_=`4`; The minumum protein folding unit size.; (`{'min': 1}`) The float number that is greater than 1.  
- **samples**: (number:**float>1**)_[OPTIONAL]_=`10000`; (Ignore for exhaustive sampling) The sample number for each partition scheme. Total sample number=samples*window_size.; (`{'min': 1}`) The float number that is greater than 1.  
- **sampler**: (string:**COREX Sampler**)_[OPTIONAL]_=`exhaustive`; The COREX states sampler; (`(exhaustive|montecarlo|adaptive)`) (exhaustive|montecarlo|adaptive) The COREX micro-states sampler, which could be exhaustive enumerate, Monte Carlo, or Adaptibe Monte Carlo sampler.  
- **threshold**: (number:**float>0**)_[OPTIONAL]_=`0.75`; (Ignore for exhaustive sampling) The threshold for the sampler.; (`{'min': 0}`) The float number that is greater than 0.  
- **sconf_weight**: (number:**float>0**)_[OPTIONAL]_=`1.0`; Entropy factor.; (`{'min': 0}`) The float number that is greater than 0.  
- **base_fraction**: (number:**float>0**)_[OPTIONAL]_=`1.0`; The base fraction used to sum all COREX (ln_kf) values.; (`{'min': 0}`) The float number that is greater than 0.  
- **probe_radius**: (number:**float>1**)_[OPTIONAL]_=`1.4`; The probe radius for SASA in A.; (`{'min': 1}`) The float number that is greater than 1.  
- **n_points**: (number:**float>1**)_[OPTIONAL]_=`1000`; The number of test points in Shrake & Rupley algorithm for SASA.; (`{'min': 1}`) The float number that is greater than 1.  
#### Returns  
- **pdb**: (string:**PDB File**)=`None`; The output PDB file that only contains selected chains.; (`None`) The protein PDB file  
- **pdb_id**: (string:**string**)=`None`; The file name; (`None`)   
- **chain**: (string:**PDB Chain IDs**)=`None`; The chains contained in the PDB files.; (`[A-Za-z0-9]+(,[A-Za-z0-9]+)*`) The protein chain ids, seperate with `,`, no blank character.  
- **corex**: (numarray:**COREX (ln(kf)) Values**)=`None`; The COREX values. The order is the same order as the PDB.; (`None`) COREX Values in Sorted Chain ID Order  





```python
# Now, we see, for our new workflow, there is one more parameter requried that is sheet_path for the Excel/CSV.
# Build Table from PDB files
table = build_table_with_pdb('data')
table[:, 'sheet_path'] = 'parameters.xlsx' # Set sheet_path to be our example sheet `parameters.xlsx`
# `parameters.xlsx`
# The first row is the index, which related to the pdb_id, which is the same as file name without suffix.
# Each column will be a property write as a new column in the data table
```


```python
# Now, let's try it!
tale = our_workflow(table)
```

    [8.9s] ✓ Task (COREX) CORrelation with hydrogen EXchange protection factors Finished.


```python
table[0, 'corex']
```






<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>...</th>
      <th>87</th>
      <th>88</th>
      <th>89</th>
      <th>90</th>
      <th>91</th>
      <th>92</th>
      <th>93</th>
      <th>94</th>
      <th>95</th>
      <th>96</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2.120279</td>
      <td>2.120279</td>
      <td>2.120279</td>
      <td>2.120279</td>
      <td>2.263343</td>
      <td>2.628881</td>
      <td>3.209727</td>
      <td>3.475768</td>
      <td>3.660153</td>
      <td>3.875141</td>
      <td>...</td>
      <td>4.232127</td>
      <td>3.504005</td>
      <td>2.833538</td>
      <td>2.276724</td>
      <td>1.987038</td>
      <td>1.826393</td>
      <td>1.592688</td>
      <td>1.592688</td>
      <td>1.592688</td>
      <td>1.592688</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 97 columns</p>
</div>




```python
# We could also see, there are workflow supports SASA and B-factor
# Let is combine them together
workbench['read-pdbs', , 'read-table', 'sasa', 'bfactor', 'corex']
```




### Combined Workflows  

read-pdbs> read-table> sasa> bfactor> corex  
  
#### Parameters  
- **path**: (string:**string**)=`None`; The path to the target file; (`None`)   
- **chain**: (string:**PDB Chain IDs**)_[OPTIONAL]_=`A`; The selected protein chains ID.; (`[A-Za-z0-9]+(,[A-Za-z0-9]+)*`) The protein chain ids, seperate with `,`, no blank character.  
- **sheet_path**: (string:**string**)=`None`; The path to the target sheet file (.csv or .xlsx); (`None`)   
- **algorithm**: (string:**SASA Algorithm**)_[OPTIONAL]_=`ShrakeRupley`; The SASA algorithms.; (`(ShrakeRupley|LeeRichards)`) (ShrakeRupley|LeeRichards) The SASA Algorithm that could be ShrakeRupley or LeeRichards.  
- **probe_radius**: (number:**float>1**)_[OPTIONAL]_=`1.4`; The probe radius in A.; (`{'min': 1}`) The float number that is greater than 1.  
- **n_points**: (number:**float>1**)_[OPTIONAL]_=`1000`; The number of test points in Shrake & Rupley algorithm.; (`{'min': 1}`) The float number that is greater than 1.  
- **n_slices**: (number:**float>1**)_[OPTIONAL]_=`20`; Get the number of slices per atom in Lee & Richards algorithm.; (`{'min': 1}`) The float number that is greater than 1.  
- **record**: (string:**PDB record**)_[OPTIONAL]_=`ATOM`; The PDB record for B-Factor extraction.; (`(ATOM|HETATM)`) (ATOM|HETATM) PDB record names which could be ATOM or HETATM  
- **window_size**: (number:**float>1**)_[OPTIONAL]_=`10`; The protein folding unit size. Also, the number of partition schemes.; (`{'min': 1}`) The float number that is greater than 1.  
- **min_size**: (number:**float>1**)_[OPTIONAL]_=`4`; The minumum protein folding unit size.; (`{'min': 1}`) The float number that is greater than 1.  
- **samples**: (number:**float>1**)_[OPTIONAL]_=`10000`; (Ignore for exhaustive sampling) The sample number for each partition scheme. Total sample number=samples*window_size.; (`{'min': 1}`) The float number that is greater than 1.  
- **sampler**: (string:**COREX Sampler**)_[OPTIONAL]_=`exhaustive`; The COREX states sampler; (`(exhaustive|montecarlo|adaptive)`) (exhaustive|montecarlo|adaptive) The COREX micro-states sampler, which could be exhaustive enumerate, Monte Carlo, or Adaptibe Monte Carlo sampler.  
- **threshold**: (number:**float>0**)_[OPTIONAL]_=`0.75`; (Ignore for exhaustive sampling) The threshold for the sampler.; (`{'min': 0}`) The float number that is greater than 0.  
- **sconf_weight**: (number:**float>0**)_[OPTIONAL]_=`1.0`; Entropy factor.; (`{'min': 0}`) The float number that is greater than 0.  
- **base_fraction**: (number:**float>0**)_[OPTIONAL]_=`1.0`; The base fraction used to sum all COREX (ln_kf) values.; (`{'min': 0}`) The float number that is greater than 0.  
#### Returns  
- **pdb**: (string:**PDB File**)=`None`; The output PDB file that only contains selected chains.; (`None`) The protein PDB file  
- **pdb_id**: (string:**string**)=`None`; The file name; (`None`)   
- **chain**: (string:**PDB Chain IDs**)=`None`; The chains contained in the PDB files.; (`[A-Za-z0-9]+(,[A-Za-z0-9]+)*`) The protein chain ids, seperate with `,`, no blank character.  
- **sasa**: (numarray:**SASA Values**)=`None`; The solvent accessible surface area. The order is the same order as the PDB.; (`None`) SASA Values in Sorted Chain ID Order  
- **bfactor**: (numarray:**B-Factor Values**)=`None`; The B-Factor. The order is the same order as the PDB.; (`None`) B-Factor values in given PDB file atom orders  
- **corex**: (numarray:**COREX (ln(kf)) Values**)=`None`; The COREX values. The order is the same order as the PDB.; (`None`) COREX Values in Sorted Chain ID Order  





```python
table = build_table_with_pdb('data')
table[:, 'sheet_path'] = 'parameters.xlsx'
workbench['read-pdbs', 'read-table', 'sasa', 'bfactor', 'corex'](table)
```

    [8.7s] ✓ Task (COREX) CORrelation with hydrogen EXchange protection factors Finished.




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>path</th>
      <th>sheet_path</th>
      <th>pdb_id</th>
      <th>pdb</th>
      <th>chain</th>
      <th>sampler</th>
      <th>sasa</th>
      <th>bfactor</th>
      <th>corex</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>data\6cdb.pdb</td>
      <td>parameters.xlsx</td>
      <td>6cdb</td>
      <td>PDB:821 lines</td>
      <td>A</td>
      <td>exhaustive</td>
      <td>SASA Values:[1.2696183006775639, 0.84657581949...</td>
      <td>B-Factor Values:[79.72, 72.64, 64.68]...(97)</td>
      <td>COREX (ln(kf)) Values:[-5.000873006361232, -5....</td>
    </tr>
  </tbody>
</table>
</div>



## Advanced Tutorial

For this section, we will have a guide line that how to define your own workflow and add new computational resource.

**Build Workflow**  
You could build your own workflow by combine tools.

Let is build a workflow to fetch a PDB from RCSB and compute COREX for it.


```python
new_workflow = ct.Workflow(
    workbench.toolkits['get-pdb'](pdb='pdb'),  # The fetch-pdb tool used to fetch pdb, and the parameter allow you to change the input and output column name.
    workbench.toolkits['select-chain'](pdb='pdb'), # Select Chain
    workbench.toolkits['list-chain'](pdb='pdb'), # List Chain
    workbench.toolkits['corex'](pdb='pdb'), # Compute COREX
    name = 'COREX (Fetch From RCSB)', # name for this workflow
    desc = 'Run COREX on fetched PDB files', # description for this workflow
)
# There maybe the same tool from different toolkits(source). CalTable will automatically choose one.
# The documentation for this workflow will be automatically inferred by CalTable
new_workflow
```




### COREX (Fetch From RCSB)  

Run COREX on fetched PDB files  
  
#### Parameters  
- **pdb_id**: (string:**PDB ID**)=`None`; The PDB ID or UniProt ID.; (`[A-Za-z0-9]{4}|[A-Za-z0-9]{6}`) The PDB ID, which can be 4 chars for RCSB or 6 chars for UniProt.  
- **source**: (string:**The PDB Source**)_[OPTIONAL]_=`alphafold2-v4`; (Ignore for 4 chars PDB ID) The PDB fetch source for UniProt.; (`alphafold2-v3|alphafold2-v4`) (alphafold2-v3|alphafold2-v4) The PDB fetch source which could be alphafold2-v3 or alphafold2-v4  
- **chain**: (string:**PDB Chain IDs**)_[OPTIONAL]_=`A`; The selected protein chains ID.; (`[A-Za-z0-9]+(,[A-Za-z0-9]+)*`) The protein chain ids, seperate with `,`, no blank character.  
- **window_size**: (number:**float>1**)_[OPTIONAL]_=`10`; The protein folding unit size. Also, the number of partition schemes.; (`{'min': 1}`) The float number that is greater than 1.  
- **min_size**: (number:**float>1**)_[OPTIONAL]_=`4`; The minumum protein folding unit size.; (`{'min': 1}`) The float number that is greater than 1.  
- **samples**: (number:**float>1**)_[OPTIONAL]_=`10000`; (Ignore for exhaustive sampling) The sample number for each partition scheme. Total sample number=samples*window_size.; (`{'min': 1}`) The float number that is greater than 1.  
- **sampler**: (string:**COREX Sampler**)_[OPTIONAL]_=`exhaustive`; The COREX states sampler; (`(exhaustive|montecarlo|adaptive)`) (exhaustive|montecarlo|adaptive) The COREX micro-states sampler, which could be exhaustive enumerate, Monte Carlo, or Adaptibe Monte Carlo sampler.  
- **threshold**: (number:**float>0**)_[OPTIONAL]_=`0.75`; (Ignore for exhaustive sampling) The threshold for the sampler.; (`{'min': 0}`) The float number that is greater than 0.  
- **sconf_weight**: (number:**float>0**)_[OPTIONAL]_=`1.0`; Entropy factor.; (`{'min': 0}`) The float number that is greater than 0.  
- **base_fraction**: (number:**float>0**)_[OPTIONAL]_=`1.0`; The base fraction used to sum all COREX (ln_kf) values.; (`{'min': 0}`) The float number that is greater than 0.  
- **probe_radius**: (number:**float>1**)_[OPTIONAL]_=`1.4`; The probe radius for SASA in A.; (`{'min': 1}`) The float number that is greater than 1.  
- **n_points**: (number:**float>1**)_[OPTIONAL]_=`1000`; The number of test points in Shrake & Rupley algorithm for SASA.; (`{'min': 1}`) The float number that is greater than 1.  
#### Returns  
- **pdb**: (string:**PDB File**)=`None`; The output PDB file that only contains selected chains.; (`None`) The protein PDB file  
- **chain**: (string:**PDB Chain IDs**)=`None`; The chains contained in the PDB files.; (`[A-Za-z0-9]+(,[A-Za-z0-9]+)*`) The protein chain ids, seperate with `,`, no blank character.  
- **corex**: (numarray:**COREX (ln(kf)) Values**)=`None`; The COREX values. The order is the same order as the PDB.; (`None`) COREX Values in Sorted Chain ID Order  





```python
# You could check the tool documentation following
workbench.toolkits['get-pdb']()
```




### Get PDB file  

Get PDB file by PDB ID.  
  
#### Parameters  
- **pdb_id**: (string:**PDB ID**)=`None`; The PDB ID or UniProt ID.; (`[A-Za-z0-9]{4}|[A-Za-z0-9]{6}`) The PDB ID, which can be 4 chars for RCSB or 6 chars for UniProt.  
- **source**: (string:**The PDB Source**)_[OPTIONAL]_=`alphafold2-v4`; (Ignore for 4 chars PDB ID) The PDB fetch source for UniProt.; (`alphafold2-v3|alphafold2-v4`) (alphafold2-v3|alphafold2-v4) The PDB fetch source which could be alphafold2-v3 or alphafold2-v4  
#### Returns  
- **pdb**: (string:**PDB File**)=`None`; The fetched PDB file.; (`None`) The protein PDB file  





```python
# Now, the input only pdb_id is required.
# We could create the table in different way:
# We could also customize parameter here
table = ct.DataTable([{'pdb_id':'6CDB', 'sampler':'exhaustive'}, # For 6CDB we use Exhaustive
                      {'pdb_id':'1AOL', 'sampler':'adaptive'},]) # For 1AOL we use Exhaustive
table
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>pdb_id</th>
      <th>sampler</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>6CDB</td>
      <td>exhaustive</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1AOL</td>
      <td>adaptive</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Let's try it!
table = new_workflow(table)
table
```

    [1m7.1s] ✓ Task (COREX) CORrelation with hydrogen EXchange protection factors Finished.




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>pdb_id</th>
      <th>sampler</th>
      <th>pdb</th>
      <th>chain</th>
      <th>corex</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>6CDB</td>
      <td>exhaustive</td>
      <td>PDB:821 lines</td>
      <td>A</td>
      <td>COREX (ln(kf)) Values:[-5.000873006361232, -5....</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1AOL</td>
      <td>adaptive</td>
      <td>PDB:2007 lines</td>
      <td>A</td>
      <td>COREX (ln(kf)) Values:[19.610296569177322, 19....</td>
    </tr>
  </tbody>
</table>
</div>



The CalTable could auto decide which server to use, built also, you could force it to choose one:


```python
new_workflow = ct.Workflow(
    workbench.toolkits['get-pdb'](pdb='pdb'),  # The fetch-pdb tool used to fetch pdb, and the parameter allow you to change the input and output column name.
    workbench.toolkits['select-chain'](pdb='pdb'), # Select Chain
    workbench.toolkits['list-chain'](pdb='pdb'), # List Chain
    workbench.toolkits['corex:Jellyroll Bioinformatics'](pdb='pdb'), # Compute COREX (Force Jellyroll server)
    name = 'COREX (Fetch From RCSB)', # name for this workflow
    desc = 'Run COREX on fetched PDB files', # description for this workflow
)
```

### Add New Computation Resource
Except Jellyroll, we could also add more resource for more tools.


```python
# workbench.toolkits.add(ct.RemoteCalBlockLib(host='', api_id='', api_key=''))
```

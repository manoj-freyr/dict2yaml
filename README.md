# dict2yaml
<p>Simple dictionary to yaml converter.<br>
reads in dict and spits out yaml, <br>
Now tightly coupled with ROCm configurations as per RVS : https://github.com/ROCm-Developer-Tools/ROCmValidationSuite/tree/master/rvs/conf </p>


# Usage
  `python utils.py <conf filename>`<br>
  reads the file and uses it to list out all the parameters in the conf and spit out a dictionary which has param_name and data type.<br>
  
  `python runner.py` <br>
  takes input list of dictionaries and spits out a yaml file based on input. Can be used to trigger rvs runs<br>

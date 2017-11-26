# ipy-storage
Store and retrieve object sets in ipython! 


Create different object sets in ipython for your different experiments or projects! Better than that pesky native ```%store``` as it uses ```dill``` as backend (instead of ```pickle```) and allows you to better manage your objects dividing them in sets.

It may or may not work with jupyter and other kernels, testing is still due.

## Instalation

### Pre-requisites
It works with the pre-packaged (c)python3 ```pickle```, but I highly reccomend installing ```dill```, as it offers a much wider object type support (including functions). IPy-storage will use ```dill``` as the default serialization protocol if it is installed.

### Instructions
Just %load the storage.py file. It is recommended to include the file in the ipython initialization to avoid doing this for every new interpreter instance. 

## Usage

Your different object sets will be divided in folders that will be inside a base directory. The objects will be saved in those folders in dill/pickle serialization format, depending on which backend you have installed. 

You may create or open a new set with ```%setopen <set_name> <base_dir>```. The default base directory defaults to ```./ipy_db``` and will be placed on the current ipython working dir when a new set is created.

Once a set is open, you may store and retrieve files from a set with ```%setstore <objs_to_store>``` and ```%setload <objs_to_load>```. You may store/load multiple objects at time, e.g. ```%setstore apple,orange,bars```. You can also use ```%setload -a``` to load all objects inside a set at once.

You can use ```%listsets <base_dir>``` to list all sets in the appointed base directory (defaults to ```ipy_db```), and ```%setobjs <set>``` to list all objects inside a set (defaults to the currently open set, if any). 


## Future

I hope to turn this in a more complete helper for Ipython data storage, including the hability to load files from different sets without having to change sets constantly, show stored objects type and size, among others. 

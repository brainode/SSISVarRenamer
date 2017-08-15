#SSIS Variable Renamer

This tool is need for rename variable in SSIS packages(*.dtsx)

##Build

You can build standalone package with [pyinstaller](http://www.pyinstaller.org/).

Tested with **Python 3.5.2**

##Usage

You can type:
    *python SSISVarRenamer.py -h* to get help.
To rename variable:
    *python SSISVarRenamer.py rename CurrientVarName NewVarName* to rename variable in packages.
    
##Problems

If you have Script Component, you must reopen script(Need to refresh meta data).  
    
# pythonProject1

P2 : Utilisez les bases de Python pour l'analyse de marché

* These steps are for Win32 on which the code was built.

* Set up of the environment:

* download of the source files from github:

	cd mypath

	git clone https://github.com/jsoques1/pythonProject1.git
	
* create a virtual environment if not already done:

	python -m venv mypath/venv

* install the additional pip package:
	
	mypath/env/Scripts/activate
		
	pip install -r <mypath>/pythonProject1/requirement.txt

* Execution:

cd mypath/pythonProject1

* usage:

    1) python basic_source.py : creates directories for csv file and images for each book categories
		
    2) python basic_source.py category : creates directories for csv file and images for specified book category
                                      argument category should be a string enclosed by a double quote
				
tab is the separator for the csv file
									  
developped and tested with Pycharm 2021.3 under Win32 Python 3.10.1

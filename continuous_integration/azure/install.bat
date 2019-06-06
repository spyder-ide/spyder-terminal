:: Install dependencies
conda install -q -y -c spyder-ide --file requirements/conda_win.txt
if errorlevel 1 exit 1

conda install -q -y -c spyder-ide --file requirements/tests.txt
if errorlevel 1 exit 1

pip install -q codecov
if errorlevel 1 exit 1
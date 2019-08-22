:: Install dependencies
if %USE_CONDA% == yes (
  if %PYTHON_VERSION% == 3.6 (
    conda install -q -y python=3.6.8=h9f7ef89_7
  )

  conda install -q -y -c spyder-ide --file requirements/conda_win.txt
  if errorlevel 1 exit 1

  conda install -q -y -c spyder-ide --file requirements/tests.txt
  if errorlevel 1 exit 1

  conda install -q -y -c conda-forge nodejs 
  if errorlevel 1 exit 1
) else (
  pip install -r requirements/conda_win.txt
  if errorlevel 1 exit 1

  pip install -r requirements/tests.txt
  if errorlevel 1 exit 1

  if %PYTHON_VERSION% == 3.7 (
    pip install -U pywinpty
    if errorlevel 1 exit 1

    pip install --pre -U spyder
    if errorlevel 1 exit 1
  )

  :: Install nodejs
  pip install nodejs
  if errorlevel 1 exit 1
)

pip install -q codecov
if errorlevel 1 exit 1

:: npm using https for git
git config --global url."https://github.com/".insteadOf git@github.com:
git config --global url."https://".insteadOf git://

:: Install dependencies
if %USE_CONDA% == yes (
  if %PYTHON_VERSION% == 3.6 (
    conda install -q -y python=3.6.8=h9f7ef89_7
  )

  conda install -q -y -c conda-forge --file requirements/conda_win.txt
  if errorlevel 1 exit 1

  conda install -q -y -c conda-forge --file requirements/tests.txt
  if errorlevel 1 exit 1

  conda install -q -y -c conda-forge nodejs
  if errorlevel 1 exit 1

  conda install -q -y -c conda-forge yarn
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
  conda install -q -y -c conda-forge nodejs
  if errorlevel 1 exit 1

  :: Install yarn
  conda install -q -y -c conda-forge yarn
  if errorlevel 1 exit 1
)

pip install -q codecov
if errorlevel 1 exit 1

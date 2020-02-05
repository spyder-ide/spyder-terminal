To release a new version of spyder-terminal:

* git fetch upstream && git merge upstream/master

* Close milestone on Github

* git clean -xfdi

* Update CHANGELOG.md with `loghub -m <milestone> -u <github-user> spyder-ide/spyder-terminal`

* Update VERSION_INFO in `__init__.py` (set release version, remove 'dev0')

* git add and git commit

* python setup.py clean_components

* python setup.py sdist upload

* python3 setup.py bdist_wheel --plat-name win_amd64 upload

* python setup.py bdist_wheel --universal upload

* git tag -a vX.X.X -m 'comment'

* Update VERSION_INFO in `__init__.py` (add 'dev0' and increment minor)

* git add and git commit

* git push upstream master

* git push upstream --tags

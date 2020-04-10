To release a new version of spyder-terminal:

* git fetch upstream && git merge upstream/master

* Close milestone on Zenhub

* git clean -xfdi

* Update CHANGELOG.md with `loghub spyder-ide/spyder-terminal -zr "spyder-terminal vX.X.X"`

* git add and git commit with "Update Changelog"

* Update VERSION_INFO in `__init__.py` (set release version, remove 'dev0')

* git add and git commit with "Release x.x.x"

* python setup.py clean_components

* python setup.py build_static

* python setup.py bdist_wheel --universal

* python setup.py sdist

* twine check dist/*

* twine upload dist/*

* git tag -a vX.X.X -m 'Release x.x.x'

* Update VERSION_INFO in `__init__.py` (add 'dev0' and increment minor)

* git add and git commit

* git push upstream master

* git push upstream --tags

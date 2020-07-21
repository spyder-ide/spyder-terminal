# Release
Follow the steps to release a new version of spyder-terminal

## Translation updates

* Install [gettext-helpers](https://github.com/spyder-ide/gettext-helpers) from source.
* Update the `*.pot` and `*.po` translation files by following these steps:
  * Run `spyder-gettext scan spyder_terminal` to update localization files.
  * Create and merge a new PR with these updated files.
  * Once merged, the new strings are now available on Crowdin.
* Close the current translation PR and delete the `translate/<branch-name>` branch associated with it.
* Go to the [integrations page](https://crowdin.com/project/spyder/settings#integration) on Crowdin and press `Sync now` to open a new translation PR.
* Request translators on a Github issue to update their translations on Crowdin. This can take between a couple of days to a couple of weeks depending on the amount of strings to translate. It's necessary to wait for that before proceeding to the next step.
* Checkout the translation PR and update the `*.mo` files in there by running `spyder-gettext compile spyder_terminal`.
* Squash all commits in that PR into a single one. This commit will include the `*.pot`, `*.po` and `*.mo` file changes.
* Once that's done, merge the PR to finish the process.
* Don't forget to remove your local checkout of `translate/<branch-name>` because that's going to be outdated for next time.

## Release updates
* git fetch upstream && git merge upstream/master

* Close milestone on Zenhub

* Run `check-manifest` to verify that all required files are part of the distribution.

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

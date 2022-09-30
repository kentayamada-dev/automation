.PHONY: install-packages
install-packages:
	pip3 --disable-pip-version-check --no-cache-dir install -r requirements.txt

.PHONY: instagram
instagram:
	python3 instagram.py

.PHONY: twitter
twitter:
	python3 twitter.py

# https://docs.cypress.io/guides/getting-started/installing-cypress#Ubuntu-Debian
.PHONY: install-dependencies
install-dependencies:
	sudo apt-get update && export DEBIAN_FRONTEND=noninteractive \
	&& sudo apt-get -y install --no-install-recommends libgtk2.0-0 libgtk-3-0 libgbm-dev libnotify-dev libgconf-2-4 libnss3 libxss1 libasound2 libxtst6 xauth xvfb

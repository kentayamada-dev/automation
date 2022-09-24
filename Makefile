.PHONY: install-chrome
install-chrome:
	wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add - \
	&& echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/chrome.list \
	&& sudo apt-get update \
	&& sudo apt-get -y install --no-install-recommends google-chrome-stable

.PHONY: install-packages
install-packages:
	pip3 --disable-pip-version-check --no-cache-dir install -r common-requirements.txt -r twitter-requirements.txt -r instagram-requirements.txt

.PHONY: instagram
instagram:
	python3 instagram.py

.PHONY: twitter
twitter:
	python3 twitter.py

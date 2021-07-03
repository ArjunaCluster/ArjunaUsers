# Pull the baseurl from _config.yml
BASEURL ?= $(shell grep baseurl _config.yml | awk '{print $2}')

.PHONY: build serve test install

build: _site/

install: Gemfile.lock pip.install

Gemfile.lock: Gemfile
	bundle install
	touch $@

# Install Python dependencies
pip.install: requirements.txt
	python -m pip install --user -r requirements.txt 2>&1 | tee $@

SRC := $(shell git ls-tree -r --name-only HEAD -- **/*.md)
_site/: Gemfile.lock _config.yml $(SRC)
	rm -rf $@ && mkdir -p $@
	bundle exec jekyll build -d $(join $@, $(BASEURL)) -b $(BASEURL)
	touch $@

# Run test on the website using htmlproofer
test: _site/
	bundle exec htmlproofer \
	--allow-hash-href \
	--disable-external \
	--check-html --check-img-http --enforce-https \
	_site/

# Build and serve the site for viewing locally
serve: _site/ Gemfile.lock
	bundle exec jekyll serve

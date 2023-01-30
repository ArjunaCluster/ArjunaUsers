# Pull the baseurl from _config.yml
BASEURL ?= $(word 2, $(shell grep baseurl _config.yml))

build: _site/

Gemfile.lock: Gemfile
	bundler install
	touch $@

SRC := $(shell git ls-tree -r --name-only HEAD -- **/*.md)
_site/: Gemfile.lock _config.yml $(SRC)
	rm -rf $@ && mkdir -p $@
	bundler exec jekyll build -d $(join $@, $(BASEURL)) -b $(BASEURL)
	touch $@

# Run test on the website using htmlproofer
test: _site/ Gemfile.lock
	bundler exec htmlproofer \
	--root-dir=_site/ \
	--disable-external=true \
	_site/

# Build and serve the site for viewing locally
serve: _site/ Gemfile.lock
	bundler exec jekyll serve

# Archive Site for Publishing
site.zip: _site/
	cd _site/$(BASEURL) &&  zip -r $(abspath site.zip) .
